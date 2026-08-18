# How it works

Loop separates lifecycle ownership from reusable delivery controls.

## Lifecycle

1. `ai-sdlc-loop-flow` explores and fingerprints one route; `ai-sdlc-loop-orchestrate` remains the direct stage router.
2. `ai-sdlc-loop-specify` normalizes scope and writes the specification fingerprint.
3. `ai-sdlc-loop-implement` checks current approval before source mutation.
4. `ai-sdlc-loop-verify` collects command evidence and computes readiness.
5. `ai-sdlc-loop-commit` checks a separate current approval before one commit.

## Delivery controls

Eleven focused skills own approvals, branching, requirements review, test cases, QA, validation, code review, security testing, commit preparation, Conventional Commit validation, and release readiness. They share one standard-library runtime and do not require the full Harness refinement catalog.

`ai-sdlc-loop-doctor` independently diagnoses the installed inventory and previews non-authorizing upgrade plans. See [Flow](guides/flow.md) and [Doctor](guides/doctor.md) for procedures.

## Authority model

TOON receipts record explicit decisions against exact fingerprints. They are capability records, not cryptographic identity proofs. A missing, rejected, stale, mismatched, or drifted receipt denies the protected transition.

Git remains authoritative for source state. Loop preserves unrelated tracked, staged, unstaged, and untracked work and refuses changes outside the approved paths.

## Evidence model

Verification executes only declared argv-safe commands without a shell. Evidence includes ordered outcomes, bounded redacted output, hashes, and readiness. Any failed, missing, interrupted, or timed-out required command blocks readiness.

## Harness compatibility

`promote` validates Loop state and emits `ai-sdlc-harness-promotion/v1` TOON. It preserves supported request, path, trace, fingerprint, approval, command, and evidence fields without rewriting Harness state.
