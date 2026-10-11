"""Tester för inläsning och sammanfattningar"""

import pandas as pd
import pytest

from csv_explorer import chart_data, get_dataset_info, missing_values_table, numeric_summary, read_csv_bytes


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "region": ["Göteborg", "Malmö", None, "Göteborg"],
        "antal": [1, 2, 3, None],
        "pris": [100.0, 200.0, 300.0, 400.0],
    })


#  Inläsning 

def test_read_csv_bytes_reads_valid_file():
    content = "a,b\n1,2\n3,4\n".encode("utf-8")
    df = read_csv_bytes(content)
    assert df.shape == (2, 2)
    assert list(df.columns) == ["a", "b"]


@pytest.mark.parametrize("content", [b"", b"a,b\n"])
def test_read_csv_bytes_rejects_empty_data(content):
    with pytest.raises(ValueError):
        read_csv_bytes(content)


# Sammanfattningar

def test_get_dataset_info(sample_df):
    info = get_dataset_info(sample_df)
    assert info.rows == 4
    assert info.columns == 3
    assert info.numeric_columns == ["antal", "pris"]
    assert info.missing_values == 2


def test_numeric_summary(sample_df):
    summary = numeric_summary(sample_df)
    assert summary.loc["pris", "medel"] == pytest.approx(250.0)
    assert summary.loc["antal", "min"] == 1
    assert summary.loc["antal", "max"] == 3
    assert "region" not in summary.index


def test_numeric_summary_without_numeric_columns():
    df = pd.DataFrame({"namn": ["a", "b"]})
    assert numeric_summary(df).empty


def test_missing_values_table(sample_df):
    table = missing_values_table(sample_df)
    assert set(table["kolumn"]) == {"region", "antal"}
    assert table["saknade"].sum() == 2


def test_summary_does_not_change_original(sample_df):
    original = sample_df.copy()
    numeric_summary(sample_df)
    missing_values_table(sample_df)
    pd.testing.assert_frame_equal(sample_df, original)


#  Diagramdata 

def test_chart_data_text_column(sample_df):
    result = chart_data(sample_df, "region")
    counts = dict(zip(result["värde"], result["antal"]))
    assert counts == {"Göteborg": 2, "Malmö": 1}


def test_chart_data_numeric_column_counts_all_values(sample_df):
    result = chart_data(sample_df, "pris")
    assert result["antal"].sum() == 4


def test_chart_data_unknown_column(sample_df):
    with pytest.raises(ValueError, match="finns inte"):
        chart_data(sample_df, "finns_ej")

