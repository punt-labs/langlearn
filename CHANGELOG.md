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
  resolved against the GitHub API, and no SHA was changed.

- Initial scaffolding for langlearn.
- Added ROADMAP.md and refreshed README/DESIGN/MIGRATION documentation.
