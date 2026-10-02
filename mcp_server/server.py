from __future__ import annotations

from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from mcp_server.config import load_config
from mcp_server.tools import analyze_dataframe, clean_dataframe, load_dataframe, profile_dataframe, save_dataframe


SERVER_NAME = "ccaf-data-tools"
mcp = FastMCP(SERVER_NAME)


@mcp.tool()
def load_dataset(path: str, preview_rows: int = 5) -> dict[str, Any]:
    dataframe = load_dataframe(path)
    return profile_dataframe(dataframe, source_path=str(Path(path).resolve()), preview_rows=preview_rows)


@mcp.tool()
def profile_dataset(path: str, preview_rows: int = 5) -> dict[str, Any]:
    dataframe = load_dataframe(path)
    return profile_dataframe(dataframe, source_path=str(Path(path).resolve()), preview_rows=preview_rows)


@mcp.tool()
def analyze_dataset(path: str) -> dict[str, Any]:
    dataframe = load_dataframe(path)
    return analyze_dataframe(dataframe)


@mcp.tool()
def clean_dataset(path: str, output_path: str | None = None) -> dict[str, Any]:
    config = load_config()
    dataframe = load_dataframe(path)
    cleaned, report = clean_dataframe(dataframe, config=config)

    saved_output: Path | None = None
    if output_path is not None:
        saved_output = save_dataframe(cleaned, output_path)

    report["source_path"] = str(Path(path).resolve())
    report["output_path"] = str(saved_output.resolve()) if saved_output is not None else None
    return report


@mcp.tool()
def save_dataset(path: str, output_path: str) -> dict[str, Any]:
    dataframe = load_dataframe(path)
    saved_path = save_dataframe(dataframe, output_path)
    return {
        "source_path": str(Path(path).resolve()),
        "output_path": str(saved_path.resolve()),
    }


def build_server() -> FastMCP:
    return mcp


def main() -> None:
    build_server().run()


if __name__ == "__main__":
    main()
