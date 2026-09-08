---
name: ai-sdlc-loop-hierarchical-decomposition
description: Decompose an initiative, Epic or Story into a sourced delivery hierarchy with explicit uncertainty, acceptance, dependencies and independently reviewed branch handoffs. Does not approve implementation or create tickets.
---

# ai-sdlc-loop-hierarchical-decomposition: Hierarchical Delivery Decomposition

## 0. Skill Card

- Skill name: `ai-sdlc-loop-hierarchical-decomposition`
- Primary audience: PM
- Supporting audience: BA, Delivery, Architecture, QA, Dev
- Audience tags: PM, BA, QA, Dev
- SDLC stage: Bounded delivery decomposition before implementation SDD
- Purpose: Build the smallest evidence-backed hierarchy that covers the requested outcome without inventing scope.
- Output: Canonical decomposition candidate and verified report, table-first preview and sourced branch handoff

## Chat Output Contract

Use `scripts/decompose.py render` for complete results: Decomposition Summary
(Metric / Result), Delivery Tree (ID / Type / Parent / Title / Outcome / Status),
then distinct Epic, Feature, Story, Task, Acceptance, INVEST, Traceability,
Assumptions & Unknowns, Quality and Next Action tables when nonempty.
Never invent scores: quality records contain observable gates and reviewer evidence.
Failures: Branch / Status / Blocker / Evidence / Required action.
Clarification: Missing decision / Why required / Known evidence / Options.
At most six columns and eight preview rows per detail table; link the full native
artifact and show omitted totals. No duplicated prose or executable commands in cells.
PASS / FAIL / WARNING / BLOCKED / PENDING / N/A are chat states; preserve domain enums.
Use [chat schema](references/chat-output.toon) for compact progress and questions;
use the decomposition renderer for the full domain report.

## Deterministic Execution Contract

- D: [the owning Python entry point](scripts/decompose.py) owns schemas, IDs, canonical order, coverage, NFR propagation, dependency topology, bounded status and safe writes.
- S: classify input level; identify supported requirements; propose child outcomes, decomposition axes, granularity and independent reviewer judgments with evidence.
- H: validate each candidate, then obtain four current branch review receipts. Structural PASS is not proof that source interpretation is correct.
- Three candidate iterations total. Repair affected branches only; unresolved gates at the limit produce BLOCKED. Never derive approval from confidence.
- Read explicit evidence only. No repository-wide dump, ticket writes, test execution, source modification or lifecycle-state completion in this skill.

## Step Selector

This table is generated from `steps/manifest.toon`. The manifest and linked
step documents are canonical; regenerate this projection after graph changes.

| Step | Ready when | Depends on | Operation | Load |
| --- | --- | --- | --- | --- |
| `preflight` | `prepare` | none | `bound-discovery` | [`steps/01-prepare.md`](steps/01-prepare.md) — `required` |
| `context` | `clarify`, `route` | `preflight` | `collect-requirements-evidence` | [`steps/02-context.md`](steps/02-context.md) — `required` |
| `execute` | `execute` | `context` | `analyze-business-options` | [`steps/02-execute.md`](steps/02-execute.md) — `on-demand` |
| `validate` | `validate` | `execute` | `validate-discovery` | [`steps/03-validate-and-handoff.md`](steps/03-validate-and-handoff.md) — `before-completion` |
| `handoff` | `handoff`, `complete` | `validate` | `handoff-result` | [`steps/04-handoff.md`](steps/04-handoff.md) — `before-completion` |

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
