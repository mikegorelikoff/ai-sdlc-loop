# Validate

## Entry

Specification state operation (init, fetch, publish, rotate, refresh-index, or cleanup) has completed.

## Procedure

Verify that all published artifacts adhere to naming conventions (`YYYYMMDD-<name>-spec.md`, etc.), frontmatter contains valid schemas, git sync completed cleanly or degraded fail-open safely, and no unauthorized file deletions occurred.

Quality gate:
- Pass when storage is synchronized, index freshness is within policy, and required artifacts follow naming and metadata conventions.
- Fail when `.sdlc.toon` is invalid, storage Git connection is unreachable without fallback, or published artifacts escape the designated repository directory.

## Exit

Evidence accurately reflects valid specification state and satisfies configured policy.
