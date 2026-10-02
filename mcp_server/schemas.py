from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def _python_value(value: Any) -> Any:
    if value is None:
        return None
    try:
        import math

        if isinstance(value, float) and math.isnan(value):
            return None
    except Exception:
        pass
    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            return value
    return value


@dataclass(slots=True)
class ColumnProfile:
    name: str
    dtype: str
    null_count: int
    non_null_count: int
    sample_values: list[Any] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "dtype": self.dtype,
            "null_count": self.null_count,
            "non_null_count": self.non_null_count,
            "sample_values": [_python_value(value) for value in self.sample_values],
        }


@dataclass(slots=True)
class DatasetSummary:
    source_path: str
    row_count: int
    column_count: int
    columns: list[ColumnProfile]
    preview_rows: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_path": self.source_path,
            "row_count": self.row_count,
            "column_count": self.column_count,
            "columns": [column.to_dict() for column in self.columns],
            "preview_rows": [
                {key: _python_value(value) for key, value in row.items()}
                for row in self.preview_rows
            ],
        }


@dataclass(slots=True)
class CleanReport:
    source_path: str
    output_path: str | None
    rows_before: int
    rows_after: int
    rows_removed: int
    columns_trimmed: int
    numeric_fill_strategy: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_path": self.source_path,
            "output_path": self.output_path,
            "rows_before": self.rows_before,
            "rows_after": self.rows_after,
            "rows_removed": self.rows_removed,
            "columns_trimmed": self.columns_trimmed,
            "numeric_fill_strategy": self.numeric_fill_strategy,
        }
