# Validate evidence

## Entry

`evidence.toon` exists.

## Procedure

Confirm schema, spec and change fingerprints, ordered commands, redaction, and
readiness. Recompute against current changes to detect drift, and revalidate the
engineering quality report so verification-side workspace changes cannot reuse
stale readiness. Use `ai-sdlc-loop-qa` for acceptance, regression, and
manual-check signoff; `ai-sdlc-loop-code-review` for independent correctness
review; and `ai-sdlc-loop-security-testing` when authorization, input, secret,
command, or trust-boundary risk is present.

## Exit

Passing evidence may proceed to separate commit approval; failed or drifted evidence may not.
