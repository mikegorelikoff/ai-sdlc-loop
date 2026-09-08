# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared check result; evidence supports the reported result. | validation.log:5 |

| Check | Expected | Actual | Status | Evidence |
| --- | --- | --- | --- | --- |
| pytest tests/payments | All assertions pass | 12 passed | PASS | validation.log:5 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Validate verification command with its owning workflow | validation.log:5 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | validation.log:5 |

| Check | Expected | Actual | Status | Evidence |
| --- | --- | --- | --- | --- |
| pytest tests/payments | All assertions pass | 12 passed | PASS | validation.log:5 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Validate verification command with its owning workflow | validation.log:5 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Verification command is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Verification command | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Verification command | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide verification command |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Provide verification command | Validated verification command |
