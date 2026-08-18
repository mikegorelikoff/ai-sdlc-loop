# Guided Flow Contract

## Explore

Explore reads only bounded repository evidence. It never writes state, logs, caches, branches, or artifacts. The decision fingerprint covers the normalized intent, feature, selected stage and skill, rigor, repository identity, source digests, blockers, and planned writes.

## Apply

Apply accepts a complete `ai-sdlc-loop-flow/v1` TOON card, rebuilds it from current evidence, and requires the same fingerprint. A successful Apply is a verified handoff to exactly one owning skill. It is not authentication, approval, sandbox permission, source mutation, command execution, or commit authority.

## Routing

Explicit intent for diagnosis, commit, release, security, review, testing, verification, implementation, or specification routes to the matching Loop owner. A new implementation request first routes to Specify; existing `specified`, `verification-failed`, and `verified` state resumes Implement, Verify, and commit preparation respectively. Ambiguous delivery intent routes to `ai-sdlc-loop-orchestrate`. Missing owners block the card.
