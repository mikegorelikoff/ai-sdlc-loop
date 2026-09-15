# Execute verification

## Entry

The command list is explicit.

## Procedure

Run `verify` with repeatable `--command`. Persist bounded redacted `evidence.toon`; any nonzero, missing, interrupted, or timed-out command blocks readiness.

## Exit

Return the verified fingerprint or the exact failing evidence.

## Bounded deterministic verification

The shared `loop.py verify` runner records command/stage durations and bounds
verification to three executed attempts. An unchanged passing state returns its
current receipt; an unchanged failed state stops. Repair the cause first. For a
changed environment, provide concrete `--retry-condition` evidence. Neither
respecification nor escalation resets attempt history for the feature.

Commands run sequentially by default. After checking resource independence,
`--jobs 2 --independent` runs explicit commands concurrently (maximum eight).
Both pre- and post-command source snapshots and the current quality report must
still match. Do not run formatters or source mutations concurrently with checks.
