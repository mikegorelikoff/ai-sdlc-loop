Result
Status: BLOCKED
Decision: Review complete; resolve the reported blocker before delivery.
Evidence: handler.py:42

primary: Evidence: handler.py:42; Finding: Ownership check absent; Remediation: Constrain lookup to tenant; Severity: HIGH; Trust boundary: Tenant lookup.
failures: Trust boundary: Trust boundary; Status: BLOCKED; Blocker: Unresolved behavior prevents the next stage; Evidence: handler.py:42; Required action: Resolve the primary finding before handoff.
actions: Owner: QA; Next action: Validate trust boundary with its owning workflow; Expected evidence: handler.py:42.

secondary: Source: Confirm source for payment retry; Supported claim: Confirm supported claim for payment retry; Freshness: Confirm freshness for payment retry; Evidence: handler.py:42.
