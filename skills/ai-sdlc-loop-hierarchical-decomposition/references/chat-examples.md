# Compact chat examples

These simulated examples exercise the compact contract. The full domain report is rendered by `decompose.py render`.

## Happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Source-backed branch evaluated; execution approval remains separate | decomposition.toon |

| ID | Type | Parent | Title | Outcome | Status |
| --- | --- | --- | --- | --- | --- |
| STORY-example | STORY | EPIC-example | Verify email | Email becomes verified | PASS |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Delivery owner | Hand off reviewed Story | decomposition.toon |


## Warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Source-backed branch evaluated; execution approval remains separate | decomposition.toon |

| ID | Type | Parent | Title | Outcome | Status |
| --- | --- | --- | --- | --- | --- |
| STORY-example | STORY | EPIC-example | Verify email | Email becomes verified | WARNING |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Delivery owner | Hand off reviewed Story | decomposition.toon |


## Blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Resolve identity model before decomposition | decomposition.toon |

| Branch | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| EPIC-example | BLOCKED | Identity model unknown | decomposition.toon | Provide owner decision |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Delivery owner | Resolve missing identity decision | decomposition.toon |
