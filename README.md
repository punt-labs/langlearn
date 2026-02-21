# langlearn

Orchestrator for LangLearn workflows (evaluation gates + backends).

## Status (2026-02-21)

- CLI and MCP surfaces are scaffolding only (version, doctor, serve).
- Language registry and language scaffolding exist, but pipelines are not wired end-to-end.
- Orchestration flow, prompt engine, and media enrichment are still being ported.

## Roadmap

See ROADMAP.md.

## Migration

See MIGRATION.md for the legacy port plan and feature mapping.

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
