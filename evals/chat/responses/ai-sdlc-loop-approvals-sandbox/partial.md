| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Partial result: second case is unverified; do not infer full coverage. | sandbox.log:3 |

| Command | Boundary | Escalation | Evidence |
| --- | --- | --- | --- |
| pytest tests/api | External cache write | Not required | sandbox.log:3 |
| pytest tests/api | External cache write [pending case] | Not required | sandbox.log:3 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate blocked command with its owning workflow | sandbox.log:3 |
