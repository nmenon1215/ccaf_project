from __future__ import annotations

from typing import Any

import pandas as pd

from mcp_server.config import ServerConfig
from mcp_server.schemas import CleanReport


def clean_dataframe(dataframe: pd.DataFrame, config: ServerConfig | None = None) -> tuple[pd.DataFrame, dict[str, Any]]:
    config = config or ServerConfig()
    cleaned = dataframe.copy()
    columns_trimmed = 0

    for column_name in cleaned.select_dtypes(include=["object", "string"]).columns:
        cleaned[column_name] = cleaned[column_name].astype("string").str.strip()
        columns_trimmed += 1

    cleaned = cleaned.drop_duplicates()

    for column_name in cleaned.select_dtypes(include="number").columns:
        if cleaned[column_name].isna().any():
            if config.numeric_fill_strategy == "mean":
                fill_value = cleaned[column_name].mean()
            else:
                fill_value = cleaned[column_name].median()
            cleaned[column_name] = cleaned[column_name].fillna(fill_value)

    report = CleanReport(
        source_path="",
        output_path=None,
        rows_before=int(len(dataframe)),
        rows_after=int(len(cleaned)),
        rows_removed=int(len(dataframe) - len(cleaned)),
        columns_trimmed=columns_trimmed,
        numeric_fill_strategy=config.numeric_fill_strategy,
    )
    return cleaned, report.to_dict()
