Result
Status: BLOCKED
Decision: Review complete; resolve the reported blocker before delivery.
Evidence: TC-001 reproduces double charge

primary: Evidence: TC-001 reproduces double charge; Finding: Duplicate charge on retry; Location: src/payments.py:84; Required fix: Reuse idempotency key; Severity: HIGH.
failures: Review diff: Review diff; Status: BLOCKED; Blocker: Unresolved behavior prevents the next stage; Evidence: TC-001 reproduces double charge; Required action: Resolve the primary finding before handoff.
actions: Owner: Engineer; Next action: Validate review diff with its owning workflow; Expected evidence: TC-001 reproduces double charge.

secondary: Check: Confirm check for payment retry; Status: PENDING; Evidence: TC-001 reproduces double charge; Coverage gap: Confirm coverage gap for payment retry.
