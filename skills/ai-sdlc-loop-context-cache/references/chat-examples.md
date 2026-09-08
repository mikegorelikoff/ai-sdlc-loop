# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared query result; evidence supports the reported result. | context-pack.toon:12 |

| Query | Strategy | Freshness | Budget used | Evidence |
| --- | --- | --- | --- | --- |
| payment retries | direct_read | Current source hash | 820 / 2000 tokens | context-pack.toon:12 |

| Excluded source | Reason | Evidence |
| --- | --- | --- |
| build/generated-client.py | Generated duplicate of tracked source | context-pack.toon:12 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate context query with its owning workflow | context-pack.toon:12 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | context-pack.toon:12 |

| Query | Strategy | Freshness | Budget used | Evidence |
| --- | --- | --- | --- | --- |
| payment retries | direct_read | Current source hash | 820 / 2000 tokens | context-pack.toon:12 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate context query with its owning workflow | context-pack.toon:12 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Context query is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Context query | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Context query | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide context query |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide context query | Validated context query |
