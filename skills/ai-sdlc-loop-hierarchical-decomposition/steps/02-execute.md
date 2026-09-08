# Execute — ai-sdlc-loop-hierarchical-decomposition

## Entry

The manifest prerequisites are satisfied and this owning node is selected.

## Procedure

Follow [the local D/S/H contract](../SKILL.md#deterministic-execution-contract).
Read `references/execution.md` before creating a semantic candidate.
For each parent: identify the intended outcome and source obligations, choose
an outcome-oriented axis, propose minimal children, map requirements and NFRs,
then assess sibling overlap, parent coverage and granularity. Stop at configured
level or any blocking unknown. Retain stable keys when repairing a branch.

Run `evaluate --root <project> --input <candidate.toon> --output <decomposition.toon>`.
A valid blocked report exits 3 and is useful evidence. Invalid input exits 2 and
must not replace an existing artifact. Codes identify targeted repairs.

Run `fingerprint` on the candidate. Product, Delivery, Architecture and QA reviewers
independently review each node using current branch fingerprints. They must not
copy the generator's conclusions. Record actual evidence, assessment and action;
fixture review assertions are never production review receipts.

Baseline is iteration 1; repair affected branches at iterations 2 and 3 only.
Retain failed captures, semantic defects and unchanged branch identities. Refresh
only reviews invalidated by branch/source/dependency changes. Do not reduce gate
severity or reinterpret unresolved knowledge to force PASS.

## Exit

Return the declared evidence or explicit blocker; do not improvise authority.
