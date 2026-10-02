# CCAF Project

A capstone project for building an AI-assisted data workflow that can ingest datasets, clean them, and produce analytical insights.

This repository is structured around a split between orchestration, prompt design, and tool execution:

- `orchestrator/` contains the workflow logic that decides what tasks to run
- `prompts/` contains the prompt strategy and agent instructions
- `mcp_server/` is the canonical Python package that exposes concrete data operations
- `eval/` contains evaluation scenarios and expected behaviors
- `docs/` contains architecture and design notes

## Current architecture

The project currently follows a Python MCP server pattern:

- The MCP server lives in `mcp_server/`
- Tool modules are separated by responsibility:
  - `ingest.py` for loading/saving data
  - `profile.py` for dataset inspection and summary metrics
  - `clean.py` for trimming, deduplication, and missing-value handling
- The server entrypoint is `mcp_server/server.py`
- VS Code can launch the server via `.vscode/mcp.json`

## Project goals

The AI workflow is intended to support a simple but powerful sequence:

1. Accept a dataset from a user or file path
2. Inspect schema, types, and quality issues
3. Clean malformed or incomplete values
4. Run analysis or summary generation
5. Export the cleaned and analyzed result

This pattern makes the system modular: the orchestrator decides the sequence, while the MCP server provides execution tools used by the agent.

## Repository layout

```text
ccaf_project/
├── .vscode/
│   └── mcp.json
├── .gitignore
├── docs/
│   └── architecture.md
├── eval/
│   └── test_cases.md
├── mcp_server/
│   ├── __init__.py
│   ├── config.py
│   ├── schemas.py
│   ├── server.py
│   └── tools/
│       ├── __init__.py
│       ├── ingest.py
│       ├── profile.py
│       └── clean.py
├── orchestrator/
│   ├── base_agent.py
│   └── main.py
├── prompts/
│   └── prompts.md
├── tests/
│   └── test_tools.py
├── pyproject.toml
├── README.md
```

## MCP tool server

The MCP server exposes dataset-focused functions such as:

- `load_dataset`
- `profile_dataset`
- `analyze_dataset`
- `clean_dataset`
- `save_dataset`

These tools are intentionally narrow and composable so the agent can keep using them in different sequences depending on the dataset and analysis task.

## Local setup

Requirements:

- Python 3.11+
- pip

Install the project dependencies:

```bash
python -m pip install -U pip
python -m pip install "mcp>=1.0.0,<2.0.0" pandas pytest
```

Or install from the project metadata if you want to use the package manifest:

```bash
python -m pip install -e .
```

## Run the MCP server

From the project root:

```bash
python -m mcp_server.server
```

The VS Code config in `.vscode/mcp.json` is also configured to launch the server with the same command.

## Testing

The current automated checks live under `tests/` and cover the basic tool behavior:

```bash
python -m pytest tests/test_tools.py
```

At the moment, the project includes targeted checks for:

- dataset format detection
- dataframe profiling
- cleaning behavior
- save/load round-trip
- summary analysis generation

## Notes

- The project intentionally keeps `tests/` separate from `eval/` so one is used for executable verification and the other is used for scenario-driven evaluation design.
- The MCP server is designed to be a tool layer, not the place where orchestration strategy lives.
- The orchestrator and prompt files are expected to coordinate when to invoke each tool, while the MCP server simply performs the action reliably.

## Next phase

The next logical milestone is to wire the orchestrator to the MCP tool server and define the exact prompts and task sequencing used by the agents for dataset ingestion, cleaning, and analysis.
