from __future__ import annotations

from typing import Any

import pandas as pd

from mcp_server.schemas import ColumnProfile, DatasetSummary


def _sample_values(series: pd.Series, limit: int = 3) -> list[Any]:
    values: list[Any] = []
    for value in series.dropna().head(limit).tolist():
        values.append(value)
    return values


def profile_dataframe(dataframe: pd.DataFrame, source_path: str, preview_rows: int = 5) -> dict[str, Any]:
    columns = [
        ColumnProfile(
            name=str(column_name),
            dtype=str(dataframe[column_name].dtype),
            null_count=int(dataframe[column_name].isna().sum()),
            non_null_count=int(dataframe[column_name].notna().sum()),
            sample_values=_sample_values(dataframe[column_name]),
        )
        for column_name in dataframe.columns
    ]

    preview = dataframe.head(preview_rows).to_dict(orient="records")
    summary = DatasetSummary(
        source_path=source_path,
        row_count=int(len(dataframe)),
        column_count=int(len(dataframe.columns)),
        columns=columns,
        preview_rows=preview,
    )
    return summary.to_dict()


def analyze_dataframe(dataframe: pd.DataFrame) -> dict[str, Any]:
    numeric_columns = dataframe.select_dtypes(include="number")
    categorical_columns = dataframe.select_dtypes(exclude="number")

    analysis: dict[str, Any] = {
        "row_count": int(len(dataframe)),
        "column_count": int(len(dataframe.columns)),
        "numeric_summary": {},
        "categorical_summary": {},
    }

    if not numeric_columns.empty:
        analysis["numeric_summary"] = numeric_columns.describe().to_dict()

    if not categorical_columns.empty:
        analysis["categorical_summary"] = {
            str(column_name): categorical_columns[column_name].astype("string").value_counts(dropna=False).head(10).to_dict()
            for column_name in categorical_columns.columns
        }

    return analysis
