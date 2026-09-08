| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Partial result: second case is unverified; do not infer full coverage. | evidence.toon |

| Check | Expected | Actual | Status | Evidence |
| --- | --- | --- | --- | --- |
| pytest tests/payments | No duplicate charge | One charge observed | PASS | evidence.toon |
| pytest tests/payments | No duplicate charge | One charge observed [pending case] | PASS | evidence.toon |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Validate current quality evidence with its owning workflow | evidence.toon |
