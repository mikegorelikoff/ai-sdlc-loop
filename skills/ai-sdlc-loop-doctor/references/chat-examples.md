# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared check result; evidence supports the reported result. | fixture.toon:1 |

| Check | Installed state | Expected state | Status | Remediation |
| --- | --- | --- | --- | --- |
| Runtime import | Available | Available | PASS | None |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Validate installation root with its owning workflow | fixture.toon:1 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | fixture.toon:1 |

| Check | Installed state | Expected state | Status | Remediation |
| --- | --- | --- | --- | --- |
| Runtime import | Available | Available | PASS | None |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Validate installation root with its owning workflow | fixture.toon:1 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Installation root is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Installation root | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Installation root | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide installation root |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Provide installation root | Validated installation root |
