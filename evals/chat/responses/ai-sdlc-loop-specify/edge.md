| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared bounded behavior / allowed path entities; listed evidence satisfies this skill check. | spec.toon |

| Requirement ID | Bounded behavior | Allowed path | Acceptance | Evidence |
| --- | --- | --- | --- | --- |
| AC-001 &#124; перенос<br>строки | Idempotent retry | src/payments.py | One charge per key | spec.toon |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate allowed scope with its owning workflow | spec.toon |

```toon
schema: fixture/v1
status: pending
source: "literal | value"
```
