# AI SDLC Loop

**Ship a bounded change through Specify → Implement → Verify with explicit approval before code mutation and commit.**

[![CI](https://github.com/mikegorelikoff/ai-sdlc-loop/actions/workflows/ci.yml/badge.svg)](https://github.com/mikegorelikoff/ai-sdlc-loop/actions/workflows/ci.yml)
[![Docs](https://github.com/mikegorelikoff/ai-sdlc-loop/actions/workflows/docs.yml/badge.svg)](https://mikegorelikoff.github.io/ai-sdlc-loop/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

AI SDLC Loop is the focused delivery member of the AI SDLC product family. It installs a guided Flow, an installation Doctor, a fixed stage workflow, eleven proven delivery-control skills, and one shared runtime while keeping deterministic TOON specs, reviews, approvals, QA plans, evidence, release decisions, and promotion artifacts in the local project.

## Why use it?

- Guided Flow, read-only Doctor, five stage entrypoints, eleven delivery-control skills, and one shared standard-library runtime.
- Explicit Implement and commit approvals tied to current fingerprints.
- Bounded paths, local evidence, secret redaction, and no runtime network or telemetry.
- Versioned artifacts that can be promoted into AI SDLC Harness workflows.

## Quick start

Install for a Codex project with one shell command:

```sh
curl -fsSL https://raw.githubusercontent.com/mikegorelikoff/ai-sdlc-loop/v0.2.0/install.sh | sh -s -- codex-project
```

Then verify separately:

```sh
python3 .ai-sdlc-loop/install/install.py verify codex-project
```

For a local checkout, use `python3 install.py codex-project`. Claude Code uses `claude-code-project`; another compatible agent uses `agent-project --skills-root .agent/skills`.

## Expected result

The installer contributes 18 working `ai-sdlc-loop-{slug}` skills and `ai-sdlc-loop-shared-runtime`, for 19 installed directories. Each skill has a canonical `steps/manifest.toon` and bounded step documents. Existing unrelated skills remain untouched. The TOON install record and reusable verifier are written below `.ai-sdlc-loop/install/`. See the generated [skill catalog](https://mikegorelikoff.github.io/ai-sdlc-loop/reference/skills/) for the exact inventory.

## Workflow

Ask the agent to use `ai-sdlc-loop-flow` for guided Explore and Apply, or `ai-sdlc-loop-orchestrate` when the required stage is already clear:

1. Specify the request and allowed paths, then show a stable fingerprint.
2. Request explicit approval before Implement.
3. Make only the approved bounded change.
4. Verify with explicit commands and persist redacted evidence.
5. Request a separate approval before any commit.

The CLI contract is available with:

```sh
python3 .agents/skills/ai-sdlc-loop-shared-runtime/scripts/loop.py --help
```

## Scope

Loop controls a small local delivery cycle. It does not reduce or cap model requests, replace human review, provide hosted orchestration, or automatically push, release, deploy, or open pull requests.

## Documentation

- [Start here](https://mikegorelikoff.github.io/ai-sdlc-loop/start-here/) for installation and the first run.
- [How it works](https://mikegorelikoff.github.io/ai-sdlc-loop/how-it-works/) for lifecycle, authority, and evidence.
- [Reference](https://mikegorelikoff.github.io/ai-sdlc-loop/reference/) for exact profiles, skills, commands, and formats.
- [Project](https://mikegorelikoff.github.io/ai-sdlc-loop/project/) for status, limitations, security, and governance.

## Harness compatibility

`promote` emits `ai-sdlc-harness-promotion/v1` TOON while preserving request, allowed paths, trace IDs, fingerprints, approvals, state, commands, and evidence. Consumers must reject unsupported schema versions.

## Security and privacy

Runtime state is local, commands run without a shell, paths are contained, and common secret patterns are redacted before evidence is persisted. Review [SECURITY.md](SECURITY.md) before using Loop with sensitive repositories.

## Status

The public API is experimental until the first stable release. Schema changes require a new version and migration notes.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache License 2.0. See [LICENSE](LICENSE).
