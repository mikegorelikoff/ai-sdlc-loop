# Specify route

## Entry

A bounded repository change is requested.

## Procedure

Load `ai-sdlc-loop-specify`, follow its manifest, and return its exact spec fingerprint for human review.

## Execution contract

Route a bounded repository change through the fixed Loop lifecycle; do not substitute orchestration for the owning stage or its approval gates.

Read the [shared execution decisions](../../ai-sdlc-loop-shared-runtime/references/execution-contract.md) once for this invocation.
Apply its required/discoverable/inherited/optional input rules to this step's
declared inputs. Record the source and status of material facts, then validate
the owning output contract and current evidence before completion.

## Exit

Stop before source mutation. The next owner is `ai-sdlc-loop-implement` only after explicit approval.

## Chat presentation

Before a result, warning, blocker or question, apply the local [chat schema](../references/chat-output.toon) and the Chat Output Contract in `SKILL.md`. Preserve native artifact and tool-input formats.
## Adaptive routing

Persist the initial scope through `loop.py specify`; it automatically classifies
execution depth into `state.toon:execution`. Supply observed `--signal` values
for scope, confidence and risk; `--mode` is only a minimum and `--full-flow`
retains DEEP. Use `loop.py next --feature <feature>` to select missing work.
For STANDARD record acceptance, intended implementation and checks as compact
`loop.py adapt --feature <feature> --plan-step "..."` entries. For DEEP complete
the existing planning/readiness/specification work before implementation.

Every owner consumes the same `execution.context_pack`. Extend it with
`adapt --context-file <path> --signal <key=value>`. Record completed adaptive
stages using `adapt --complete-stage <stage> --evidence <existing-path>`; owning
validators remain required. After implementation the router still selects the
Engineering Quality Gate before Verify. Current passing verification ends the
delivery; commit remains a separately authorized action.

Record host stage timing and counters through `adapt --record-stage <stage>
--elapsed <seconds> --model-calls <count> --tool-calls <count>
--context-tokens <count> --skill <owner>`. Omit unavailable counters.
