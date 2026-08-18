# Runtime contracts

- Loop state schema: `ai-sdlc-loop/v1` encoded as canonical TOON.
- Promotion schema: `ai-sdlc-harness-promotion/v1` encoded as canonical TOON.
- Install schema: `ai-sdlc-loop-install/v1` encoded as canonical TOON.
- Durable extensions: `.toon` only for state, specifications, approvals, evidence, install records, and promotion output.
- Fingerprints: SHA-256 over canonical TOON with the fingerprint field omitted.
- Authority: Implement and Commit receipts are distinct and bound to current fingerprints.
