| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Partial result: second case is unverified; do not infer full coverage. | handler.py:42 |

| Trust boundary | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Trust boundary | BLOCKED | Unresolved behavior prevents the next stage | handler.py:42 | Resolve the primary finding before handoff |

| Severity | Trust boundary | Finding | Evidence | Remediation |
| --- | --- | --- | --- | --- |
| HIGH | Tenant lookup | Ownership check absent (case 1) | handler.py:42 | Constrain lookup to tenant |
| HIGH | Tenant lookup | Ownership check absent (case 2) | handler.py:42 [pending case] | Constrain lookup to tenant |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Validate trust boundary with its owning workflow | handler.py:42 |
