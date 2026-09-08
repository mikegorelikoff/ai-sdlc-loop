# Guide: deliver a bounded change

## Goal

Complete one repository change with explicit scope, repository-grounded engineering review, verification evidence, and separate implementation and commit approvals.

## When to use it

Use Loop when the request needs a safe coding cycle but does not need the complete AI SDLC Harness discovery and refinement catalog.

## Prerequisites

- Python 3 and Git are available.
- Loop is installed and verified for the project.
- The intended source paths and validation commands can be identified.
- A human or authorized host can provide approval decisions.

## Procedure

If the request is still raw, first [clarify the requirements](requirements-discovery.md)
to compare business options and prepare stakeholder questions.

1. Ask for `ai-sdlc-loop-orchestrate` and describe the bounded outcome.
2. Review the normalized request, allowed paths, trace IDs, and specification fingerprint.
3. Approve or reject implementation explicitly.
4. Review the resulting changed paths and run
   `ai-sdlc-loop-engineering-quality-gate`.
5. Inspect the repository profile, representative examples, findings, safe
   fixes, deterministic check outcomes, and current quality-report fingerprint.
6. Run the declared tests and checks through Verify only when the report is
   ready for the next stage.
7. Review readiness, redacted evidence, and the verified fingerprint.
8. Approve or reject the commit separately.

## Verify

Confirm that feature state, the current engineering quality report, and verification evidence are TOON; all changed paths are in scope; no blocking finding remains; every required available command passed; and the resulting commit contains the expected traceability.

## Troubleshooting

- **Approval rejected as stale:** regenerate the relevant fingerprint after reviewing drift.
- **Out-of-scope path:** stop and update the specification; do not widen scope implicitly.
- **Quality report stale or non-ready:** rerun the gate against the current diff;
  do not copy, edit, or bypass its fingerprinted decision.
- **Verification not ready:** resolve the named failing or missing command and rerun Verify.
- **Installer reports drift:** preserve the local skill edit and review it before replacement.

## Next step

Use [Reference](../reference/index.md) for exact skills and commands, or [Project](../project/index.md) for support and security boundaries.
