# Decision log

## 2026-09-08 — Deterministic execution boundaries

Retain Loop's compact lifecycle manifests and interpret them through the
read-only `loop.py steps` selector. Reject malformed graphs and inconsistent
completion claims; selection does not grant action authority. Semantic helper
graphs continue through their existing selector and now require validation
before terminal handoff.

Use Loop receipts for the Loop lifecycle. A compatible Harness SDD package is
optional input, not an implicit prerequisite. Commit preparation proposes
contents and validates current evidence; only the Commit owner validates
separate approval and creates the commit. Recheck the source snapshot after
verification commands and reuse one evidence validator at approval and commit.

Keep all existing skill names, public paths and artifact schemas. Validate
source-bound execution references, graph mutations, intent routing, approval
freshness and every distributed skill graph with local regression tests.

| Date | Decision | Status |
| --- | --- | --- |
| 2026-09-07 | Require deterministic offline scripts for discovery contexts, draft schemas, evidence links, coverage and canonical reports. Stable bytes and local freshness checks supplement model-authored business analysis; the result grants no execution approval. | Accepted |
| 2026-09-07 | Add optional `ai-sdlc-loop-requirements-discovery` before Specify for raw requirements, sourced business options and stakeholder elicitation; its packet grants no implementation approval and adds no required lifecycle stage. Update source inventory to 21 directories; released inventories remain unchanged. | Accepted |
| 2026-08-17 | Publish Loop as the focused independently versioned member of the AI SDLC product family. | Accepted |
| 2026-08-17 | Keep durable Loop-owned machine artifacts canonical TOON. | Accepted |
| 2026-08-17 | Namespace every installed skill as `ai-sdlc-loop-{slug}`. | Accepted |
| 2026-08-18 | Add guided Flow and read-only Doctor without importing the full Harness dependency cascade. | Accepted |
| 2026-08-18 | Mirror Harness documentation architecture and validation while keeping Loop's content surface focused. | Accepted |

## 2026-09-08 — Release 0.3.0

Publish the 21-skill package with deterministic graph selection, current-evidence
gates, requirements discovery and engineering review. Pin install defaults and
first-run commands to v0.3.0. No schema-major migration is introduced; v0.2.0
remains an immutable rollback target.

## 2026-09-15 — Adaptive depth and bounded verification

Preserve the compact graph and approval/quality/evidence contracts. Add adaptive
coordination in existing state under `execution`; `next` selects missing work and
`adapt` records context, decisions and escalation without granting authority.
Independent commands may run concurrently after implementation. Three attempts
bound repair; unchanged failed checks stop. All skills consume the shared adaptive
execution contract. Preserve existing public paths and legacy manual commands.

## 2026-09-25 — Loop-native SDD entry point

Add `ai-sdlc-loop-sdd` as the installed, namespaced SDD entry point. It owns the
same deterministic TOON contract as Specify and routes through the existing
`loop.py specify` runtime rather than importing Harness's larger Markdown SDD
package. Keep `ai-sdlc-loop-specify` as a compatibility path and route new Loop
SDD selections to the new skill. This makes the advertised SDD lifecycle stage
available in every Loop installation without changing approval semantics.
