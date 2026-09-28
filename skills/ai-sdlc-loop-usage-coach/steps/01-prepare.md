# Prepare

## Entry

The contributor invoked the usage coach or requested behavioral workflow feedback.

## Procedure

Resolve safe project-relative paths, active or requested session identifier, and establish read-only coaching advisory authority. Fail open if the usage session directory does not yet exist.

## Execution contract

Read the [shared execution decisions](../../ai-sdlc-loop-shared-runtime/references/execution-contract.md) once for this invocation.
Coach provides evidence-backed suggestions and reports; it never mutates source code or grants workflow approvals.

## Exit

Input paths are resolved and journal discovery bounds are established.

## Chat presentation

Before a result, warning, blocker or question, apply the local [chat schema](../references/chat-output.toon) and the Chat Output Contract in `SKILL.md`. Preserve native artifact and tool-input formats.
