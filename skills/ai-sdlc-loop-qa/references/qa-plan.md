# QA plan quality bar

Each acceptance scenario must name an actor, setup, action, observable expected result, evidence type, and risk. Reject generic checks such as “verify it works.”

Regression targets identify existing behavior that may break. Validation entries distinguish passed, failed, planned, and skipped checks. Manual checks include an environment and owner when known. Signoff is `ready` only when required automated and human evidence exists; otherwise use `planned`, `partial`, or `blocked` and state the residual risk.

Never include secrets, production credentials, raw provider tokens, or personal data in a QA artifact.
