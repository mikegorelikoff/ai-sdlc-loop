# Prepare the Loop commit handoff

## Entry

The user requested commit preparation and the active Loop feature is known.
A commit request permits preparation; the Commit stage still validates its
separate approval receipt for the verified fingerprint.

## Procedure

1. Read `git status --short --branch`, `git diff --stat` and
   `git diff --cached --stat`. Identify related and unrelated paths without
   staging or reverting them.
2. Run the sibling shared runtime's `loop.py evidence-check --feature <feature>`.
   This checks specification identity, executed passing commands, exact current
   changed files and current engineering quality evidence. A missing, failed,
   invalid or stale receipt blocks the commit handoff; return to Verify or the
   owning repair stage. Do not substitute a planned command list.
3. Run `scripts/check_commit_ready.py --allow-unstaged --no-require-staged`
   for Git preflight. These flags are for preparation before staging; they do
   not authorize committing unrelated paths.
4. If the task explicitly includes a Harness SDD package, pass its actual path
   with `--spec`; use `--task TNNN` only for an explicitly scoped completed task.
   Missing optional SDD context must not trigger creation of a second lifecycle.
   An unavailable SDD validator is an uncovered gate, never a passing check.
5. Use `ai-sdlc-loop-conventional-commit` to draft and validate the message from
   the actual diff and evidence. Do not invent task IDs or validation outcomes.
6. Return the exact proposed paths, excluded dirty work, message and verified
   fingerprint to `ai-sdlc-loop-commit`. That owner performs approval validation,
   staging, commit execution and post-commit checks.

## Exit

Complete preparation when current evidence and the proposed commit contents
are explicit. Do not run `git commit`, amend, push, tag or publish here. Return
one blocked handoff when a required gate fails, with the exact recovery action.

Apply [D/S/H](../SKILL.md#deterministic-execution-contract).
