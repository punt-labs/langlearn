# Changelog

## [Unreleased]

### Changed

- Migrate from `mcp` (>=1.28.1,<2) to `fastmcp` (>=2,<3). FastMCP was
  extracted from the mcp SDK into its own package as part of mcp 2.0 —
  `mcp.server.fastmcp` no longer exists in the 2.x line. The only change
  needed is the import site: `from mcp.server.fastmcp import FastMCP` →
  `from fastmcp import FastMCP`. All 84 tests pass. Supersedes Dependabot
  PR #70 which was trying to bump `mcp` to 2.0 but would have failed at
  import.

- Initial scaffolding for langlearn.
- Added ROADMAP.md and refreshed README/DESIGN/MIGRATION documentation.
