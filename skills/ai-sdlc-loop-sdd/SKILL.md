---
name: ai-sdlc-loop-sdd
description: Create and validate a bounded AI SDLC Loop implementation specification before code mutation. Use for a medium or large change that needs an explicit change contract, acceptance scenarios, allowed paths, and a fingerprint-bound implementation approval.
---

# AI SDLC Loop — Specification-Driven Development

`ai-sdlc-loop-sdd` is the Loop-native SDD entry point. It writes the same
bounded, fingerprinted TOON specification as `ai-sdlc-loop-specify`; the latter
remains available for existing callers. Use the namespaced SDD skill in Loop
installations so it is present in every supported project profile.

For raw feature notes with an unresolved business approach, use
`ai-sdlc-loop-requirements-discovery` first. Use
`ai-sdlc-loop-requirements-review` when actors, rules, acceptance logic, or
dependencies are incomplete. Follow `steps/manifest.toon` in dependency order;
this skill never authorizes source mutation.

## Deterministic step selection

Use the sibling shared runtime `scripts/loop.py steps --skill ai-sdlc-loop-sdd
--phase <entrypoint>` with each completed ID as `--completed-step <id>`. Read
only `selected_paths` and `required_references`. The selector validates
dependencies and returns `authorizes_execution: false`; the generated
fingerprint still requires explicit Implement approval.
