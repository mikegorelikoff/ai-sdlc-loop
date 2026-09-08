# Handoff — ai-sdlc-loop-hierarchical-decomposition

## Entry

The manifest prerequisites are satisfied and this owning node is selected.

## Procedure

Render the verified artifact with `render --root <project> --input <decomposition.toon>`.
Link the full artifact alongside the bounded chat preview. Empty tables are omitted.
Use `handoff --root <project> --input <decomposition.toon> --node <key> --output <handoff.toon>`
for a passing branch. Consumers run `verify-handoff --root <project> --input <handoff.toon>
--report <decomposition.toon>` before using the packet; forged or stale content fails. The packet carries ancestors, source evidence, requirement
mapping, acceptance, dependencies, assumptions and unknowns; it authorizes no action.

Requirements readiness consumes unresolved questions and sourced scope. Backbone
backlog planning consumes the hierarchy for owner/estimation/release work; SDD consumes
a reviewed Story packet to design implementation. Loop Specify consumes the same
packet before its normal scope and approval gates. Jira planning may map stable IDs
to external issue keys offline; never create or update issues in this skill.
Implementation planning preserves Story→Task→AC links. Verification consumes AC
and expected outcomes; proposed verification is not an executed test result.

Keep reports beside feature refinement context (`specs-refiniment/<feature>/` in
Backbone; an explicit feature evidence path in Loop). Derived human reports do not
replace canonical lifecycle Markdown or its OKF owning writer. This utility does
not modify state.toon, mark readiness or bypass an owning handoff contract.

## Exit

Return the declared evidence or explicit blocker; do not improvise authority.

The owning coordinator emits its journal-backed `ai-sdlc-handoff/v2` with `result`,
`blockers`, `next_required` and `next_optional`. Each action records reason, command
and expected_artifact. The decomposition packet is evidence attached to that handoff,
not a substitute for the coordinator journal or execution authorization.
