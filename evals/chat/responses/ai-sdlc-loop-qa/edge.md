| Status | Decision | Evidence |
| --- | --- | --- |
| PENDING | Prepared actor / setup / action entities; owner decision or execution remains pending. | qa.md:20 |

| Scenario ID | Actor / setup | Action | Expected result | Execution status | Evidence |
| --- | --- | --- | --- | --- | --- |
| QA-001 &#124; перенос<br>строки | Operator with failed callback | Replay callback | One ledger entry | PENDING | qa.md:20 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Replay callback | qa.md:20 |

```toon
schema: fixture/v1
status: pending
source: "literal | value"
```
