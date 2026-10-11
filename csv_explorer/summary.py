"""Sammanfattningar av en DataFrame. All beräkningslogik ligger här separat från Streamlit-koden i app.py """

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class DatasetInfo:
    """ Grundläggande fakta om ett dataset """

    rows: int
    columns: int
    numeric_columns: list[str]
    missing_values: int


def get_dataset_info(df: pd.DataFrame) -> DatasetInfo:
    """ Returnerar antal rader, kolumner, numeriska kolumner och saknade värden """
    return DatasetInfo(
        rows=len(df),
        columns=len(df.columns),
        numeric_columns=df.select_dtypes(include="number").columns.tolist(),
        missing_values=int(df.isna().sum().sum()),
    )


def numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    """ Medelvärde, min och max för varje numerisk kolumn """
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.empty:
        return pd.DataFrame(columns=["medel", "min", "max"])

    summary = numeric_df.agg(["mean", "min", "max"]).T
    summary.columns = ["medel", "min", "max"]
    return summary.round(2)


def missing_values_table(df: pd.DataFrame) -> pd.DataFrame:
    """Tabell med antal saknade värden per kolumn (bara kolumner med saknade värden)."""
    missing = df.isna().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    return missing.rename("saknade").rename_axis("kolumn").reset_index()


def chart_data(df: pd.DataFrame, column: str, bins: int = 10) -> pd.DataFrame:
    """Förbereder data för ett stapeldiagram över en vald kolumn 

    - Numerisk kolumn: värdena delas in i intervall och räknas 
    - Textkolumn: de 10 vanligaste värdena räknas """
    if column not in df.columns:
        raise ValueError(f"Kolumnen '{column}' finns inte i datan.")

    values = df[column].dropna()
    if values.empty:
        raise ValueError(f"Kolumnen '{column}' har bara saknade värden.")

    if pd.api.types.is_numeric_dtype(values):
        counts = pd.cut(values, bins=min(bins, values.nunique())).value_counts().sort_index()
        labels = counts.index.astype(str)
    else:
        counts = values.astype(str).value_counts().head(10)
        labels = counts.index

    return pd.DataFrame({"värde": labels, "antal": counts.to_numpy()})