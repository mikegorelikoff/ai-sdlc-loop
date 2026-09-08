# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared test id result; evidence supports the reported result. | test-cases.md:12 |

| Test ID | Requirement ID | Setup / trigger | Expected result | Layer | Evidence |
| --- | --- | --- | --- | --- | --- |
| TC-001 | AC-001 | Existing key; repeat callback | Original charge returned | Service | test-cases.md:12 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Validate acceptance criterion with its owning workflow | test-cases.md:12 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | test-cases.md:12 |

| Test ID | Requirement ID | Setup / trigger | Expected result | Layer | Evidence |
| --- | --- | --- | --- | --- | --- |
| TC-001 | AC-001 | Existing key; repeat callback | Original charge returned | Service | test-cases.md:12 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Validate acceptance criterion with its owning workflow | test-cases.md:12 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Acceptance criterion is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Acceptance criterion | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Acceptance criterion | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide acceptance criterion |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Provide acceptance criterion | Validated acceptance criterion |
