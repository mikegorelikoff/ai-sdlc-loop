| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | 20 severity records; 8 shown; inspect the linked full artifact. | TC-001 |

| Severity | Location | Finding | Disposition | Verification | Evidence |
| --- | --- | --- | --- | --- | --- |
| HIGH | src/payments.py:84 | Duplicate callback creates charge (case 1) | Fixed locally #1 | PASS | TC-001 |
| HIGH | src/payments.py:84 | Duplicate callback creates charge (case 2) | Fixed locally #2 | PASS | TC-001 |
| HIGH | src/payments.py:84 | Duplicate callback creates charge (case 3) | Fixed locally #3 | PASS | TC-001 |
| HIGH | src/payments.py:84 | Duplicate callback creates charge (case 4) | Fixed locally #4 | PASS | TC-001 |
| HIGH | src/payments.py:84 | Duplicate callback creates charge (case 5) | Fixed locally #5 | PASS | TC-001 |
| HIGH | src/payments.py:84 | Duplicate callback creates charge (case 6) | Fixed locally #6 | PASS | TC-001 |
| HIGH | src/payments.py:84 | Duplicate callback creates charge (case 7) | Fixed locally #7 | PASS | TC-001 |
| HIGH | src/payments.py:84 | Duplicate callback creates charge (case 8) | Fixed locally #8 | PASS | TC-001 |

| Shown | Total | Full evidence |
| --- | --- | --- |
| 8 | 20 | full-result.toon |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate implementation diff with its owning workflow | TC-001 |
