# Validate and Handoff — ai-sdlc-loop-shared-runtime: Portable Helper Dependency

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

For user-facing chat, use this skill’s Chat Output Contract. Preserve the
owning artifacts, exact validation evidence, scope and unresolved risks.

Quality gate:

- Pass when the canonical runtime inventory is complete and an installed
  downstream helper imports and executes successfully.
- Fail when inventory exists but imports fail, the runtime is installed under a
  different root, package files are inconsistent, or verification mutates real delivery
  artifacts.

## Examples

Valid diagnosis:

```text
The SDD helper cannot import ai_sdlc_artifact_helper because the shared runtime
package is absent. Reinstall the complete pinned package, then rerun --help.
```

Invalid diagnosis:

```text
Copy one module from an arbitrary checkout into the installed package and keep
working.
```

Reject the invalid path because it bypasses package provenance and can mix
incompatible runtime bytes.

## Edge Cases

- Source and installed layouts use the same runtime package contract; only the
  skills-root prefix differs.
- A project may expose host-specific symlinks, but all selected skill folders
  and the runtime must resolve to compatible bytes.
- Installing only one downstream skill without this dependency is incomplete.
- `--help` proves importability, not correctness of a consumer feature; run the
  downstream workflow's own validation for that claim.

## Scope Boundary

This skill verifies the portable runtime dependency. It does not select product
work, approve network access, change policy, implement features, repair Git,
publish releases, or mutate authoritative lifecycle evidence.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.

## Chat presentation

Present the result using the owning `SKILL.md` Chat Output Contract and local [chat schema](../references/chat-output.toon). The machine handoff remains native; show its decision, evidence and owned action without dumping the journal.
