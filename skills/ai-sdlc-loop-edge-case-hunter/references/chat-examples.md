# Chat examples

Authored structural simulations; native candidate gates are exercised separately.

## Happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared check result; evidence supports the reported result. | fixture.toon:1 |

| ID | Edge case | Dimension | Impact | Expected behavior | Test mapping |
| --- | --- | --- | --- | --- | --- |
| HUNT-1 | Boundary hypothesis | INPUT | Source-backed impact | Expected behavior | PROPOSED |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Validate source anchors and candidate review | fixture.toon:1 |

## Warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | fixture.toon:1 |

| ID | Edge case | Dimension | Impact | Expected behavior | Test mapping |
| --- | --- | --- | --- | --- | --- |
| HUNT-1 | Boundary hypothesis | INPUT | Source-backed impact | Expected behavior | PROPOSED |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Validate source anchors and candidate review | fixture.toon:1 |

## Blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Source inventory is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Analysis scope | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Target behavior | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide source inventory |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Provide source inventory | Validated source inventory |
