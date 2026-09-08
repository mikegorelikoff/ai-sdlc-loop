| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | sandbox.log:3 |

| Command | Boundary | Escalation | Evidence |
| --- | --- | --- | --- |
| pytest tests/api | External cache write | Not required | sandbox.log:3 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate blocked command with its owning workflow | sandbox.log:3 |
