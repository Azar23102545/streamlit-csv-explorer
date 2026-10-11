"""Testar själva Streamlit-appen med Streamlits inbyggda testverktyg AppTest
AppTest kör app.py utan webbläsare så vi kan kontrollera vad som visas """

from pathlib import Path

from streamlit.testing.v1 import AppTest

APP_PATH = str(Path(__file__).parent.parent / "app.py")


def test_app_starts_without_file():
    at = AppTest.from_file(APP_PATH).run()
    assert not at.exception
    assert at.title[0].value == "CSV-utforskaren"
    assert "Ingen fil uppladdad" in at.info[0].value


def test_rerun_counter_increases():
    at = AppTest.from_file(APP_PATH).run()
    assert at.sidebar.metric[0].value == "1"
    at.run()  # simulerar att användaren gör något -> hela skriptet körs om
    assert at.sidebar.metric[0].value == "2"

