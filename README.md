# langlearn

Orchestrator for LangLearn workflows (evaluation gates + backends).

## Install

```bash
uv tool install punt-langlearn
```

## CLI

```bash
langlearn --help
langlearn --json version
langlearn doctor
langlearn serve
```

## MCP

```bash
langlearn install
langlearn serve
```

## Development

```bash
uv sync --all-extras
uv run ruff check .
uv run ruff format --check .
uv run mypy src/ tests/
uv run pyright src/ tests/
uv run pytest
```
