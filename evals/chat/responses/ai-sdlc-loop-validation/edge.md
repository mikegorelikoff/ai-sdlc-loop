| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared expected / actual entities; listed evidence satisfies this skill check. | validation.log:5 |

| Check | Expected | Actual | Status | Evidence |
| --- | --- | --- | --- | --- |
| pytest tests/payments &#124; перенос<br>строки | All assertions pass | 12 passed | PASS | validation.log:5 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Validate verification command with its owning workflow | validation.log:5 |

```toon
schema: fixture/v1
status: pending
source: "literal | value"
```
