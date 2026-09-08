# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared subject result; evidence supports the reported result. | commit-message.txt |

| Subject | Specification | Task ID | Validation | Evidence |
| --- | --- | --- | --- | --- |
| fix(payments): deduplicate retries | specs/payments | T001 | PASS | commit-message.txt |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate change summary with its owning workflow | commit-message.txt |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | commit-message.txt |

| Subject | Specification | Task ID | Validation | Evidence |
| --- | --- | --- | --- | --- |
| fix(payments): deduplicate retries | specs/payments | T001 | PASS | commit-message.txt |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate change summary with its owning workflow | commit-message.txt |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Change summary is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Change summary | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Change summary | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide change summary |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide change summary | Validated change summary |
