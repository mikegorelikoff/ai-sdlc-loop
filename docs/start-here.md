# Start here

This is the canonical first-run path for AI SDLC Loop.

## Install

From the project that should receive the skills, run one command:

```sh
curl -fsSL https://raw.githubusercontent.com/mikegorelikoff/ai-sdlc-loop/v0.8.1/install.sh | sh -s -- codex-project
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
4. review the diff against repository patterns, fix safe significant findings,
   and produce a current engineering quality report;
5. run explicit verification commands;
6. request a separate approval before committing.

## Expected result

A current source-checkout installation contains 21 `ai-sdlc-loop-*`
directories; immutable `v0.1.1` retains its prior 17-member inventory. Local
workflow state appears below `.ai-sdlc-loop/<feature>/` and durable machine
artifacts use TOON. The quality gate writes its current report to
`.ai-sdlc-loop/<feature>/quality-gate.toon`.

## If installation stops

Loop fails closed on unsafe roots, symlink escapes, occupied unmanaged targets, or drifted managed skills. Read the reported path, preserve local edits, and resolve the conflict before retrying.

Continue with [How it works](how-it-works.md).
