# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PENDING | Prepared intent result; owner decision or execution remains pending. | fixture.toon:1 |

| Intent | Selected skill | Reason | Authority | Expected artifact |
| --- | --- | --- | --- | --- |
| Clarify retry rules | ai-sdlc-requirements-discovery | Business choice unresolved | Explore only | requirements-discovery.toon |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate user intent with its owning workflow | fixture.toon:1 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | fixture.toon:1 |

| Intent | Selected skill | Reason | Authority | Expected artifact |
| --- | --- | --- | --- | --- |
| Clarify retry rules | ai-sdlc-requirements-discovery | Business choice unresolved | Explore only | requirements-discovery.toon |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate user intent with its owning workflow | fixture.toon:1 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | User intent is unavailable; dependent work has not run. | source-inventory.toon:missing |

| User intent | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| User intent | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide user intent |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide user intent | Validated user intent |
