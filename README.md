# CSV-utforskaren – en Streamlit-app

En liten Streamlit-app där man laddar upp en CSV-fil och får en snabb överblick:

- antal rader, kolumner och saknade värden,
- de första raderna i en tabell,
- medelvärde, min och max för numeriska kolumner,
- saknade värden per kolumn,
- ett stapeldiagram för en kolumn som användaren väljer.

Om filen är tom eller inte går att läsa visar appen ett tydligt felmeddelande i stället för att krascha.

Projektet är gjort för fördjupningsuppgiften i kursen *Fördjupning i Pythonprogrammering*.

## Installation

```bash
python -m venv .venv
```

Aktivera miljön:

- Windows: `.venv\Scripts\activate`
- Mac/Linux: `source .venv/bin/activate`

Installera beroenden:

```bash
pip install -r requirements.txt
```

Beroenden: `streamlit`, `pandas`, `pytest`.

## Köra appen

```bash
streamlit run app.py
```

Appen öppnas i webbläsaren

## Testdata

I mappen `data/` finns:

- `exempel_forsaljning.csv` – påhittad försäljningsdata (60 rader) med några saknade värden. Skapad av Claude för att testa appen.
- `tom_fil.csv` – en tom fil för att visa felhanteringen.

## Köra testerna

```bash
pytest
```

- `tests/test_logic.py` testar inläsning och beräkningar.
- `tests/test_app.py` testar själva appen med Streamlits testverktyg `AppTest`.

## Projektstruktur

```
streamlit-csv-explorer/
├── app.py                
├── csv_explorer/
│   ├── __init__.py
│   ├── loading.py         
│   └── summary.py          
├── tests/
│   ├── test_logic.py
│   └── test_app.py
├── data/
│   ├── exempel_forsaljning.csv
│   └── tom_fil.csv
├── rapport.md
├── pyproject.toml          
├── requirements.txt
└── README.md
```

Logiken ligger i `csv_explorer/` och vet ingenting om Streamlit. Därför kan den testas med vanlig pytest. `app.py` sköter bara det som visas på skärmen.
