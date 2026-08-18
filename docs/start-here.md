# Start here

This is the canonical first-run path for AI SDLC Loop.

## Install

From the project that should receive the skills, run one command:

```sh
curl -fsSL https://raw.githubusercontent.com/mikegorelikoff/ai-sdlc-loop/v0.2.0/install.sh | sh -s -- codex-project
```

Then verify separately:

```sh
python3 .ai-sdlc-loop/install/install.py verify codex-project
```

Claude Code projects use `claude-code-project`. Another compatible agent uses `agent-project --skills-root .agent/skills`.

## Run the first loop

Ask the agent to use `ai-sdlc-loop-flow` for a bounded repository change. Provide the intended outcome and relevant paths. The agent should:

1. create a deterministic specification and fingerprint;
2. request approval before implementation;
3. keep changes inside the approved paths;
4. run explicit verification commands;
5. request a separate approval before committing.

## Expected result

The selected project skill root contains 19 `ai-sdlc-loop-*` directories. Local workflow state appears below `.ai-sdlc-loop/<feature>/` and durable machine artifacts use TOON.

## If installation stops

Loop fails closed on unsafe roots, symlink escapes, occupied unmanaged targets, or drifted managed skills. Read the reported path, preserve local edits, and resolve the conflict before retrying.

Continue with [How it works](how-it-works.md).
