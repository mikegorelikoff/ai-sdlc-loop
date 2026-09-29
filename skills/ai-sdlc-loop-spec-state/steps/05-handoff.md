# Handoff

## Entry

Specification state is validated.

## Procedure

Report specification state to the user and hand off the compact context hierarchy (repository index, latest baseline, decision archive, incremental specs) to downstream skills (`ai-sdlc-loop-sdd`, `ai-sdlc-loop-requirements-discovery`, `ai-sdlc-loop-flow`).

## Output Spec

```text
Spec State:
- Repository: <repo-id> (v<version>)
- Storage: <storage-repo>:<branch>
- Sync status: clean | ahead | behind | diverged
- Repository index: <date> (<age> days old, <status>)
- Latest baseline: <filename> (v<version>, <date>)
- Latest decision archive: <filename> (<date>)
- Incremental feature specs: <count> / <threshold>
- Incremental decision logs: <count> / <threshold>
- Rotation recommendation: none | baseline rotation recommended | version change
- Staged context: .ai-sdlc/spec-state/context/
- Next phase: refinement | implementation | pr-publish
```

## Examples

Valid fetch result:

```text
Spec State:
- Repository: payment-service (v1.2.0)
- Storage: vestwell/agent-planning-docs:main
- Sync status: clean
- Repository index: 20260920 (8 days old, fresh)
- Latest baseline: baselinespec-payment-service-1.2.0-20260901.md (v1.2.0, 20260901)
- Latest decision archive: decision-knowledgebase-payment-service-1.2.0-20260901.md (20260901)
- Incremental feature specs: 4 / 50
- Incremental decision logs: 3 / 50
- Rotation recommendation: none
- Staged context: .ai-sdlc/spec-state/context/
- Next phase: implementation
```

## Exit

Specification context is cleanly handed off to downstream Loop skills without token bloat.

## Chat presentation

Present the result using the owning `SKILL.md` Chat Output Contract and local [chat schema](../references/chat-output.toon).
