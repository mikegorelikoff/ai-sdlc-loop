# Analyze — Requirements, Business Options and Questions

## Entry

Raw inputs and evidence limits are available; missing answers remain visible.

## Procedure

1. Normalize the request into problem, affected actors, current behavior,
   desired outcome and success measures. Distinguish the stated need from a
   suggested solution, without discarding explicit user constraints.
2. Assign observation/requirement IDs. Classify facts, assumptions,
   contradictions, unknowns and proposals; cite source IDs. Cover workflows,
   triggers, exceptions, permissions, business rules, scope, data and relevant
   non-functional constraints. Do not convert every unknown into a requirement.
3. Derive materially different business responses. Usually compare two to four
   viable options; include doing nothing, a process/manual change, a limited
   pilot or reuse when relevant. Explain if constraints leave only one option.
   Cosmetic UI differences or interchangeable technologies are not distinct
   business options unless they change value, policy, workflow or ownership.
4. For each option describe who benefits, changed workflow and rules, expected
   outcome, evidence/precedent, transfer limits, dependencies, business risks,
   reversibility, cost/effort assumptions and decision-changing unknowns. Avoid
   invented ROI, delivery estimates or precision unsupported by evidence.
5. Compare options against criteria grounded in the request. Explain tradeoffs,
   offer a conditional recommendation and say what evidence would reverse it.
   Keep rejected options and reasons where they illuminate a real constraint.
6. Build the elicitation plan from gaps AND option differences. For each
   material question identify stakeholder role (name only if known), a neutral
   ready-to-send question, linked option/gap IDs, why it matters, priority, where
   to look, and how to obtain a reliable answer: interview, process observation,
   existing policy, ticket/sample audit, analytics or prototype test.
7. State how plausible answers change scope, rules, acceptance criteria or the
   option choice. Distinguish questions needed before selecting a direction
   from questions needed before implementation and optional later learning.
   Group shared questions without losing option-specific follow-ups.
8. Validate and finalize through the helper. Return a compact problem brief, source/evidence inventory, option comparison,
   prioritized questions and next owner using the output contract. Record
   candidate acceptance examples as proposals when stakeholder rules are missing.

## Script Usage

Resolve `skills/` to the installed skills root when needed. For durable work,
run these commands in the project root; use the matching flow flag in prepare.

```bash
python3 skills/ai-sdlc-loop-requirements-discovery/scripts/requirements_discovery.py prepare --feature <feature> --request <raw-input.md> --source <past-decision.md> --quick-flow --write
python3 skills/ai-sdlc-loop-requirements-discovery/scripts/requirements_discovery.py scaffold --context .ai-sdlc-loop/<feature>/requirements-discovery-context.toon --as-of <YYYY-MM-DD> --write
```

For pasted input use `--request-stdin` instead of `--request` and stream the
verbatim request on stdin. Omit `--source` when no historical evidence is available.
The helper marks stdin as a fixed snapshot; file sources receive freshness checks.

Fill only the generated draft using the schema and example in `references/`.
Keep its context fingerprint and explicit date. Supply all business judgments,
evidence limits and source-linked records as data. The empty scaffold is
intentionally invalid until analysis and question coverage are populated.

```bash
python3 skills/ai-sdlc-loop-requirements-discovery/scripts/requirements_discovery.py validate --context .ai-sdlc-loop/<feature>/requirements-discovery-context.toon --draft .ai-sdlc-loop/<feature>/requirements-discovery-draft.toon
python3 skills/ai-sdlc-loop-requirements-discovery/scripts/requirements_discovery.py finalize --context .ai-sdlc-loop/<feature>/requirements-discovery-context.toon --draft .ai-sdlc-loop/<feature>/requirements-discovery-draft.toon --write
python3 skills/ai-sdlc-loop-requirements-discovery/scripts/requirements_discovery.py verify --report .ai-sdlc-loop/<feature>/requirements-discovery.toon
```

All commands are offline. Omit `--write` to emit without persisting; `--replace`
is used only with `--write` after reviewing a differing existing output.
Never bypass a failed check by editing a final report or its fingerprint.
For updated sources, rebuild context and review/rebase the analysis onto it.

## Exit

The packet supports a concrete business discussion and targeted evidence gathering.

Apply [D/S/H](../SKILL.md#deterministic-execution-contract).
