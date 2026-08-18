# Guide: deliver a first change

## Goal

Deliver one bounded repository change with reviewable scope, explicit approvals, and verification evidence.

## When to use it

Use this after Loop installation when the work does not require the full Harness discovery and refinement catalog.

## Prerequisites

Identify the requested outcome, a safe feature slug, likely paths, and relevant verification commands.

## Procedure

1. Use `ai-sdlc-loop-flow` to Explore the request.
2. Review its owner, blockers, planned writes, and fingerprint.
3. Apply the current route and let the selected owner Specify the change.
4. Approve implementation only after reviewing the spec fingerprint.
5. Verify the changed paths and explicit commands.
6. Approve commit separately only after reviewing current evidence.

## Verify

Confirm all durable artifacts are TOON, changed paths remain in scope, required commands passed, and the commit contains the expected traceability.

## Troubleshooting

Route drift requires a new Explore card. Spec or evidence drift requires a new owning-stage approval. Out-of-scope changes stop the loop.

## Next step

Use [Prepare a release](release.md) when the commit is ready for distribution.
