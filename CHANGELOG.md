# Changelog

## [Unreleased]

### Changed

- Migrate MCP server from the `mcp` package to `fastmcp`. FastMCP was
  extracted into its own package as part of mcp 2.0; `mcp.server.fastmcp`
  no longer exists in the 2.x line.

### Fixed

- Action pin comments now state the version actually pinned. The SHA is
  the security control, but the comment is the only part a human reads,
  so a wrong one hides a stale pin from every review — how
  `gh-action-pypi-publish` broke punt-kit's 0.12.0 release. Labels
  resolved against the GitHub API. `actions/checkout` was labelled `# v4`
  on v7.0.1's SHA, and `astral-sh/setup-uv` carried `# v10.0.0` in one
  workflow and `# v5` in another for the same SHA.
- `markdownlint-cli2-action` is repinned from an unreleased commit on the
  action's default branch — ahead of every tag including v24.2.0 — to the
  v24.2.0 release commit. This is the one SHA change: the pin now names an
  immutable released artifact rather than a moving branch head. It is not
  a version jump; the workflow was already running code past v24.2.0 while
  the comment claimed v22.

- Initial scaffolding for langlearn.
- Added ROADMAP.md and refreshed README/DESIGN/MIGRATION documentation.
