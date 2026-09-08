# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared runtime check result; evidence supports the reported result. | smoke.log:4 |

| Runtime check | Expected | Actual | Status | Evidence |
| --- | --- | --- | --- | --- |
| Installed helper import | Imports sibling runtime | Import succeeds | PASS | smoke.log:4 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Validate installed helper with its owning workflow | smoke.log:4 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | smoke.log:4 |

| Runtime check | Expected | Actual | Status | Evidence |
| --- | --- | --- | --- | --- |
| Installed helper import | Imports sibling runtime | Import succeeds | PASS | smoke.log:4 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Validate installed helper with its owning workflow | smoke.log:4 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Installed helper is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Installed helper | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Installed helper | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide installed helper |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Provide installed helper | Validated installed helper |
