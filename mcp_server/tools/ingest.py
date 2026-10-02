from __future__ import annotations

from pathlib import Path

import pandas as pd


def detect_dataset_format(path: str | Path) -> str:
    suffix = Path(path).suffix.lower()
    if suffix == ".csv":
        return "csv"
    if suffix == ".json":
        return "json"
    if suffix == ".parquet":
        return "parquet"
    raise ValueError(f"Unsupported dataset format: {suffix or '<no extension>'}")


def load_dataframe(path: str | Path) -> pd.DataFrame:
    dataset_path = Path(path)
    dataset_format = detect_dataset_format(dataset_path)

    if dataset_format == "csv":
        return pd.read_csv(dataset_path)

    if dataset_format == "json":
        try:
            return pd.read_json(dataset_path)
        except ValueError:
            return pd.read_json(dataset_path, lines=True)

    if dataset_format == "parquet":
        return pd.read_parquet(dataset_path)

    raise ValueError(f"Unsupported dataset format: {dataset_format}")


def save_dataframe(dataframe: pd.DataFrame, path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    suffix = output_path.suffix.lower()
    if suffix == ".csv":
        dataframe.to_csv(output_path, index=False)
    elif suffix == ".json":
        dataframe.to_json(output_path, orient="records", indent=2)
    elif suffix == ".parquet":
        dataframe.to_parquet(output_path, index=False)
    else:
        raise ValueError(f"Unsupported output format: {suffix or '<no extension>'}")

    return output_path
