# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared check result; evidence supports the reported result. | evidence.toon |

| Check | Expected | Actual | Status | Evidence |
| --- | --- | --- | --- | --- |
| pytest tests/payments | No duplicate charge | One charge observed | PASS | evidence.toon |

| Artifact | Freshness | Evidence |
| --- | --- | --- |
| Recorded in retry decision DEC-001 | Snapshot supplied for this scenario | evidence.toon |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Validate current quality evidence with its owning workflow | evidence.toon |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | evidence.toon |

| Check | Expected | Actual | Status | Evidence |
| --- | --- | --- | --- | --- |
| pytest tests/payments | No duplicate charge | One charge observed | PASS | evidence.toon |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Validate current quality evidence with its owning workflow | evidence.toon |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Current quality evidence is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Current quality evidence | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Current quality evidence | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide current quality evidence |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Provide current quality evidence | Validated current quality evidence |
