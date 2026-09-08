# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review complete; resolve the reported blocker before delivery. | spec.toon:12 |

| Requirement package | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Requirement package | BLOCKED | Unresolved behavior prevents the next stage | spec.toon:12 | Resolve the primary finding before handoff |

| Requirement ID | Gap category | Severity | Impact | Evidence | Resolution |
| --- | --- | --- | --- | --- | --- |
| AC-002 | Business rule | HIGH | Timeout untestable | spec.toon:12 | Define deadline |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Validate requirement package with its owning workflow | spec.toon:12 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review complete with a blocking finding and a source-freshness warning. | spec.toon:12 |

| Requirement package | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Requirement package | BLOCKED | Unresolved behavior prevents the next stage | spec.toon:12 | Resolve the primary finding before handoff |

| Requirement ID | Gap category | Severity | Impact | Evidence | Resolution |
| --- | --- | --- | --- | --- | --- |
| AC-002 | Business rule | HIGH | Timeout untestable | spec.toon:12 | Define deadline |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Validate requirement package with its owning workflow | spec.toon:12 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Requirement package is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Requirement package | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Requirement package | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide requirement package |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Provide requirement package | Validated requirement package |
