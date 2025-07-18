## Raiplay Feed

Raiplay feed serve per generare un feed RSS dei podcast RAI che altrimenti sarebbero accessibili solo tramite la loro (pessima) applicazione "RaiPlay Sound". In questo modo si può inserire il feed in ogni lettore podcast.

Lo script è basato sull'ottimo lavoro di: [timendum/raiplaysound](https://github.com/timendum/raiplaysound). Solo leggermente modificato per rispettare correttamente le date di uscita dei podcast, e automatizzata la generazione ogni ora, nel caso fossero presenti nuovi episodi. 

Questo repository è impostato per aggiornarsi automaticamente ogni ora e ricreare i file XML con i nuovi episodi, se presenti. 

Siccome l'ho fatto per me, ho incluso i podcast che mi interessano:

- [Almanacco Mafioso](https://www.raiplaysound.it/programmi/almanaccomafioso)
- [Battiti](https://www.raiplaysound.it/programmi/battiti)
- [Eta Beta](https://www.raiplaysound.it/programmi/etabeta)
- [Detectives - Casi risolti e irrisolti](https://www.raiplaysound.it/programmi/detectives-casirisoltieirrisolti)
- [Giù la maschera](https://www.raiplaysound.it/programmi/giulamaschera)
- [GR 1](https://www.raiplaysound.it/programmi/gr1)
- [GR Friuli Venezia Giulia](https://www.raiplaysound.it/programmi/grfriuliveneziagiulia)
- [Il Ruggito del Coniglio](https://www.raiplaysound.it/programmi/ilruggitodelconiglio)
- [GR Sardegna](https://www.raiplaysound.it/programmi/grsardegna)
- [L'edicola di Radio1](https://www.raiplaysound.it/programmi/ledicoladiradio1)
- [Radio2 Radio Show La Pennicanza](https://www.raiplaysound.it/programmi/radio2radioshowlapennicanza)
- [Radio3 Mondo](https://www.raiplaysound.it/programmi/radio3mondo)
- [Radio3 Scienza](https://www.raiplaysound.it/programmi/radio3scienza)
- [Radio anch'io](https://www.raiplaysound.it/programmi/radioanchio)
- [Revolution](https://www.raiplaysound.it/programmi/revolution)
- [Sotto - Questa lotta ci riguarda](https://www.raiplaysound.it/programmi/sotto-questalottaciriguarda)
- [Tutta la città ne parla](https://www.raiplaysound.it/programmi/tuttalacittaneparla)
- [Tra poco in edicola](https://www.raiplaysound.it/programmi/trapocoinedicola)
- [Un giorno da pecora](https://www.raiplaysound.it/programmi/ungiornodapecora)
- [Zapping](https://www.raiplaysound.it/programmi/zapping)

***

  Per iscriversi ai feed, i link sono:

  - `https://giuliomagnifico.github.io/raiplay-feed/feed_almanaccomafioso.xml`
  - `https://giuliomagnifico.github.io/raiplay-feed/feed_battiti.xml`
  - `https://giuliomagnifico.github.io/raiplay-feed/feed_etabeta.xml`
  - `https://giuliomagnifico.github.io/raiplay-feed/feed_detectives-casirisoltieirrisolti.xml`
  - `https://giuliomagnifico.github.io/raiplay-feed/feed_giulamaschera.xml`
  - `https://giuliomagnifico.github.io/raiplay-feed/feed_gr1.xml`
  - `https://giuliomagnifico.github.io/raiplay-feed/feed_grfriuliveneziagiulia.xml`
  - `https://giuliomagnifico.github.io/raiplay-feed/feed_grsardegna.xml`
  - `https://giuliomagnifico.github.io/raiplay-feed/feed_ilruggitodelconiglio.xml`
  - `https://giuliomagnifico.github.io/raiplay-feed/feed_ledicoladiradio1.xml`
  - `https://giuliomagnifico.github.io/raiplay-feed/feed_radio2radioshowlapennicanza.xml`
  - `https://giuliomagnifico.github.io/raiplay-feed/feed_radio3mondo.xml`
  - `https://giuliomagnifico.github.io/raiplay-feed/feed_radio3scienza.xml`
  - `https://giuliomagnifico.github.io/raiplay-feed/feed_radioanchio.xml`
  - `https://giuliomagnifico.github.io/raiplay-feed/feed_revolution.xml`
  - `https://giuliomagnifico.github.io/raiplay-feed/feed_sotto-questalottaciriguarda.xml`
  - `https://giuliomagnifico.github.io/raiplay-feed/feed_trapocoinedicola.xml`
  - `https://giuliomagnifico.github.io/raiplay-feed/feed_tuttalacittaneparla.xml`
  - `https://giuliomagnifico.github.io/raiplay-feed/feed_ungiornodapecora.xml`
  - `https://giuliomagnifico.github.io/raiplay-feed/feed_zapping.xml`


Se volete altri podcast, provate a scrivermi, appena ho tempo li aggiungo, oppure clonate il repository e aggiungeteli voi nel file [generate_feeds.py](https://github.com/giuliomagnifico/raiplay-feed/blob/main/scripts/generate_feeds.py)
<br><br><br>


>[!WARNING]
>è presente un problema di redirect e cache su Pocket Casts, per gli altri podcast player funzionano correttamente. 
>
>Se usate PocketCasts quando premete play vi dira che c'è un problema di connessione, basta scaricare il file o aspettare che scarichi il file e poi riparte. In poche parole, quando premete play, invece di fare lo streaming, va a scaricare il file, quindi vi dirà che c'è un errore ma in realtà lo sta scaricando in background. 
>
>È un problema solo di PocketCast perchè non fa partire lo streaming se c'è una redirect, sono in contatto con il loro supporto per sperare di risolvere questo fastidioso problema. 
>
>Nel frattempo, io ho attivato il download automatico per i podcast giornalieri così li trovo direttamemte scaricati nel caso usassi la coda di riproduzione. 
