# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared path group result; evidence supports the reported result. | validation.md:8 |

| Path group | Disposition | Reason | Verification | Evidence |
| --- | --- | --- | --- | --- |
| src/payments.py | Include | Implements AC-001 | PASS | validation.md:8 |

| Commit | Branch | Task ID | Evidence |
| --- | --- | --- | --- |
| abc1234 (simulated) | feature/payment-retry | T001 | validation.md:8 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Validate commit scope with its owning workflow | validation.md:8 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | validation.md:8 |

| Path group | Disposition | Reason | Verification | Evidence |
| --- | --- | --- | --- | --- |
| src/payments.py | Include | Implements AC-001 | PASS | validation.md:8 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Validate commit scope with its owning workflow | validation.md:8 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Commit scope is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Commit scope | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Commit scope | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide commit scope |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Provide commit scope | Validated commit scope |
