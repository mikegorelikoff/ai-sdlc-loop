| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | 20 requirement id records; 8 shown; inspect the linked full artifact. | spec.toon |

| Requirement ID | Bounded behavior | Allowed path | Acceptance | Evidence |
| --- | --- | --- | --- | --- |
| AC-001 | Idempotent retry | src/payments.py | One charge per key #1 | spec.toon |
| AC-001 | Idempotent retry | src/payments.py | One charge per key #2 | spec.toon |
| AC-001 | Idempotent retry | src/payments.py | One charge per key #3 | spec.toon |
| AC-001 | Idempotent retry | src/payments.py | One charge per key #4 | spec.toon |
| AC-001 | Idempotent retry | src/payments.py | One charge per key #5 | spec.toon |
| AC-001 | Idempotent retry | src/payments.py | One charge per key #6 | spec.toon |
| AC-001 | Idempotent retry | src/payments.py | One charge per key #7 | spec.toon |
| AC-001 | Idempotent retry | src/payments.py | One charge per key #8 | spec.toon |

| Shown | Total | Full evidence |
| --- | --- | --- |
| 8 | 20 | full-result.toon |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate allowed scope with its owning workflow | spec.toon |
