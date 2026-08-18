---
name: ai-sdlc-loop-doctor
description: Diagnose an AI SDLC Loop installation and preview a safe package upgrade plan using deterministic, read-only TOON evidence.
---

# AI SDLC Loop Doctor

Use this skill when installation verification fails, installed skills drift, runtime requirements are uncertain, or a maintainer needs to compare an installed package with a candidate package before approving an upgrade.

## Contract

1. Diagnostics are read-only and emit `ai-sdlc-loop-doctor-report/v1`.
2. Check Python, Git, install record, profile, exact inventory, digests, step manifests, and shared runtime.
3. Every failed check includes remediation text but Doctor never executes it.
4. Upgrade planning compares current installed content with a local candidate package and emits `ai-sdlc-loop-upgrade-plan/v1`.
5. Doctor never installs, replaces, removes, or repairs files and never broadens host authority.

## Usage

```sh
python3 scripts/doctor.py check --project-root . --profile codex-project
python3 scripts/doctor.py upgrade-plan --project-root . --profile codex-project --package-root /path/to/ai-sdlc-loop
```

Resolve the active procedure through `steps/manifest.toon`. Durable machine output is TOON.

## Step selector

| Step | Procedure |
| --- | --- |
| `preflight` | [`steps/01-prepare.md`](steps/01-prepare.md) |
| `context` | [`steps/02-context.md`](steps/02-context.md) |
| `execute` | [`steps/03-diagnose.md`](steps/03-diagnose.md) |
| `validate` | [`steps/04-validate.md`](steps/04-validate.md) |
| `handoff` | [`steps/05-handoff.md`](steps/05-handoff.md) |
