# Handoff — Engineering Quality Gate

> Executable checkpoint: handoff

## Entry

The canonical report has passed the helper's current-state verification, or a
specific failed invariant is recorded. Do not infer completion from a draft,
pre-fix context, or conversational summary.

## Procedure

Assemble an `ai-sdlc-handoff/v2` result from terminal evidence. Include the
completed step IDs; canonical report path, context and report fingerprints;
status and `ready_for_next_stage`; fixed and remaining findings; exact command
outcomes; unresolved blockers; residual risks; current owner; and one next
required action.

Route to `ai-sdlc-loop-verify` only when the report is current, schema-valid,
helper-verified, and ready. Otherwise keep ownership with the engineering gate
and name the exact recovery: required clarification, authorized scoped fix,
failed check correction, unavailable environment, or context regeneration.

Keep optional Code Review, Security Testing, QA, and broader validation work
separate from required recovery. Never activate another skill automatically,
broaden paths or permissions, create approval, mark an unexecuted check passed,
stage, commit, publish, or conceal a failed gate.

## Exit

Return the evidence-backed human YAML and unambiguous handoff. The next owner
must be able to verify the canonical TOON rather than reconstructing state from
prose.

## Chat presentation

Present the result using the owning `SKILL.md` Chat Output Contract and local [chat schema](../references/chat-output.toon). The machine handoff remains native; show its decision, evidence and owned action without dumping the journal.
