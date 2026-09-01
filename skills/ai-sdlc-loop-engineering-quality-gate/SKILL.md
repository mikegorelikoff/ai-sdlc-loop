---
name: ai-sdlc-loop-engineering-quality-gate
description: Mandatory repository-grounded engineering quality gate for completed AI implementations. Use after any implementation step, and in AI SDLC Loop between Implement and Verify, to inspect the request and current diff, compare relevant repository patterns, record typed adversarial findings before mutation, run deterministic checks, fix only authorized High and safe localized Medium findings, rerun checks, and emit a current canonical TOON report plus concise human YAML. Supports `--quick-flow` and `--full-flow` without weakening approval, scope, evidence, or readiness rules.
---

# AI SDLC Loop — Engineering Quality Gate

Evaluate whether the change is the correct implementation for this repository,
not whether the changed code looks reasonable in isolation. Prefer repository
evidence and executed checks over model opinion.

## Skill card

- Stage: mandatory after Implement and before Verify; independently callable
  after any implementation step.
- Owner: software engineer; supporting owners are QA and Security.
- Durable outputs:
  `.ai-sdlc-loop/<feature>/quality-context.toon` and
  `.ai-sdlc-loop/<feature>/quality-gate.toon`.
- Human output: concise YAML rendered in the active response; do not persist a
  second Markdown or JSON report.
- Canonical report schema: `ai-sdlc-engineering-quality-gate/v1`.
- Mutation authority: an existing, current Loop Implement approval and its
  `allowed_paths`; invoking this skill never creates or broadens authority.

## Step selector

The manifest and linked documents are canonical. Resolve the ready step with
`ai-sdlc-loop-shared-runtime/scripts/ai_sdlc_steps.py`; do not invent a step
path or skip a dependency.

| Step | Ready when | Depends on | Load |
| --- | --- | --- | --- |
| `preflight` | `prepare` | none | [`steps/01-prepare.md`](steps/01-prepare.md) — required |
| `context` | `clarify`, `route` | `preflight` | [`steps/02-context.md`](steps/02-context.md) — required |
| `execute` | `execute` | `context` | [`steps/02-execute.md`](steps/02-execute.md) — on demand |
| `validate` | `validate` | `execute` | [`steps/03-validate-and-handoff.md`](steps/03-validate-and-handoff.md) — before completion |
| `handoff` | `handoff`, `complete` | `validate` | [`steps/04-handoff.md`](steps/04-handoff.md) — before completion |

## Required resources

- Read [`references/quality-gate-contract.md`](references/quality-gate-contract.md)
  before review or remediation.
- Read [`references/context-schema.toon`](references/context-schema.toon) and
  [`references/report-schema.toon`](references/report-schema.toon) before
  creating a draft or interpreting a report.
- Read [`references/usage-examples.md`](references/usage-examples.md) only when
  invocation or draft construction needs an example.
- Use
  [`references/example-quality-report.toon`](references/example-quality-report.toon)
  as shape guidance, never as evidence or a reusable verdict.
- Use `scripts/engineering_quality_gate.py` for deterministic context capture,
  canonical report finalization, fingerprints, and current-state verification.

## Non-negotiable boundaries

- Create findings before editing source. Fix every safely resolvable evidenced
  High and each safe, localized Medium that current authority permits; never
  fix Low findings as opportunistic cleanup.
- Before any gate fix, run the shared Loop runtime `implement-check` for the
  feature and enforce the current `spec.toon` `allowed_paths`. A missing,
  rejected, stale, or mismatched receipt makes the run review-only.
- Preserve unrelated tracked, staged, unstaged, and untracked bytes. Do not
  stage, commit, suppress tests, weaken lint or type rules, add dependencies
  casually, redesign architecture, or rewrite unrelated files.
- Record verification as `pass`, `fail`, `not_run`, or `unavailable`. Never
  infer success from a command that was not executed.
- Rebuild context after every source fix. A report bound to an earlier diff is
  stale and cannot be ready.
- Keep durable machine artifacts TOON-only. Exclude timestamps, durations,
  absolute paths, raw nondeterministic output, and secrets from fingerprinted
  identity.

## Runtime paths

Treat `skills/` as the logical skill root in the standalone Loop repository. In
an installed project use `.agents/skills/`, `.claude/skills/`, or the safe
project skills root recorded by the Loop installer. In this Harness checkout,
the source root is `products/ai-sdlc-loop/skills/`. Verify that the chosen root
contains this skill and `ai-sdlc-loop-shared-runtime` before running helpers.
