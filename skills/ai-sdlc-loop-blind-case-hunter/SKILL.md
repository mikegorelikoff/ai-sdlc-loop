---
name: ai-sdlc-loop-blind-case-hunter
description: Use before implementation or during model review to discover omitted actors, failure/recovery dimensions and operational concerns; not arbitrary boundary inputs or code bugs.
---

# ai-sdlc-loop-blind-case-hunter

## 0. Skill Card

- Skill name: `ai-sdlc-loop-blind-case-hunter`
- Primary audience: QA, Dev
- Supporting audience: BA, Architecture, Delivery
- SDLC stage: Model omission discovery
- Purpose: Challenge missing model dimensions using bounded negative search and explicit exclusions.
- Output: Canonical `ai-sdlc-hunter-report/v1` and non-authorizing `ai-sdlc-hunter-handoff/v1`.

## Contract

- Preconditions: explicit source root, scope, and bounded source inventory with
  requirements/design/implementation/tests/operations roles. Discover relevant
  paths via repository search or the existing context-cache; do not read all code.
- Inputs: inventory for prepare; current source-bound candidates for evaluate;
  reviewed report for verify/render/handoff. Reproduction requires an explicitly
  selected trusted Python unittest and output/log paths.
- Outputs: native TOON candidates, findings, coverage, source hashes and routes.
  Commands print by default; explicit outputs use shared atomic, bounded writes.
- Semantic boundary: propose hypotheses, impacts, canonical equivalence signatures
  and review decisions with reasons. Python owns applicable dimensions, IDs,
  status gates, dedupe, negative search, counts, ordering and rendering.
- Completion: requested dimensions considered, exclusions evidenced, candidates
  validated, uncertainties retained, current report verifies and chat validates.
  Empty or inapplicable analysis is BLOCKED, never a clean-bill-of-health claim.
- Handoff: requirements/readiness and SDD; proposals cannot silently become requirements.

## Determinism Contract

Use `scripts/hunt.py` and the sibling shared engine. Source snapshots and exact
anchors bind evidence; changing files invalidates evaluation and handoff. IDs
use SHA-256 of hunter/scope/dimension/path/normalized signature; severity uses
the existing critical/high/medium/low/info vocabulary. Semantic impact inputs
are not confidence. Preserve cross-hunter links; never merge unlike kinds.

## Deterministic Execution Contract

Use [the owning Python entry point](scripts/hunt.py).

- D: prepare, parse, verify, search, deduplicate, rank and render with Python.
- S: hypothesis quality, meaning of coverage, defect reasoning and impact.
- H: explicit semantic candidates become proposals only after deterministic gates.
At most three candidate iterations; after that return ANALYSIS_INCOMPLETE.
OKF remains document provenance; hunters never write lifecycle or approval state.

## Failure Handling

Invalid input, stale evidence, unsupported dimensions and unresolved references
fail closed with native errors. Incomplete negative search is UNKNOWN. A test
error, timeout or unsuccessful reproduction means UNVERIFIED, not NO_BUG.
Review rejection or sourced exclusion prevents promotion. A confirmed bug needs
both a current failing-test receipt and an explicit evidence-backed review.

## Chat Output Contract

Primary: ID / Missing concern / Dimension / Gap evidence / Impact / Next action.
Summary: Status / Decision / Evidence. Failure: Analysis scope / Status / Blocker / Evidence / Required action.
Clarification: Missing input / Why required / Known evidence / Options.
Next action: Owner / Next action / Expected evidence. Keep cells within 180
characters and previews within eight rows. Use the shared renderer/evaluator;
full TOON carries omitted rows. Preserve native artifacts; no duplicate prose.

See [execution and evidence rules](references/execution.md) and
[local chat schema](references/chat-output.toon). Normal hypotheses are proposals;
warning/unknown and blocked cases remain structured with an owned next action.

## Step Selector

This table is generated from `steps/manifest.toon`. The manifest and linked
step documents are canonical; regenerate this projection after graph changes.

| Step | Ready when | Depends on | Operation | Load |
| --- | --- | --- | --- | --- |
| `preflight` | `prepare` | none | `bound-discovery` | [`steps/01-prepare.md`](steps/01-prepare.md) — `required` |
| `context` | `clarify`, `route` | `preflight` | `compile-context` | [`steps/02-context.md`](steps/02-context.md) — `required` |
| `execute` | `execute` | `context` | `evaluate-hypotheses` | [`steps/03-execute.md`](steps/03-execute.md) — `on-demand` |
| `validate` | `validate` | `execute` | `verify-findings` | [`steps/04-validate.md`](steps/04-validate.md) — `before-completion` |
| `handoff` | `handoff`, `complete` | `validate` | `route-findings` | [`steps/05-handoff.md`](steps/05-handoff.md) — `before-completion` |

## Progressive Disclosure Contract

- Resolve the phase entrypoint and dependency-ready set with
  `ai-sdlc-loop-shared-runtime/scripts/ai_sdlc_steps.py`; never invent a step path.
- Read only the emitted StepCard and its selected context. Pass completed step
  IDs back to the selector before requesting the next ready node.
- Treat `direct_read` as an explicit context strategy. Block only when mandatory
  evidence or critical anchors are missing.
- Explore is read-only. After Apply, journal every selected owning-skill step,
  including analysis and validation nodes, before advancing the graph.
- In source use `skills/<skill>/...`; use `.agents/skills/<skill>/...` for
  Codex, `.claude/skills/<skill>/...` for Claude Code, or the project skills
  root recorded in `.ai-sdlc-loop/install/<profile>.toon` for `agent-project`.
