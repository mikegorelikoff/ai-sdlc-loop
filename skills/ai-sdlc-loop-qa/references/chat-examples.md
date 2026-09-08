# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PENDING | Prepared scenario id result; owner decision or execution remains pending. | qa.md:20 |

| Scenario ID | Actor / setup | Action | Expected result | Execution status | Evidence |
| --- | --- | --- | --- | --- | --- |
| QA-001 | Operator with failed callback | Replay callback | One ledger entry | PENDING | qa.md:20 |

| Regression target | Risk | Execution status | Evidence |
| --- | --- | --- | --- |
| Existing successful charge | Retry change could duplicate a charge | PENDING | qa.md:20 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Replay callback | qa.md:20 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | qa.md:20 |

| Scenario ID | Actor / setup | Action | Expected result | Execution status | Evidence |
| --- | --- | --- | --- | --- | --- |
| QA-001 | Operator with failed callback | Replay callback | One ledger entry | PENDING | qa.md:20 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Replay callback | qa.md:20 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Acceptance outcome is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Acceptance outcome | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Acceptance outcome | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide acceptance outcome |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Provide acceptance outcome | Validated acceptance outcome |
