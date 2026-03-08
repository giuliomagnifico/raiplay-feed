import os
import re
import tempfile
from datetime import datetime as dt
from itertools import chain
from urllib.parse import urljoin, urlparse

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
        has_track = (
            isinstance(node.get("track_info"), dict)
            or isinstance(node.get("trackInfo"), dict)
            or "page_url" in node
        )
        has_audio = (
            isinstance(node.get("audio"), dict)
            or isinstance(node.get("downloadable_audio"), dict)
            or isinstance(node.get("downloadableAudio"), dict)
        )
        if has_track and has_audio:
            yield node

        for v in node.values():
            yield from _iter_episode_like_nodes(v)

    elif isinstance(node, list):
        for v in node:
            yield from _iter_episode_like_nodes(v)


def resolve_final_audio_url(session: requests.Session, url: str) -> str | None:
    """
    Risolve il link audio finale.
    Accetta solo file audio diretti (.mp3/.m4a/.aac o content-type audio/*).
    Scarta relinker non risolti, playlist HLS (.m3u8) e risposte HTML/XML.
    """
    if not url:
        return None

    url = str(url).replace("http:", "https:")

    try:
        r = session.get(url, allow_redirects=True, timeout=20, stream=True)
        final_url = r.url
        content_type = (r.headers.get("content-type") or "").lower()
        r.close()
    except requests.RequestException:
        return None

    if not final_url:
        return None

    parsed = urlparse(final_url)
    path = (parsed.path or "").lower()

    if "relinkerservlet" in path:
        return None

    if path.endswith(".m3u8") or "application/vnd.apple.mpegurl" in content_type:
        return None

    if path.endswith(".mp3") or path.endswith(".m4a") or path.endswith(".aac"):
        return final_url

    if content_type.startswith("audio/"):
        return final_url

    return None


def get_content_length(session: requests.Session, url: str) -> str | None:
    """
    Recupera content-length se disponibile.
    """
    try:
        r = session.head(url, allow_redirects=True, timeout=20)
        if r.ok:
            length = r.headers.get("content-length")
            if length and length.isdigit():
                return length
    except requests.RequestException:
        pass

    try:
        r = session.get(url, allow_redirects=True, timeout=20, stream=True)
        if r.ok:
            length = r.headers.get("content-length")
            r.close()
            if length and length.isdigit():
                return length
    except requests.RequestException:
        pass

    return None


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
        feed._data[f"{NSITUNES}owner"] = {
            f"{NSITUNES}email": "giuliomagnifico@gmail.com"
        }

        genres = pi.get("genres") or []
        subgenres = pi.get("subgenres") or []
        dfp = pi.get("dfp") or {}
        esc_genres = dfp.get("escaped_genres") or []
        esc_typ = dfp.get("escaped_typology") or []
        categories = {
            c.get("name")
            for c in chain(genres, subgenres)
            if isinstance(c, dict) and c.get("name")
        }
        categories |= {
            c for c in chain(esc_genres, esc_typ) if isinstance(c, str) and c
        }

        if categories:
            feed._data[f"{NSITUNES}category"] = [
                {"@text": c} for c in sorted(categories)
            ]

        feed.items = []

        for item in _iter_episode_like_nodes(rdata):
            audio = item.get("audio") or {}
            d_audio = item.get("downloadable_audio") or {}

           
