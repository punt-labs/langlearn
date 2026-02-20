# Design Decision Log

## 0001 — Initial split into tri-modal packages (SETTLED)
- Orchestrator owns evaluation gates for prompts, images, audio, and cards.
- Backends are optional, one-way integrations via langlearn-types protocols.
- All outputs are evaluated before proceeding to the next workflow step.
