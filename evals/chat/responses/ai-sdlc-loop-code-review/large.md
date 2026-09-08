| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | 20 severity records; 20 blockers; 8 shown; inspect the linked full artifact. | TC-001 reproduces double charge |

| Review diff | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Review diff | BLOCKED | Unresolved behavior prevents the next stage | TC-001 reproduces double charge | Resolve the primary finding before handoff |

| Severity | Location | Finding | Evidence | Required fix |
| --- | --- | --- | --- | --- |
| HIGH | src/payments.py:84 | Duplicate charge on retry (case 1) | TC-001 reproduces double charge #1 | Reuse idempotency key |
| HIGH | src/payments.py:84 | Duplicate charge on retry (case 2) | TC-001 reproduces double charge #2 | Reuse idempotency key |
| HIGH | src/payments.py:84 | Duplicate charge on retry (case 3) | TC-001 reproduces double charge #3 | Reuse idempotency key |
| HIGH | src/payments.py:84 | Duplicate charge on retry (case 4) | TC-001 reproduces double charge #4 | Reuse idempotency key |
| HIGH | src/payments.py:84 | Duplicate charge on retry (case 5) | TC-001 reproduces double charge #5 | Reuse idempotency key |
| HIGH | src/payments.py:84 | Duplicate charge on retry (case 6) | TC-001 reproduces double charge #6 | Reuse idempotency key |
| HIGH | src/payments.py:84 | Duplicate charge on retry (case 7) | TC-001 reproduces double charge #7 | Reuse idempotency key |
| HIGH | src/payments.py:84 | Duplicate charge on retry (case 8) | TC-001 reproduces double charge #8 | Reuse idempotency key |

| Shown | Total | Full evidence |
| --- | --- | --- |
| 8 | 20 | full-result.toon |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Reuse idempotency key | TC-001 reproduces double charge |
