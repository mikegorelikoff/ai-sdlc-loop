| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | One severity result; scope and evidence are explicit. | TC-001 reproduces double charge |

| Review diff | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Review diff | BLOCKED | Unresolved behavior prevents the next stage | TC-001 reproduces double charge | Resolve the primary finding before handoff |

| Severity | Location | Finding | Evidence | Required fix |
| --- | --- | --- | --- | --- |
| HIGH | src/payments.py:84 | Duplicate charge on retry | TC-001 reproduces double charge | Reuse idempotency key |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Reuse idempotency key | TC-001 reproduces double charge |
