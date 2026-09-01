# Engineering quality gate route

## Entry

Implementation and scope checking are complete for the approved paths.

## Procedure

Load `ai-sdlc-loop-engineering-quality-gate`. It owns bounded repository
context discovery, representative-example selection, adversarial findings,
authorized localized High and Medium fixes, deterministic verification reruns,
and the current fingerprinted quality report.

## Exit

Proceed to `ai-sdlc-loop-verify` only when
`.ai-sdlc-loop/<feature>/quality-gate.toon` is current, has status `PASS` or
`PASS_WITH_FINDINGS`, and declares
`final_decision.ready_for_next_stage: true`. Otherwise stop with the exact
finding, verification, or drift blocker.
