""" Inläsning av CSV-filer. Den här modulen vet ingenting om Streamlit. Den tar emot filens innehåll
som bytes och returnerar en DataFrame. Det gör att funktionen går att
testa med pytest utan att starta någon app """

import io
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def read_csv_bytes(file_content: bytes) -> pd.DataFrame:
    """Läser CSV-data (bytes) och returnerar en DataFrame """
    if not file_content:
        raise ValueError("Filen är tom.")

    try:
        df = pd.read_csv(io.BytesIO(file_content))
    except pd.errors.EmptyDataError as error:
        raise ValueError("Filen innehåller ingen data.") from error
    except pd.errors.ParserError as error:
        raise ValueError("Filen kunde inte tolkas som en CSV-fil.") from error
    except UnicodeDecodeError as error:
        raise ValueError("Filen har fel teckenkodning. Spara den som UTF-8.") from error

    if df.empty:
        raise ValueError("Filen har kolumnnamn men inga rader.")

    logger.info("Läste in %d rader och %d kolumner", len(df), len(df.columns))
    return df