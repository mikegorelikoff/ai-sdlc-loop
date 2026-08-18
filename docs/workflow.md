# Workflow

Flow is the guided entrypoint; Orchestrate is the direct stage router. Both preserve ownership:

```text
Explore → Apply handoff → Specify → approval → Implement → Verify → approval → Commit
                         ↘ review / QA / security / release controls as required
```

Explore and Doctor are read-only. Apply confirms one route but does not execute the owner action. Specify persists bounded scope. Implement and Commit validate separate fingerprint-bound approval receipts. Verify executes only declared argv-safe commands and records redacted TOON evidence.

See [Contracts](reference/contracts.md) for exact schema and authority boundaries.
