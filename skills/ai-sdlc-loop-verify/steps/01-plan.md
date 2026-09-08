# Plan verification

## Entry

Implementation scope is bounded and complete, and
`.ai-sdlc-loop/<feature>/quality-gate.toon` exists.

## Procedure

First use `ai-sdlc-loop-engineering-quality-gate` to verify that the report is
schema-valid, bound to the current context and change fingerprints, has status
`PASS` or `PASS_WITH_FINDINGS`, and declares
`final_decision.ready_for_next_stage: true`. Any missing, invalid, failed,
non-ready, or stale report blocks Verify. Then use `ai-sdlc-loop-validation` to
select explicit relevant commands, expected outcomes, and a positive timeout.
State the commands before execution.

## Execution contract

Use only with current engineering-quality-gate evidence; use validation to select commands and QA for scenario coverage. This stage does not approve commit.

Read the [shared execution decisions](../../ai-sdlc-loop-shared-runtime/references/execution-contract.md) once for this invocation.
Apply its required/discoverable/inherited/optional input rules to this step's
declared inputs. Record the source and status of material facts, then validate
the owning output contract and current evidence before completion.

## Exit

Proceed with no implicit shell expansion or hidden checks.

## Chat presentation

Before a result, warning, blocker or question, apply the local [chat schema](../references/chat-output.toon) and the Chat Output Contract in `SKILL.md`. Preserve native artifact and tool-input formats.
