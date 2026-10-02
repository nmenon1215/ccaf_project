from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True, slots=True)
class ServerConfig:
    preview_rows: int = int(os.getenv("CCAF_PREVIEW_ROWS", "5"))
    output_dir: Path = Path(os.getenv("CCAF_OUTPUT_DIR", "artifacts"))
    numeric_fill_strategy: str = os.getenv("CCAF_NUMERIC_FILL", "median")


def load_config() -> ServerConfig:
    return ServerConfig()
