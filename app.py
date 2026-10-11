"""Streamlit-app: ladda upp en CSV-fil och få en snabb överblick. Starta med:  streamlit run app.py """

import logging

import streamlit as st

from csv_explorer import chart_data, get_dataset_info, missing_values_table, numeric_summary, read_csv_bytes

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)


@st.cache_data
def load_data(file_content: bytes):
    """Läser filen. Tack vare cachen läses samma fil bara in en gång,
    även om skriptet körs om många gånger."""
    logger.info("Läser in fil (cachen saknade denna fil)")
    return read_csv_bytes(file_content)


st.set_page_config(page_title="CSV-utforskaren", layout="wide")
st.title("CSV-utforskaren")
st.write("Ladda upp en CSV-fil så får du en snabb överblick över datan.")

# Räknare som visar hur många gånger skriptet har körts (pedagogiskt exempel på rerun).
if "reruns" not in st.session_state:
    st.session_state.reruns = 0
st.session_state.reruns += 1
st.sidebar.metric("Antal körningar", st.session_state.reruns)

uploaded_file = st.file_uploader("Välj en CSV-fil", type="csv")

if uploaded_file is None:
    st.info("Ingen fil uppladdad än.")
    st.stop()

try:
    df = load_data(uploaded_file.getvalue())
except ValueError as error:
    st.error(f"Kunde inte läsa filen: {error}")
    st.stop()

# --- Överblick ---
info = get_dataset_info(df)
col1, col2, col3 = st.columns(3)
col1.metric("Rader", info.rows)
col2.metric("Kolumner", info.columns)
col3.metric("Saknade värden", info.missing_values)

st.subheader("Första raderna")
st.dataframe(df.head(10))

# --- Sammanfattningar ---
st.subheader("Numeriska kolumner")
summary = numeric_summary(df)
if summary.empty:
    st.write("Datan har inga numeriska kolumner.")
else:
    st.dataframe(summary)

st.subheader("Saknade värden per kolumn")
missing = missing_values_table(df)
if missing.empty:
    st.success("Inga saknade värden.")
else:
    st.dataframe(missing, hide_index=True)

# --- Diagram ---
st.subheader("Diagram")
column = st.selectbox("Välj en kolumn", df.columns)
try:
    st.bar_chart(chart_data(df, column), x="värde", y="antal")
except ValueError as error:
    st.warning(str(error))
