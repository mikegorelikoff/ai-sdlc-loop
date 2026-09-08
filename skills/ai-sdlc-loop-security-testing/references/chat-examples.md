# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review complete; resolve the reported blocker before delivery. | handler.py:42 |

| Trust boundary | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Trust boundary | BLOCKED | Unresolved behavior prevents the next stage | handler.py:42 | Resolve the primary finding before handoff |

| Severity | Trust boundary | Finding | Evidence | Remediation |
| --- | --- | --- | --- | --- |
| HIGH | Tenant lookup | Ownership check absent | handler.py:42 | Constrain lookup to tenant |

| Source | Supported claim | Freshness | Evidence |
| --- | --- | --- | --- |
| provider-contract.md:12 | Idempotency key prevents duplicate charges | Snapshot supplied for this scenario | handler.py:42 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Validate trust boundary with its owning workflow | handler.py:42 |

## warning

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

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Trust boundary is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Trust boundary | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Trust boundary | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide trust boundary |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Provide trust boundary | Validated trust boundary |
