# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared requirement id result; evidence supports the reported result. | spec.toon |

| Requirement ID | Bounded behavior | Allowed path | Acceptance | Evidence |
| --- | --- | --- | --- | --- |
| AC-001 | Idempotent retry | src/payments.py | One charge per key | spec.toon |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate allowed scope with its owning workflow | spec.toon |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | spec.toon |

| Requirement ID | Bounded behavior | Allowed path | Acceptance | Evidence |
| --- | --- | --- | --- | --- |
| AC-001 | Idempotent retry | src/payments.py | One charge per key | spec.toon |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate allowed scope with its owning workflow | spec.toon |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Allowed scope is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Allowed scope | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Allowed scope | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide allowed scope |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide allowed scope | Validated allowed scope |
