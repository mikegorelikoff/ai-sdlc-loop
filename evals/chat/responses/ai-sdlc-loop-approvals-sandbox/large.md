| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | 20 command records; 8 shown; inspect the linked full artifact. | sandbox.log:3 |

| Command | Boundary | Escalation | Evidence |
| --- | --- | --- | --- |
| pytest tests/api | External cache write #1 | Not required | sandbox.log:3 |
| pytest tests/api | External cache write #2 | Not required | sandbox.log:3 |
| pytest tests/api | External cache write #3 | Not required | sandbox.log:3 |
| pytest tests/api | External cache write #4 | Not required | sandbox.log:3 |
| pytest tests/api | External cache write #5 | Not required | sandbox.log:3 |
| pytest tests/api | External cache write #6 | Not required | sandbox.log:3 |
| pytest tests/api | External cache write #7 | Not required | sandbox.log:3 |
| pytest tests/api | External cache write #8 | Not required | sandbox.log:3 |

| Shown | Total | Full evidence |
| --- | --- | --- |
| 8 | 20 | full-result.toon |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate blocked command with its owning workflow | sandbox.log:3 |
