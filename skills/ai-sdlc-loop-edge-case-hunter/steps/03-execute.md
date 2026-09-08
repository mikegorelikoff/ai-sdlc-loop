# Propose and evaluate hypotheses

## Entry

Manifest prerequisites and the selected StepCard are satisfied.

## Procedure

Propose candidates inside applicable dimensions with exact quotes, stable semantic signatures, trace targets, impact and review reasons. Run evaluate. Reproduce only an explicitly authorized trusted test in a disposable source copy; this is not an OS sandbox. Never edit production code.

Read [execution](../references/execution.md) and use `scripts/hunt.py`.

## Exit

Return validated evidence or an explicit blocker; no lifecycle authority changes.

Explicit artifact writes belong to this workspace-write step. Reproduction is an optional authorized test execution using the existing validation permission policy; the graph does not grant authority to execute untrusted tests. Other steps use stdout/read-only verification.
