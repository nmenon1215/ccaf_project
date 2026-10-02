from __future__ import annotations

from pathlib import Path

import pandas as pd

from mcp_server.tools.clean import clean_dataframe
from mcp_server.tools.ingest import detect_dataset_format, load_dataframe, save_dataframe
from mcp_server.tools.profile import analyze_dataframe, profile_dataframe


def test_detect_dataset_format_csv(tmp_path: Path) -> None:
    path = tmp_path / "sample.csv"
    path.write_text("name,age\nAda,36\n", encoding="utf-8")

    assert detect_dataset_format(path) == "csv"


def test_profile_dataframe(tmp_path: Path) -> None:
    frame = pd.DataFrame({"name": ["Ada", "Grace"], "age": [36, 45]})

    result = profile_dataframe(frame, source_path=str(tmp_path / "sample.csv"), preview_rows=1)

    assert result["row_count"] == 2
    assert result["column_count"] == 2
    assert result["columns"][0]["name"] == "name"
    assert result["preview_rows"] == [{"name": "Ada", "age": 36}]


def test_clean_dataframe_fills_numeric_and_trims_strings() -> None:
    frame = pd.DataFrame({"name": [" Ada ", "Ada", None], "age": [36, 36, 45]})

    cleaned, report = clean_dataframe(frame)

    assert list(cleaned["name"].dropna()) == ["Ada"]
    assert report["rows_removed"] == 1
    assert cleaned["age"].isna().sum() == 0


def test_save_and_reload_dataframe(tmp_path: Path) -> None:
    frame = pd.DataFrame({"name": ["Ada"], "age": [36]})
    output_path = tmp_path / "output.csv"

    saved_path = save_dataframe(frame, output_path)
    reloaded = load_dataframe(saved_path)

    assert saved_path == output_path
    assert reloaded.to_dict(orient="records") == [{"name": "Ada", "age": 36}]


def test_analyze_dataframe() -> None:
    frame = pd.DataFrame({"team": ["A", "A", "B"], "score": [1, 2, 3]})

    analysis = analyze_dataframe(frame)

    assert analysis["row_count"] == 3
    assert analysis["numeric_summary"]["score"]["mean"] == 2.0
    assert analysis["categorical_summary"]["team"]["A"] == 2
