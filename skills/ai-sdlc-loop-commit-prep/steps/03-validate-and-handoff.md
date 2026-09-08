# Validate commit preparation

## Entry

The proposed commit contents and current Loop evidence have been inspected.

## Procedure

Independently check that every proposed path belongs to the verified snapshot,
excluded dirty paths remain untouched, the message validator passed and
`loop.py evidence-check --feature <feature>` still succeeds. Evidence changes
invalidate readiness. Report the branch, feature, proposed paths, exclusions,
message, verified fingerprint, checks and remaining blockers.

A complete preparation result is a proposal for the Commit owner. It is not a
created commit and must not include an invented commit hash. Only
`ai-sdlc-loop-commit` can report the commit after its separate gate and actual
Git execution. Keep optional Harness SDD traceability distinct from mandatory
Loop receipts; never fabricate a full SDD package to make preparation pass.

## Exit

Return ready-for-commit-review or blocked, with evidence and one next required
owner/action. Preserve all existing user changes and separate approval.
