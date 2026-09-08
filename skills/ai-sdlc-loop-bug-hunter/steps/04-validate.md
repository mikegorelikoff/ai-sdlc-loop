# Verify source-bound findings

## Entry

Manifest prerequisites and the selected StepCard are satisfied.

## Procedure

Run verify on the current report. Check that semantic review matches evidence and expected behavior; observed quotes alone do not prove defects. Repair only failed fields or affected candidates, bounded to three iterations. Use render and the shared chat evaluator.

Read [execution](../references/execution.md) and use `scripts/hunt.py`.

## Exit

Return validated evidence or an explicit blocker; no lifecycle authority changes.

A current fingerprint establishes freshness, not semantic correctness. Preserve unresolved review decisions and never convert a skipped check into PASS.
