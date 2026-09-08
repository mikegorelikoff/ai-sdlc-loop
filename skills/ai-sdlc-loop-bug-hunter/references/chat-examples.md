# Chat examples

Authored structural simulations; native candidate gates are exercised separately.

## Happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared check result; evidence supports the reported result. | fixture.toon:1 |

| ID | Severity | Location | Bug | Evidence | Decision status |
| --- | --- | --- | --- | --- | --- |
| HUNT-1 | HIGH | app.py:1 | Incorrect boundary | TC-01 | SUPPORTED |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Validate source anchors and candidate review | fixture.toon:1 |

## Warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | fixture.toon:1 |

| ID | Severity | Location | Bug | Evidence | Decision status |
| --- | --- | --- | --- | --- | --- |
| HUNT-1 | HIGH | app.py:1 | Incorrect boundary | TC-01 | SUPPORTED |

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
