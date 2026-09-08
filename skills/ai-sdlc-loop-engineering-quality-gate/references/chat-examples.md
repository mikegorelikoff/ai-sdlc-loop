# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared severity result; evidence supports the reported result. | TC-001 |

| Severity | Location | Finding | Disposition | Verification | Evidence |
| --- | --- | --- | --- | --- | --- |
| HIGH | src/payments.py:84 | Duplicate callback creates charge | Fixed locally | PASS | TC-001 |

| Gate | Status | Unresolved count | Evidence |
| --- | --- | --- | --- |
| Retry acceptance | PASS | 0 | TC-001 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate implementation diff with its owning workflow | TC-001 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | TC-001 |

| Severity | Location | Finding | Disposition | Verification | Evidence |
| --- | --- | --- | --- | --- | --- |
| HIGH | src/payments.py:84 | Duplicate callback creates charge | Fixed locally | PASS | TC-001 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate implementation diff with its owning workflow | TC-001 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Implementation diff is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Implementation diff | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Implementation diff | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide implementation diff |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide implementation diff | Validated implementation diff |
