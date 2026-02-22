# LangLearn Projects — Standards Audit

Date: 2026-02-21
Audited by: punt-kit standards sweep (session)

## Scope

Four repositories: langlearn, langlearn-anki, langlearn-imagegen, langlearn-types.
Audited against punt-kit standards: python.md, github.md, distribution.md, plugins.md, shell.md.

## Summary

| Category | Status | Details |
|----------|--------|---------|
| Quality gates (ruff, mypy, pyright, pytest) | PASS | All 4 projects have full config |
| CI workflows (lint, test, docs) | PASS | All present with SHA-pinned actions |
| Markdownlint config | PASS | Both config files present in all 4 |
| CLAUDE.md | PASS | All 4 have standard quality gates |
| CHANGELOG.md | PASS | All 4 present |
| .beads/ | PASS | Initialized in all 4 (0 open issues) |
| README.md | PASS | Install, CLI, MCP, Development sections |
| release.yml | MISSING | None of the 4 have a release workflow |
| install.sh | MISSING | None of the 4 have an install script |
| .biff | MISSING | None of the 4 have team communication config |
| .claude-plugin/plugin.json | N/A | These are CLI+MCP tools, not plugins |

## Issues Found

### P1 — Fix Before Shipping

**1. No release workflow (all 4)**
None of the langlearn projects have release.yml. Per distribution.md, every PyPI
package needs a GitHub Actions release workflow that publishes to TestPyPI and PyPI
on tag push. Use the punt-kit template (same as biff/quarry/langlearn-tts).

**2. No install.sh (all 4)**
Per distribution.md, every user-facing project needs a POSIX sh install script as
the primary install path. Each should follow the established pattern:

- Check Python 3.13+
- Check/install uv
- `uv tool install --force <package>@git+https://github.com/punt-labs/<repo>.git`
  (git URL workaround until PyPI org prefix approved)
- Run `<binary> install` if applicable
- Run `<binary> doctor` if applicable

Note: langlearn-types may not need its own install script if it's only consumed as a
library dependency (not installed standalone). Evaluate whether the CLI/server surface
in langlearn-types is intentional or scaffolding.

### P2 — Should Fix

**3. setup-uv action SHA inconsistency (langlearn-anki)**
langlearn-anki pins `astral-sh/setup-uv` to `d4b2f3b6ecc6e67c4457f6d3e41ec42d3d0fcb86`
(v5.4.2). The other three projects pin to `eac588ad8def6316056a12d4907a9d4d84ff7a3b`
(v7.3.0). All should use the same version.

**4. langlearn CI missing dependency clones**
langlearn has path dependencies on langlearn-types, langlearn-anki, langlearn-imagegen,
and langlearn-tts in `[tool.uv.sources]`. Its CI workflows do NOT clone these sibling
repos before `uv sync`. langlearn-anki correctly clones langlearn-types. Either:

- langlearn CI is broken and nobody has noticed (because tests are smoke-only), or
- uv resolves path deps from PyPI fallback when the path doesn't exist

This needs investigation. If CI passes without clones, the path deps are unused at
install time and only affect local development. If CI would fail, it's latent breakage.

**5. .biff missing (all 4)**
Per org rollout, all active projects should have a `.biff` config file:

```toml
[team]
members = ["jmf-pobox"]

[relay]
url = "tls://connect.ngs.global"
```

### P3 — Observations

**6. langlearn-types has CLI/MCP surface**
For a types-and-protocols library, langlearn-types declares CLI (`langlearn-types`)
and MCP server (`langlearn-types-server`) entry points, plus `typer`, `rich`, `mcp`
as runtime dependencies. If this is intentional (e.g., the types package also serves
as a shared MCP tool registry), document why. If it's scaffolding from project
generation, consider removing to keep the types package dependency-light.

**7. Test coverage is thin**
langlearn-imagegen and langlearn-types have 1 test file each (smoke tests only).
langlearn has 2 test files. Only langlearn-anki has meaningful test coverage (5 files).
This is expected for v0.1.0 projects but should be tracked as they mature.

**8. Dev deps use optional-dependencies, not dependency-groups**
All 4 use `[project.optional-dependencies] dev = [...]`. The punt-kit standard
(python.md) recommends `[dependency-groups]` for dev dependencies. Both work with
`uv sync --all-extras`, but dependency-groups is the newer pattern. Low priority.

## Per-Project Beads to Create

### langlearn

- Add release.yml workflow
- Add install.sh (POSIX sh, git URL)
- Add .biff config
- Investigate CI path dependency resolution

### langlearn-anki

- Add release.yml workflow
- Add install.sh (POSIX sh, git URL)
- Add .biff config
- Pin setup-uv to v7.3.0 (match other projects)

### langlearn-imagegen

- Add release.yml workflow
- Add install.sh (POSIX sh, git URL)
- Add .biff config

### langlearn-types

- Add release.yml workflow
- Add .biff config
- Evaluate CLI/MCP surface — keep or remove?
- (install.sh only if CLI surface is kept)
