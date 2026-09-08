# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared commit result; evidence supports the reported result. | commit-receipt.toon |

| Commit | Branch | Included scope | Approval | Evidence |
| --- | --- | --- | --- | --- |
| abc1234 | feature/payments | T001 only | Current fingerprint | commit-receipt.toon |

| Remaining path | Reason | Evidence |
| --- | --- | --- |
| Recorded in retry decision DEC-001 | Generated duplicate of tracked source | commit-receipt.toon |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Validate commit approval with its owning workflow | commit-receipt.toon |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | commit-receipt.toon |

| Commit | Branch | Included scope | Approval | Evidence |
| --- | --- | --- | --- | --- |
| abc1234 | feature/payments | T001 only | Current fingerprint | commit-receipt.toon |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Validate commit approval with its owning workflow | commit-receipt.toon |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Commit approval is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Commit approval | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Commit approval | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide commit approval |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Provide commit approval | Validated commit approval |
