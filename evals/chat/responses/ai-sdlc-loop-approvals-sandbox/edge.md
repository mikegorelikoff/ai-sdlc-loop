| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared boundary / escalation entities; listed evidence satisfies this skill check. | sandbox.log:3 |

| Command | Boundary | Escalation | Evidence |
| --- | --- | --- | --- |
| pytest tests/api &#124; перенос<br>строки | External cache write | Not required | sandbox.log:3 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate blocked command with its owning workflow | sandbox.log:3 |

```toon
schema: fixture/v1
status: pending
source: "literal | value"
```
