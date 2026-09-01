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

## Exit

Proceed with no implicit shell expansion or hidden checks.
