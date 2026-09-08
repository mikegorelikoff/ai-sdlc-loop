| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Partial result: second case is unverified; do not infer full coverage. | spec.toon |

| Requirement ID | Bounded behavior | Allowed path | Acceptance | Evidence |
| --- | --- | --- | --- | --- |
| AC-001 | Idempotent retry | src/payments.py | One charge per key | spec.toon |
| AC-001 | Idempotent retry | src/payments.py | One charge per key [pending case] | spec.toon |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate allowed scope with its owning workflow | spec.toon |
