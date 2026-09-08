# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared stage result; evidence supports the reported result. | spec.toon |

| Stage | State | Owning skill | Gate | Evidence |
| --- | --- | --- | --- | --- |
| Specify | complete | ai-sdlc-loop-specify | Schema valid | spec.toon |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate feature scope with its owning workflow | spec.toon |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | spec.toon |

| Stage | State | Owning skill | Gate | Evidence |
| --- | --- | --- | --- | --- |
| Specify | complete | ai-sdlc-loop-specify | Schema valid | spec.toon |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate feature scope with its owning workflow | spec.toon |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Feature scope is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Feature scope | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Feature scope | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide feature scope |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide feature scope | Validated feature scope |
