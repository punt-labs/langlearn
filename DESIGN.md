# Design Decision Log

## 0001 — Initial split into tri-modal packages (SETTLED)

- Orchestrator owns evaluation gates for prompts, images, audio, and cards.
- Backends are optional, one-way integrations via langlearn-types protocols.
- All outputs are evaluated before proceeding to the next workflow step.

## 0002 — Multi-repo tri-modal architecture plan (SETTLED)

- Scope: multi-repo layout with `langlearn`, `langlearn-types`, `langlearn-imagegen`, `langlearn-anki`, and `langlearn-tts` as sibling directories.
- `langlearn-types` holds shared contracts only (protocols + dataclasses) and has no runtime dependencies.
- `langlearn-imagegen` is a dumb executor: accepts prompt + optional evaluator and returns `ImageResult`; no prompt logic and no evaluation logic inside the package.
- `langlearn-anki` performs card generation and export only; it consumes provided media assets and never generates media.
- `langlearn-tts` remains tri-modal and aligns request/response types to `langlearn-types`.
- `langlearn` is the orchestrator; it owns prompts, styles, and evaluation policies and wires imagegen + tts + anki together.
- Evaluation is centralized in the orchestrator for image, audio, and deck outputs.
- Default development transport is the library interface; CLI and MCP remain supported for parity and orchestration.
- Cross-repo dependencies are recorded in issue descriptions as `Cross-repo deps: <repo>: <issue-id>[, ...]`.
- Phase 0: ensure repos exist with minimal scaffolding and baseline docs.
- Phase 1: define `langlearn-types` contracts (requests, results, provider protocols).
- Phase 2: extract image providers into `langlearn-imagegen` and expose tri-modal surfaces.
- Phase 3: extract ankigen into `langlearn-anki` and remove media generation.
- Phase 4: build the orchestrator pipeline that wires imagegen + tts + anki.
- Phase 5: add test tiers, docs, and CI alignment across all repos.

## 0003 — Templates live with the Anki backend (SETTLED)

- HTML/CSS templates are owned and shipped by `langlearn-anki`.
- The orchestrator supplies fields and media references only.
