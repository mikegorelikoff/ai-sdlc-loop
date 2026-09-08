# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review complete; resolve the reported blocker before delivery. | TC-001 reproduces double charge |

| Review diff | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Review diff | BLOCKED | Unresolved behavior prevents the next stage | TC-001 reproduces double charge | Resolve the primary finding before handoff |

| Severity | Location | Finding | Evidence | Required fix |
| --- | --- | --- | --- | --- |
| HIGH | src/payments.py:84 | Duplicate charge on retry | TC-001 reproduces double charge | Reuse idempotency key |

| Check | Status | Evidence | Coverage gap |
| --- | --- | --- | --- |
| Retry test | PASS | TC-001 reproduces double charge | No gap in the bounded reviewed case |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Reuse idempotency key | TC-001 reproduces double charge |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review complete with a blocking finding and a source-freshness warning. | TC-001 reproduces double charge |

| Review diff | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Review diff | BLOCKED | Unresolved behavior prevents the next stage | TC-001 reproduces double charge | Resolve the primary finding before handoff |

| Severity | Location | Finding | Evidence | Required fix |
| --- | --- | --- | --- | --- |
| HIGH | src/payments.py:84 | Duplicate charge on retry | TC-001 reproduces double charge | Reuse idempotency key |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Reuse idempotency key | TC-001 reproduces double charge |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review diff is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Review diff | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Review diff | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide review diff |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide review diff | Validated review diff |
