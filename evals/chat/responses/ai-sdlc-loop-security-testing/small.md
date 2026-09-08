| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | One severity result; scope and evidence are explicit. | handler.py:42 |

| Trust boundary | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Trust boundary | BLOCKED | Unresolved behavior prevents the next stage | handler.py:42 | Resolve the primary finding before handoff |

| Severity | Trust boundary | Finding | Evidence | Remediation |
| --- | --- | --- | --- | --- |
| HIGH | Tenant lookup | Ownership check absent | handler.py:42 | Constrain lookup to tenant |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Validate trust boundary with its owning workflow | handler.py:42 |
