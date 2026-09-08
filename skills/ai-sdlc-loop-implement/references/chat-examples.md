# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PENDING | Prepared file / component result; owner decision or execution remains pending. | diff.patch:12 |

| File / component | Change | Requirement ID | Verification | Evidence |
| --- | --- | --- | --- | --- |
| src/payments.py | Reuse charge by key | AC-001 | PENDING | diff.patch:12 |

| Check | Status | Evidence |
| --- | --- | --- |
| Retry test | PASS | diff.patch:12 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate implementation approval with its owning workflow | diff.patch:12 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | diff.patch:12 |

| File / component | Change | Requirement ID | Verification | Evidence |
| --- | --- | --- | --- | --- |
| src/payments.py | Reuse charge by key | AC-001 | PENDING | diff.patch:12 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate implementation approval with its owning workflow | diff.patch:12 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Implementation approval is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Implementation approval | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Implementation approval | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide implementation approval |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide implementation approval | Validated implementation approval |
