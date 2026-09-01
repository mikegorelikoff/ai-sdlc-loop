# Execute — Engineering Quality Gate

> Executable checkpoint: execute

## Entry

A current bounded context profile and repository engineering profile exist.
Source bytes have not been changed by this gate, and the preflight authority
result is explicit.

## Procedure

### 1. Record findings before mutation

Review as a skeptical Staff Engineer. Optimize, in order, for correctness,
repository consistency, regression safety, simplicity, maintainability,
testability, and relevant performance. Compare the change with the cited
repository examples rather than with an invented ideal architecture.

Create all findings before editing. Follow `references/report-schema.toon` and
give each finding a stable ID, non-inflated `high|medium|low` severity, allowed
category, repository-relative file and optional location, concise issue,
non-empty evidence, concrete impact, recommended fix, and resolution state.
Product ambiguity remains an explicit unresolved finding; do not guess.

Review every applicable dimension:

- correctness: requirements, acceptance behavior, edge and empty states,
  contracts, state transitions, transactions, async/concurrency/retry behavior,
  resources, serialization, and fallbacks;
- repository fit: existing helpers and abstractions, naming, validation, errors,
  logging, dependency injection, data access, tests, and layer boundaries;
- simplicity and maintainability: duplication, responsibilities, control flow,
  public API clarity, hidden side effects, magic values, misleading comments,
  unnecessary indirection, and speculative generality;
- testing: behavior and negative/boundary coverage, changed behavior, excessive
  mocking, brittle implementation coupling, and existing test style;
- security and reliability where evidenced: validation, authorization, paths,
  injection, secrets, deserialization, external calls, failure isolation,
  retries, races, and idempotency;
- scope: files and approximate lines changed, unrelated modifications, new
  dependencies/abstractions, public API changes, and why the diff budget is
  proportionate.

Explicitly check AI-code smells: obvious narration comments, one-use generic
abstractions, invented architecture, excessive helpers or wrappers, duplicate
utilities, silent/catch-all fallbacks, excessive mocks, TODO placeholders,
speculative compatibility/configuration, unrelated refactors, oversized change,
fake impossible-state checks, and solving a broader problem than requested.

### 2. Run pre-fix verification

Detect commands only from repository-owned contracts such as contributor
instructions, scripts, task runners, package metadata, CI, and build/lint/type
configuration. Use argv, never a shell string. Choose a deterministic order:
focused affected checks before broader build, typecheck, lint, unit/integration
tests, or static analysis. Run only commands allowed by the active host and
record exact argv, kind, `before_fix` phase, required/available status, outcome
(`pass|fail|not_run|unavailable`), bounded evidence, and reason/counts where
applicable. Never claim unexecuted success.

### 3. Apply only authorized material fixes

Fix High findings and safe localized Medium findings when repository evidence
supports one clear correction. Immediately before the first source edit, rerun
Loop `implement-check`; for every proposed path, prove containment in the
current `spec.toon` `allowed_paths`. If either check fails, keep the finding
open with the authority or scope reason.

Do not fix Low findings, broad-refactor Medium findings, clarification-blocked
findings, unrelated defects, or style preferences. Do not add dependencies
casually, redesign architecture, weaken configuration, suppress failures,
delete tests, stage files, commit, or change public behavior except where the
accepted request requires it. Reuse existing repository patterns and the
smallest coherent correction.

After edits, compare the worktree and index with the preflight baseline. Fail
closed on any new path outside `allowed_paths` or any unrelated byte change.

### 4. Rebuild evidence and rerun checks

Regenerate `quality-context.toon` against the post-fix diff; never reuse the
pre-fix fingerprint. Reinspect affected examples when the changed topology
differs. Rerun every relevant check after fixes and label it `after_fix`. Record
failures and unavailable/not-run checks truthfully. Keep before-fix entries as
evidence rather than overwriting them.

Create a repository-relative TOON draft with schema
`ai-sdlc-engineering-quality-gate-draft/v1`, the post-fix context fingerprint,
repository profile, findings fixed and remaining, all verification records,
change scope, evidence-backed quality assessment, and proposed decision.
Exclude volatile timestamps, durations, absolute paths, secrets, and raw
nondeterministic output.

## Exit

Return the pre-mutation finding set, applied fixes, remaining findings,
pre/post-fix verification records, post-fix context fingerprint, unrelated-work
preservation evidence, and draft path. A failed authority, containment, or
preservation check makes readiness false.
