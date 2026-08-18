# Validate evidence

## Entry

`evidence.toon` exists.

## Procedure

Confirm schema, spec and change fingerprints, ordered commands, redaction, and readiness. Recompute against current changes to detect drift. Use `ai-sdlc-loop-qa` for acceptance, regression, and manual-check signoff; `ai-sdlc-loop-code-review` for correctness; and `ai-sdlc-loop-security-testing` when authorization, input, secret, command, or trust-boundary risk is present.

## Exit

Passing evidence may proceed to separate commit approval; failed or drifted evidence may not.
