# Validate and Handoff — ai-sdlc-loop-branching: Branching

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

For user-facing chat, use this skill’s Chat Output Contract. Preserve the
owning artifacts, exact validation evidence, scope and unresolved risks.

Quality gate:

- Pass when implementation starts on a branch that matches the task type and,
  for medium or large work, includes the active spec slug.
- Fail when repo-tracked files are mutated on a shared/default branch, unrelated
  dirty files are carried silently, branch/spec mismatch is hidden, or Git
  command failures are ignored.

## Examples

Valid medium-work start:

Chat example: use the normal, warning and blocked examples in
`references/chat-examples.md`; their evidence comes from explicit scenario fixtures.

Invalid counter-example:

```text
Edited files directly on the shared base and will make a branch later.
```

Reject this because branch verification must happen before repo-tracked file
mutation for implementation work.

## Edge Cases

- If the repository has no declared/present base branch, stop and ask the owner
  to declare one; do not invent `dev`.
- If already on a correctly named task branch, continue and report `already
  correct`.
- If already on a non-default branch that clearly belongs to the same task,
  report `reused with reason`; do not create a second branch.
- For new task branches, do not skip checkout/pull of the resolved base merely
  because it looks recent.
- If `git pull --ff-only` reports divergence, stop and ask for repository
  maintenance instead of merge-committing during task setup.
- If the branch name matches multiple specs or no spec for medium or large work,
  resolve the active bounded specification with `ai-sdlc-loop-specify` before implementation.
- If unrelated dirty files exist, do not run destructive cleanup. Ask the user
  whether to keep, commit, stash, or otherwise handle them.
- If branch creation fails from sandboxing, request escalation rather than
  inventing an alternate branch state.
- Do not push branches unless the user explicitly asks or the commit workflow
  requires it.

## Scope Boundary

- Do not create or update bounded specification artifacts; use `ai-sdlc-loop-specify`.
- Do not decide validation commands; use `$ai-sdlc-loop-validation`.
- Do not stage files or create commits; use `$ai-sdlc-loop-commit-prep`.
- Do not draft commit messages; use `$ai-sdlc-loop-conventional-commit`.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.

## Chat presentation

Present the result using the owning `SKILL.md` Chat Output Contract and local [chat schema](../references/chat-output.toon). The machine handoff remains native; show its decision, evidence and owned action without dumping the journal.
