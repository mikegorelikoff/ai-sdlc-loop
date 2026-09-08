Result
Status: BLOCKED
Decision: One severity result; scope and evidence are explicit.
Evidence: TC-001 reproduces double charge

primary: Evidence: TC-001 reproduces double charge; Finding: Duplicate charge on retry; Location: src/payments.py:84; Required fix: Reuse idempotency key; Severity: HIGH.
failures: Review diff: Review diff; Status: BLOCKED; Blocker: Unresolved behavior prevents the next stage; Evidence: TC-001 reproduces double charge; Required action: Resolve the primary finding before handoff.
actions: Owner: Engineer; Next action: Validate review diff with its owning workflow; Expected evidence: TC-001 reproduces double charge.
