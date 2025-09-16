import os
from single import RaiParser

SCRIPT_PATH = os.path.abspath("scripts/single.py")
PROGRAMS = {
    "almanaccomafioso": "https://www.raiplaysound.it/programmi/almanaccomafioso",
    "ungiornodapecora": "https://www.raiplaysound.it/programmi/ungiornodapecora",
    "zapping": "https://www.raiplaysound.it/programmi/zapping",
    "radioanchio": "https://www.raiplaysound.it/programmi/radioanchio",
    "trapocoinedicola": "https://www.raiplaysound.it/programmi/trapocoinedicola",
    "radio3scienza": "https://www.raiplaysound.it/programmi/radio3scienza",
    "etabeta": "https://www.raiplaysound.it/programmi/etabeta",
    "ledicoladiradio1": "https://www.raiplaysound.it/programmi/ledicoladiradio1",
    "gr1": "https://www.raiplaysound.it/programmi/gr1",
    "grfriuliveneziagiulia": "https://www.raiplaysound.it/programmi/grfriuliveneziagiulia",
    "grsardegna": "https://www.raiplaysound.it/programmi/grsardegna",
    "gr3": "https://www.raiplaysound.it/programmi/gr3",
    "detectives-casirisoltieirrisolti": "https://www.raiplaysound.it/programmi/detectives-casirisoltieirrisolti",
    "radio3mondo": "https://www.raiplaysound.it/programmi/radio3mondo",
    "sotto-questalottaciriguarda": "https://www.raiplaysound.it/programmi/sotto-questalottaciriguarda",
    "battiti": "https://www.raiplaysound.it/programmi/battiti",
    "giulamaschera": "https://www.raiplaysound.it/programmi/giulamaschera",
    "radio2radioshowlapennicanza": "https://www.raiplaysound.it/programmi/radio2radioshowlapennicanza",
    "revolution": "https://www.raiplaysound.it/programmi/revolution",
    "ilruggitodelconiglio": "https://www.raiplaysound.it/programmi/ilruggitodelconiglio",
    "tuttalacittaneparla": "https://www.raiplaysound.it/programmi/tuttalacittaneparla",
    "primapagina": "https://www.raiplaysound.it/programmi/primapagina",
    "fahrenheit": "https://www.raiplaysound.it/programmi/fahrenheit",
    "hollywoodparty": "https://www.raiplaysound.it/programmi/hollywoodparty",
    "lidealista": "https://www.raiplaysound.it/programmi/lidealista",
    "lamusicatralerighe": "https://www.raiplaysound.it/programmi/lamusicatralerighe",
    "wikiradio": "https://www.raiplaysound.it/programmi/wikiradio",
    "wikiradiolevocidellastoria": "https://www.raiplaysound.it/programmi/wikiradiolevocidellastoria",
    "grsicilia": "https://www.raiplaysound.it/programmi/grsicilia"
}
for name, url in PROGRAMS.items():
    print(f"Generazione feed per {name}...")
    try:
        rai_parser = RaiParser(url, ".")
        rai_parser.process()
        original_file = f"{name}.xml"
        if not os.path.exists(original_file):
            print(f"Errore: Il file {original_file} non è stato generato correttamente!")
            continue
        new_file = f"feed_{name}.xml"
        os.rename(original_file, new_file)
        print(f"Feed XML salvato correttamente: {new_file}")
    except Exception as e:
        print(f"Errore generico per {name}: {e}")
