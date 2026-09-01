# Verify route

## Entry

Implementation is complete within the approved paths and
`.ai-sdlc-loop/<feature>/quality-gate.toon` is current for that exact change.

## Procedure

Load `ai-sdlc-loop-verify`; it first validates the quality report's context and
change fingerprints, `PASS` or `PASS_WITH_FINDINGS` status, and
`final_decision.ready_for_next_stage: true`. It then owns explicit command
execution, redacted evidence, readiness, and optional promotion.

## Exit

Report the verified fingerprint. Commit remains separately gated.
