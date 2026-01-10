import os
import re
import tempfile
from datetime import datetime as dt
from itertools import chain
from urllib.parse import urljoin

import requests
from feedendum import Feed, FeedItem, to_rss_string

NSITUNES = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"


def url_to_filename(url: str) -> str:
    return url.split("/")[-1] + ".xml"


def _datetime_parser(s: str) -> dt:
    if not s:
        return dt.now()

    s = str(s).strip()

    formats = [
        "%a, %d %b %Y %H:%M:%S %z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d %b %Y",
        "%d-%m-%Y %H:%M:%S",
    ]
    for fmt in formats:
        try:
            return dt.strptime(s, fmt)
        except ValueError:
            continue

    # fallback: prova a prendere solo la data (es. "09 Gen 2026" non arriverà dal JSON, ma teniamolo robusto)
    m = re.search(r"(\d{4}-\d{2}-\d{2})", s)
    if m:
        try:
            return dt.strptime(m.group(1), "%Y-%m-%d")
        except ValueError:
            pass

    return dt.now()


def _iter_episode_like_nodes(node):
    """
    Estrae ricorsivamente i dict che sembrano episodi:
    - hanno track_info (o page_url) e un audio o downloadable_audio
    """
    if isinstance(node, dict):
        has_track = isinstance(node.get("track_info"), dict) or isinstance(node.get("trackInfo"), dict) or "page_url" in node
        has_audio = isinstance(node.get("audio"), dict) or isinstance(node.get("downloadable_audio"), dict) or isinstance(node.get("downloadableAudio"), dict)
        if has_track and has_audio:
            yield node

        for v in node.values():
            yield from _iter_episode_like_nodes(v)

    elif isinstance(node, list):
        for v in node:
            yield from _iter_episode_like_nodes(v)


class RaiParser:
    def __init__(self, url: str, folderPath: str) -> None:
        self.url = url.rstrip("/")
        self.folderPath = folderPath

        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (compatible; raiplay-feed/1.0; +https://github.com/giuliomagnifico/raiplay-feed)",
                "Accept": "application/json,text/plain,*/*",
            }
        )

    def process(self) -> None:
        r = self.session.get(self.url + ".json", timeout=20)
        r.raise_for_status()
        rdata = r.json()

        feed = Feed()
        feed.title = rdata.get("title") or rdata.get("name") or self.url
        pi = rdata.get("podcast_info") or {}
        feed.description = pi.get("description") or feed.title
        feed.url = self.url

        img = pi.get("image") or rdata.get("image")
        if img:
            feed._data["image"] = {"url": urljoin(self.url + "/", img)}

        feed._data[f"{NSITUNES}author"] = "RaiPlaySound"
        feed._data["language"] = "it-it"
        feed._data[f"{NSITUNES}owner"] = {f"{NSITUNES}email": "giuliomagnifico@gmail.com"}

        # categorie: prova a comporle se ci sono
        genres = pi.get("genres") or []
        subgenres = pi.get("subgenres") or []
        dfp = pi.get("dfp") or {}
        esc_genres = dfp.get("escaped_genres") or []
        esc_typ = dfp.get("escaped_typology") or []
        categories = {c.get("name") for c in chain(genres, subgenres) if isinstance(c, dict) and c.get("name")}
        categories |= {c for c in chain(esc_genres, esc_typ) if isinstance(c, str) and c}

        if categories:
            feed._data[f"{NSITUNES}category"] = [{"@text": c} for c in sorted(categories)]

        feed.items = []

        # Estrazione episodi robusta (non dipende solo da rdata["block"]["cards"])
        for item in _iter_episode_like_nodes(rdata):
            # audio dict
            audio = item.get("audio") or {}
            d_audio = item.get("downloadable_audio") or {}

            track_info = item.get("track_info") or {}
            page_url = track_info.get("page_url") or item.get("page_url")
            if not page_url:
                continue

            title = item.get("toptitle") or item.get("title") or track_info.get("title") or "Senza titolo"
            uniq = item.get("uniquename") or track_info.get("uniquename") or page_url

            fitem = FeedItem()
            fitem.title = title
            fitem.id = "giuliomagnifico-raiplay-feed-" + str(uniq)
            fitem.update = _datetime_parser(track_info.get("date") or track_info.get("publish_date") or item.get("date"))
            fitem.url = urljoin(self.url + "/", page_url)
            fitem.content = item.get("description") or track_info.get("description") or title

            enclosure_url = None
            if isinstance(d_audio, dict) and d_audio.get("url"):
                enclosure_url = str(d_audio["url"]).replace("http:", "https:")
            elif isinstance(audio, dict) and audio.get("url"):
                enclosure_url = str(audio["url"]).replace("http:", "https:")

            if not enclosure_url:
                continue

            duration = None
            if isinstance(audio, dict):
                duration = audio.get("duration")

            img = item.get("image") or track_info.get("image")
            if img:
                img = urljoin(self.url + "/", img)

            fitem._data = {
                "enclosure": {
                    "@type": "audio/mpeg",
                    "@url": urljoin(self.url + "/", enclosure_url),
                },
                f"{NSITUNES}title": fitem.title,
                f"{NSITUNES}summary": fitem.content,
            }

            if duration is not None:
                fitem._data[f"{NSITUNES}duration"] = duration
            if img:
                fitem._data["image"] = {"url": img}

            feed.items.append(fitem)

        # ordina e dedup (per sicurezza)
        feed.items.sort(key=lambda x: x.update, reverse=True)
        seen = set()
        deduped = []
        for it in feed.items:
            if it.id in seen:
                continue
            seen.add(it.id)
            deduped.append(it)
        feed.items = deduped

        filename = os.path.join(self.folderPath, url_to_filename(self.url))
        atomic_write(filename, to_rss_string(feed))


def atomic_write(filename, content: str):
    tmp = tempfile.NamedTemporaryFile(
        mode="w", encoding="utf8", delete=False,
        dir=os.path.dirname(filename), prefix=".tmp-single-", suffix=".xml"
    )
    tmp.write(content)
    tmp.close()
    os.replace(tmp.name, filename)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Genera RSS da RaiPlaySound",
        epilog="Info su https://github.com/giuliomagnifico/raiplay-feed/"
    )
    parser.add_argument("url", help="URL podcast RaiPlaySound")
    parser.add_argument("-f", "--folder", default=".", help="Cartella output")
    args = parser.parse_args()

    RaiParser(args.url, args.folder).process()


if __name__ == "__main__":
    main()
