# Project

## Status

AI SDLC Loop is experimental. The source tree is preparing `v0.2.0`; it adds
the mandatory engineering quality gate and twenty-member install inventory.
Immutable `v0.1.1` retains its prior inventory. Schema changes require a new
version and migration notes.

## Scope and limitations

Loop controls a small local delivery cycle. Deterministic context and report
fingerprints make evidence reproducible; they do not prove semantic
correctness. Loop does not reduce or cap model requests, authenticate reviewer
identity cryptographically, replace human review, provide hosted orchestration,
or automatically push, deploy, release, or open pull requests.

## Security and privacy

Runtime state is local, commands run without a shell, paths are contained, and common secret patterns are redacted before evidence is persisted. Review the repository [security policy](https://github.com/mikegorelikoff/ai-sdlc-loop/security/policy) before processing sensitive work.

## Governance

- [Release history](https://github.com/mikegorelikoff/ai-sdlc-loop/blob/main/CHANGELOG.md)
- [Contributing](https://github.com/mikegorelikoff/ai-sdlc-loop/blob/main/CONTRIBUTING.md)
- [License](https://github.com/mikegorelikoff/ai-sdlc-loop/blob/main/LICENSE)
- [Report a vulnerability](https://github.com/mikegorelikoff/ai-sdlc-loop/security/advisories/new)
- [Decision log](decision-log.md)
- [Roadmap](roadmap.md)

## AI SDLC product family

**Structure delivery. Control context. Measure adoption.**

Loop is independently installed and remains compatible with promotion into [AI SDLC Harness](https://github.com/mikegorelikoff/ai-sdlc-harness).
