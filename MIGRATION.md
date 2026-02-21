# Legacy Port Plan (from ~/Coding/langlearn-anki)

Date: 2026-02-21

## Goal
Port the full functionality of the legacy app in `~/Coding/langlearn-anki` into the new multi-repo architecture (`langlearn`, `langlearn-anki`, `langlearn-imagegen`, `langlearn-tts`, `langlearn-types`) with a clear map of what goes where and a sequenced implementation plan.

## Legacy Architecture Summary
- CLI entry point: `src/langlearn/main.py` (language/deck/output/image-api/ai-provider/cultural-style flags).
- Pipeline: `DeckBuilderAPI` with phases: INITIALIZED → DATA_LOADED → MEDIA_ENRICHED → CARDS_BUILT → DECK_EXPORTED.
- Language implementations: German, Russian, Korean (`src/langlearn/languages/*`).
- Data assets: CSVs per language/deck under `languages/<language>/<deck>/`.
- Media: Audio via AWS Polly; Images via Pexels and OpenAI (GPT Image), plus two-stage AI evaluation and cultural styles.
- Templates: HTML/CSS card templates per language and card type.
- Anki export: `AnkiBackend` + managers (media/deck) and note type mappings.

## Feature Matrix (Legacy → Target)

| Feature | Legacy Source | Target Repo(s) | Notes |
| --- | --- | --- | --- |
| CLI deck generation (language/deck/output/image-api/ai-provider/cultural-style) | `src/langlearn/main.py` | `langlearn` | New CLI should orchestrate and call subcomponents.
| Pipeline phases + progress summary | `core/deck/builder.py`, `phases.py`, `progress.py` | `langlearn` | Orchestrator should expose phase transitions and stats.
| Language registry + implementations | `languages/registry.py`, `languages/*` | `langlearn` | Includes language code/name, TTS config, record mappings, templates.
| CSV record schemas + factories | `languages/*/records`, `core/records` | `langlearn` | Record validation, per-language mapping from CSV file → record type.
| Card builders + processors | `languages/*/services/card_builder.py`, `card_processor.py` | `langlearn` | Build card data (fields) from records + templates.
| Anki note type mappings | `languages/*/language.py` (note type mappings) | `langlearn-anki` | Map note type → record type; align with templates.
| Card HTML/CSS templates | `languages/*/templates`, `docs/UX-CARD-DESIGN.md` | `langlearn-anki` (or `langlearn`) | Decision needed on template ownership; likely `langlearn-anki`.
| Deck export (.apkg) | `infrastructure/backends/anki_backend.py` | `langlearn-anki` | Export + media packaging.
| Media generation orchestration | `MediaService`, `MediaManager`, `MediaEnricher` | `langlearn` | Should call `langlearn-tts` + `langlearn-imagegen` with policies.
| Audio generation (AWS Polly) | `infrastructure/services/audio_service.py` | `langlearn-tts` | Voices per language: German Marlene, Russian Tatyana, Korean Seoyeon.
| Image search (Pexels) | `infrastructure/services/image_service.py` | `langlearn-imagegen` | Should support cultural context keywords.
| AI image gen (OpenAI GPT Image) | `gpt_image_service.py` | `langlearn-imagegen` | Support size/quality + metadata; align with legacy `--image-api gpt-image` + `two-stage-gpt-image`.
| Two-stage AI image generation | `TwoStageDALLEService`, `best_of_image_search` | `langlearn` + `langlearn-imagegen` | Needs evaluation gates + fallback logic.
| Image evaluation scoring | `AIImageEvaluator` | `langlearn` | 0.0–1.0 scoring with threshold.
| Prompt template engine | `prompt_template_engine.py`, `prompts/` | `langlearn` | Centralized Jinja templates, cultural styles.
| Cultural styles | `prompts/cultural/*.j2` | `langlearn` | `--cultural-style` should pick templates.
| Data assets | `languages/<language>/<deck>` | `langlearn` | Decide if we keep in repo or move to a data repo.
| Logging & diagnostics | `logs/*.log`, CLI printouts | `langlearn` | Keep basic observability.

## Open Questions
- Template ownership: keep templates in `langlearn-anki` (Anki-specific) or in `langlearn` (language-owned)?
- Data assets location: keep in `langlearn` or create a dedicated `langlearn-data` repo?
- Evaluation provider: Anthropic vs OpenAI for image evaluation gates.
- Stable diffusion: legacy mentions it, but we will **not** port it unless scope changes.

## Implementation Sequence (High-Level)
1. Port core contracts and language/record schemas (`langlearn-types`, `langlearn`).
2. Port media providers (`langlearn-tts`, `langlearn-imagegen`).
3. Port templates + Anki export (`langlearn-anki`).
4. Build orchestrator pipeline + CLI (`langlearn`).
5. Add evaluation policies + two-stage image generation (`langlearn`).
6. Validate against legacy decks (German A1/A1.1/default + Russian/Korean basic).
