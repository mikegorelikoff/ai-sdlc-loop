| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review complete with a blocking finding and a source-freshness warning. | handler.py:42 |

| Trust boundary | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Trust boundary | BLOCKED | Unresolved behavior prevents the next stage | handler.py:42 | Resolve the primary finding before handoff |

| Severity | Trust boundary | Finding | Evidence | Remediation |
| --- | --- | --- | --- | --- |
| HIGH | Tenant lookup | Ownership check absent | handler.py:42 | Constrain lookup to tenant |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Validate trust boundary with its owning workflow | handler.py:42 |
