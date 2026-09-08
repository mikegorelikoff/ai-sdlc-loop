# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared command result; evidence supports the reported result. | sandbox.log:3 |

| Command | Boundary | Escalation | Evidence |
| --- | --- | --- | --- |
| pytest tests/api | External cache write | Not required | sandbox.log:3 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate blocked command with its owning workflow | sandbox.log:3 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | sandbox.log:3 |

| Command | Boundary | Escalation | Evidence |
| --- | --- | --- | --- |
| pytest tests/api | External cache write | Not required | sandbox.log:3 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate blocked command with its owning workflow | sandbox.log:3 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Blocked command is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Blocked command | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Blocked command | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide blocked command |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide blocked command | Validated blocked command |
