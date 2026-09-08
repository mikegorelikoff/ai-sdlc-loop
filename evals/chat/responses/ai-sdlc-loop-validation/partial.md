| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Partial result: second case is unverified; do not infer full coverage. | validation.log:5 |

| Check | Expected | Actual | Status | Evidence |
| --- | --- | --- | --- | --- |
| pytest tests/payments | All assertions pass | 12 passed | PASS | validation.log:5 |
| pytest tests/payments | All assertions pass | 12 passed [pending case] | PASS | validation.log:5 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Validate verification command with its owning workflow | validation.log:5 |
