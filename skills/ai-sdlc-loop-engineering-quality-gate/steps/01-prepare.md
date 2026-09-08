# Prepare — Engineering Quality Gate

> Executable checkpoint: preflight

## Entry

A completed implementation, requested change or accepted specification, Git
review target, repository root, and optional base revision are available. The
gate may be called directly, but direct invocation grants no write authority.

## Procedure

1. Resolve the Git worktree and the applicable repository instructions. Reject
   a non-Git target, unsafe root, escaping path, or ambiguous review boundary.
2. Read the requested change or accepted specification, current `git status`,
   diff summary, changed-path list, and exact diff. Separate tracked, staged,
   unstaged, and untracked state so unrelated work can be preserved.
3. Select one flow mode. `--full-flow` wins when both flags are present.
   Quick flow may reduce breadth, but it cannot weaken authority, evidence,
   determinism, fix policy, verification truthfulness, or readiness gates.
4. For a routed Loop run, require `--feature <slug>` and locate
   `.ai-sdlc-loop/<feature>/spec.toon` plus
   `.ai-sdlc-loop/<feature>/approvals/implement.toon`. Run:

   ```sh
   python3 <skills-root>/ai-sdlc-loop-shared-runtime/scripts/loop.py \
     --project-root . implement-check --feature <feature>
   ```

5. Treat the current `spec.toon` `allowed_paths` as the maximum remediation
   boundary. Do not edit a path merely because it is already changed. If the
   receipt is missing, rejected, stale, mismatched, or the feature is omitted,
   continue only as a read-only review and record the authority blocker.
6. Record a baseline sufficient to prove that unrelated tracked, staged,
   unstaged, and untracked bytes remain unchanged. Do not stage or normalize
   unrelated files.
7. Distinguish source-mutation authority from command authority. Implement
   approval does not authorize arbitrary command execution, escalation, a
   commit, network access, or a new dependency.
8. Choose repository-relative TOON paths. For routed Loop use
   `.ai-sdlc-loop/<feature>/quality-context.toon` and
   `.ai-sdlc-loop/<feature>/quality-gate.toon`.

## Execution contract

Do not use it before a bounded implementation diff and accepted change contract exist. Use `ai-sdlc-loop-specify` or the owning implementation workflow instead. Do not use it only to execute an already defined check list. Use `ai-sdlc-loop-validation` instead.

Read the [shared execution decisions](../../ai-sdlc-loop-shared-runtime/references/execution-contract.md) once for this invocation.
Apply its required/discoverable/inherited/optional input rules to this step's
declared inputs. Record the source and status of material facts, then validate
the owning output contract and current evidence before completion.

## Exit

Return the exact review target, request/spec evidence, flow mode, changed-path
boundary, Implement eligibility, approved paths, unrelated-work baseline, and
artifact paths. Block mutation unless current Implement authority and path
containment are proven.

## Chat presentation

Before a result, warning, blocker or question, apply the local [chat schema](../references/chat-output.toon) and the Chat Output Contract in `SKILL.md`. Preserve native artifact and tool-input formats.
