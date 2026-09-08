| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | spec.toon |

| Requirement ID | Bounded behavior | Allowed path | Acceptance | Evidence |
| --- | --- | --- | --- | --- |
| AC-001 | Idempotent retry | src/payments.py | One charge per key | spec.toon |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate allowed scope with its owning workflow | spec.toon |
