| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | 20 severity records; 20 blockers; 8 shown; inspect the linked full artifact. | handler.py:42 |

| Trust boundary | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Trust boundary | BLOCKED | Unresolved behavior prevents the next stage | handler.py:42 | Resolve the primary finding before handoff |

| Severity | Trust boundary | Finding | Evidence | Remediation |
| --- | --- | --- | --- | --- |
| HIGH | Tenant lookup | Ownership check absent (case 1) | handler.py:42 #1 | Constrain lookup to tenant |
| HIGH | Tenant lookup | Ownership check absent (case 2) | handler.py:42 #2 | Constrain lookup to tenant |
| HIGH | Tenant lookup | Ownership check absent (case 3) | handler.py:42 #3 | Constrain lookup to tenant |
| HIGH | Tenant lookup | Ownership check absent (case 4) | handler.py:42 #4 | Constrain lookup to tenant |
| HIGH | Tenant lookup | Ownership check absent (case 5) | handler.py:42 #5 | Constrain lookup to tenant |
| HIGH | Tenant lookup | Ownership check absent (case 6) | handler.py:42 #6 | Constrain lookup to tenant |
| HIGH | Tenant lookup | Ownership check absent (case 7) | handler.py:42 #7 | Constrain lookup to tenant |
| HIGH | Tenant lookup | Ownership check absent (case 8) | handler.py:42 #8 | Constrain lookup to tenant |

| Shown | Total | Full evidence |
| --- | --- | --- |
| 8 | 20 | full-result.toon |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Validate trust boundary with its owning workflow | handler.py:42 |
