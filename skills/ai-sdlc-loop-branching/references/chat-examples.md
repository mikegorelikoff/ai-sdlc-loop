# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared current branch result; evidence supports the reported result. | fixture.toon:1 |

| Current branch | Expected branch | Base revision | Worktree | Decision |
| --- | --- | --- | --- | --- |
| feature/025-chat-output | feature/025-chat-output | abc1234 | Clean | Reuse task branch |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Validate task scope with its owning workflow | fixture.toon:1 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | fixture.toon:1 |

| Current branch | Expected branch | Base revision | Worktree | Decision |
| --- | --- | --- | --- | --- |
| feature/025-chat-output | feature/025-chat-output | abc1234 | Clean | Reuse task branch |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Validate task scope with its owning workflow | fixture.toon:1 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Task scope is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Task scope | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Task scope | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide task scope |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Provide task scope | Validated task scope |
