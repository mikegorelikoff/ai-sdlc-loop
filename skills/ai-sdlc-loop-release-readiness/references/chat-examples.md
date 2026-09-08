# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared release gate result; evidence supports the reported result. | ci.log:7 |

| Release gate | Candidate commit | Status | Evidence | Required action |
| --- | --- | --- | --- | --- |
| CI | abc1234 | PASS | ci.log:7 | None |

| Residual risk | Owner | Mitigation | Evidence |
| --- | --- | --- | --- |
| Recorded in retry decision DEC-001 | Product owner | Recorded in retry decision DEC-001 | ci.log:7 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | None | ci.log:7 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | ci.log:7 |

| Release gate | Candidate commit | Status | Evidence | Required action |
| --- | --- | --- | --- | --- |
| CI | abc1234 | PASS | ci.log:7 | None |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | None | ci.log:7 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Candidate commit is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Candidate commit | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Candidate commit | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide candidate commit |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide candidate commit | Validated candidate commit |
