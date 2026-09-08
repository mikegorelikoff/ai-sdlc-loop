# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PENDING | Prepared option id result; owner decision or execution remains pending. | fixture.toon:1 |

| Option ID | Business option | Precedent | Trade-off | Decision status |
| --- | --- | --- | --- | --- |
| OPT-001 | Reuse payment ledger | DEC-001 | Lower effort; existing retention | Proposed |

| Question ID | Question | Owner | Evidence method | Decision impact |
| --- | --- | --- | --- | --- |
| Q-001 | What retry window must be supported? | Product owner | Read provider retention contract | Determines idempotency key retention |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Validate raw request with its owning workflow | fixture.toon:1 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | fixture.toon:1 |

| Option ID | Business option | Precedent | Trade-off | Decision status |
| --- | --- | --- | --- | --- |
| OPT-001 | Reuse payment ledger | DEC-001 | Lower effort; existing retention | Proposed |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Validate raw request with its owning workflow | fixture.toon:1 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Raw request is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Raw request | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Raw request | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide raw request |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Provide raw request | Validated raw request |
