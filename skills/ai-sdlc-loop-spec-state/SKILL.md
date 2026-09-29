---
name: ai-sdlc-loop-spec-state
description: Maintain persistent specification state, repository index freshness, baseline specifications, and decision rotation across feature development and multi-repository delivery. Operates against declarative .sdlc.toon configuration with Git-backed storage.
---

# ai-sdlc-loop-spec-state: Specification State & Lifecycle Management

`ai-sdlc-loop-spec-state` is the Loop-native specification state management primitive. It connects local feature development to a shared specification storage repository (such as `agent-planning-docs` or internal Git mirrors).

The `.sdlc.toon` configuration file is a **declarative policy file** (similar in spirit to `.customization.toon`) that governs how specification state, baselines, decision knowledgebases, and repository indexes are maintained. Third-party integrations (such as Confluence) remain disabled; specification state is managed exclusively via Git.

## 0. Skill Card

- Skill name: `ai-sdlc-loop-spec-state`
- Primary audience: Software Architect, Software Engineer, Tech Lead
- Supporting audience: BA, PM, PO, QA
- Audience tags: Architect, Dev, Lead, BA, QA
- SDLC stage: Cross-lifecycle specification state persistence and rotation
- Purpose: Keep repository specification context synchronized, compact, fresh, and deterministically accessible for downstream SDD skills without token bloat.
- Output: Synchronized specification context hierarchy (index, baseline, decision archive, incremental specs), published feature artifacts, rotated baselines, and status reports.

## Chat Output Contract

Primary: Operation / Repository ID / Status / Storage / Sync state.
Rows represent spec state operations and synchronization records.
Summary: Status / Repository ID / Storage. Failure: Operation / Status / Blocker / Evidence / Required action.
Clarification: Missing configuration / Why required / Known evidence / Options.
Use PASS, FAIL, WARNING, BLOCKED, PENDING, N/A only for chat statuses; preserve native domain states.
At most six columns, eight preview rows and 180 characters per cell; link full evidence and state omitted totals.
No duplicate prose. Keep code, commands, commit messages and machine handoffs native.
Apply [this skill’s schema and examples](references/chat-output.toon) before any user-facing result, warning or recommendation.
Use the sibling `ai-sdlc-loop-shared-runtime/scripts/chat_output.py` to render/check.

## Deterministic Execution Contract

- D: use [the owning Python entry point](scripts/spec_state.py) with explicit subcommands (`init`, `fetch`, `publish`, `status`, `refresh-index`, `rotate`, `cleanup`); success covers executed checks.
- S: interpret declarative `.sdlc.toon` configuration in repository root; cite exact storage provider, repository identity, and artifact paths.
- H: validate specification state before handoff. Downstream skills consume structured context packages without token bloat.
- Read explicit paths; never invent remote repository state. Fail open: state sync warnings never destroy uncommitted local work.

## Operations

The skill exposes focused operations:
- `init`: Scaffold a declarative `.sdlc.toon` configuration file.
- `fetch`: Retrieve the compact specification context hierarchy from storage.
- `publish`: Prepare, format, and publish feature artifacts (spec, plan, decisions, readable spec).
- `status`: Display human-readable and machine-readable state metrics and sync health.
- `refresh-index`: Generate or update the compact structural repository index.
- `rotate`: Execute atomic baseline and decision archive rotation when thresholds are reached.
- `cleanup`: Apply configurable retention policies to historical archived artifacts.

## Step Selector

| Step | Ready when | Depends on | Operation | Load |
| --- | --- | --- | --- | --- |
| `preflight` | `prepare` | none | `validate-configuration` | [`steps/01-prepare.md`](steps/01-prepare.md) — `required` |
| `context` | `clarify`, `route` | `preflight` | `fetch-spec-hierarchy` | [`steps/02-context.md`](steps/02-context.md) — `required` |
| `execute` | `execute` | `context` | `synchronize-spec-state` | [`steps/03-execute.md`](steps/03-execute.md) — `on-demand` |
| `validate` | `validate` | `execute` | `validate-evidence` | [`steps/04-validate.md`](steps/04-validate.md) — `before-completion` |
| `handoff` | `handoff`, `complete` | `validate` | `handoff-result` | [`steps/05-handoff.md`](steps/05-handoff.md) — `before-completion` |

## Progressive Disclosure Contract

- Read `.sdlc.toon` for declarative storage and lifecycle rules; never hardcode external repository names or fixed branches.
- Third-party integrations (e.g. Confluence) are currently disabled/deferred; state is maintained exclusively in Git.
- Use `scripts/spec_state.py` for all deterministic calculations (age, counts, baseline resolution, Git sync).
- Expose Python library APIs (`fetch_spec_state`, `publish_spec_state`, `status_spec_state`, `check_rotation`) so sibling Loop skills (`ai-sdlc-loop-sdd`, `ai-sdlc-loop-requirements-discovery`, `ai-sdlc-loop-flow`) can consume state programmatically.
