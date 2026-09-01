---
name: ai-sdlc-loop-implement
description: Enforce the fingerprint-bound Implement approval, constrain source mutation to approved paths, and hand the bounded diff to the mandatory engineering quality gate.
---

# AI SDLC Loop — Implement

Follow `steps/manifest.toon`. This is the only Loop skill that authorizes the
requested source mutation, and only after a matching approval receipt. A
completed implementation is not ready for Verify until
`ai-sdlc-loop-engineering-quality-gate` produces a current ready report.
