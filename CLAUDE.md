# Agent Instructions

This project follows [Punt Labs standards](https://github.com/punt-labs/punt-kit).

## No "Pre-existing" Excuse

There is no such thing as a "pre-existing" issue. If you see a problem — in code you wrote, code a reviewer flagged, or code you happen to be reading — you fix it. Do not classify issues as "pre-existing" to justify ignoring them. Do not suggest that something is "outside the scope of this change." If it is broken and you can see it, it is your problem now.

## Scratch Files

Use `.tmp/` at the project root for scratch and temporary files — never `/tmp`. The `TMPDIR` environment variable is set via `.envrc` so that `tempfile` and subprocesses automatically use it. Contents are gitignored; only `.gitkeep` is tracked.

## Quality Gates

Run before every commit. Zero violations, zero errors, all tests green.

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src/ tests/
uv run pyright src/ tests/
uv run pytest
```

## Documentation Discipline

### CHANGELOG

Entries are written **in the PR branch, before merge** — not retroactively on main. The entry is part of the diff that gets reviewed. If a PR changes user-facing behavior and the diff does not include a CHANGELOG entry, the PR is not ready to merge. Follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format. Add entries under `## [Unreleased]`. Categories: Added, Changed, Deprecated, Removed, Fixed, Security.

### README

Update `README.md` when user-facing behavior changes — new flags, commands, defaults, or config. If the PR introduces something a user would need to know about and the README doesn't reflect it, the PR is not ready to merge.

### PR/FAQ

Update `prfaq.tex` when the change shifts product direction or validates/invalidates a risk assumption. Not every PR needs this — only those that move the product thesis forward or expose new information about feasibility, adoption, or scope.

## Pre-PR Checklist

- [ ] **CHANGELOG entry** included in the PR diff (see above)
- [ ] **README updated** if user-facing behavior changed (see above)
- [ ] **prfaq.tex updated** if product direction shifted (see above)
- [ ] **Quality gates pass**

## Code Review Flow

Do **not** merge immediately after creating a PR. Expect **2–6 review cycles** before merging.

1. **Create PR** — push branch, open PR via `mcp__github__create_pull_request`. Prefer MCP GitHub tools over `gh` CLI.
2. **Request Copilot review** — use `mcp__github__request_copilot_review`.
3. **Watch for feedback in the background** — `gh pr checks <number> --watch` in a background task or separate session. Do not stop waiting. Copilot and Bugbot may take 1–3 minutes after CI completes.
4. **Read all feedback** via MCP: `mcp__github__pull_request_read` with `get_reviews` and `get_review_comments`.
5. **Take every comment seriously.** There is no such thing as "pre-existing" or "unrelated to this change" — if you can see it, you own it. If you disagree, explain why in a reply.
6. **Fix and re-push** — commit fixes, push, re-run quality gates. Each fix triggers a new review cycle.
7. **Repeat steps 3–6** until the latest review is **uneventful** — zero new comments, all checks green.
8. **Merge only when the last review was clean** — use `mcp__github__merge_pull_request` (not `gh pr merge`).

## Issue Tracking

This project uses **beads** (`bd`) for issue tracking. If an issue discovered here affects multiple repos or requires a standards change, escalate to a [punt-kit bead](https://github.com/punt-labs/punt-kit) instead (see [bead placement scheme](../CLAUDE.md#where-to-create-a-bead)).

## Ethos & Delegation

Identity: `agent: claude` per `.punt-labs/ethos.yaml`. Sub-agent calls (`Agent(subagent_type=…)`) match ethos identity handles.

langlearn is the orchestrator: it composes the typed protocols from `langlearn-types` with the provider-side implementations (`langlearn-tts`, `langlearn-imagegen`, `langlearn-anki`). Most code is Python; the surface is CLI + MCP. Within each row, the worker and evaluator must be distinct handles. Claude is the leader, never the evaluator.

| Task type | Worker | Evaluator |
|-----------|--------|-----------|
| Python orchestration logic | `rmh` (Hettinger) | `gvr` (van Rossum) — language-design view |
| Protocol / contract evolution | `gvr` | `rmh` |
| CLI surface | `mdm` (McIlroy) | `rop` (Pike) |
| MCP server tool definitions | `rmh` | `mdm` |
| Cross-repo integration with langlearn-types | `rmh` | `gvr` — protocol stability |
| Provider selection / routing | `rmh` | `mdm` |
| Security — API keys, env-var resolution | `rmh` | `djb` (Bernstein) |
| Infra / CI / release | `adb` (Lovelace) | `kth` (Hightower) |
| Pedagogy / learner outcomes | `claude` (leader) | `mcg` (Cagan) — outcome-driven product |
| User research with language learners | `claude` (leader) | `tdt` (Torres) — continuous discovery |

Use the `standard` pipeline for features, `coverage` for test gaps, `coe` for recurring failures across providers.

## Standards References

- [Python](https://github.com/punt-labs/punt-kit/blob/main/standards/python.md)
- [GitHub](https://github.com/punt-labs/punt-kit/blob/main/standards/github.md)
- [Workflow](https://github.com/punt-labs/punt-kit/blob/main/standards/workflow.md)
- [CLI](https://github.com/punt-labs/punt-kit/blob/main/standards/cli.md)
- [Shell](https://github.com/punt-labs/punt-kit/blob/main/standards/shell.md)
