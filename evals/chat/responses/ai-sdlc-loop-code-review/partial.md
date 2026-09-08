| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Partial result: second case is unverified; do not infer full coverage. | TC-001 reproduces double charge |

| Review diff | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Review diff | BLOCKED | Unresolved behavior prevents the next stage | TC-001 reproduces double charge | Resolve the primary finding before handoff |

| Severity | Location | Finding | Evidence | Required fix |
| --- | --- | --- | --- | --- |
| HIGH | src/payments.py:84 | Duplicate charge on retry (case 1) | TC-001 reproduces double charge | Reuse idempotency key |
| HIGH | src/payments.py:84 | Duplicate charge on retry (case 2) | TC-001 reproduces double charge [pending case] | Reuse idempotency key |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Reuse idempotency key | TC-001 reproduces double charge |
