# Validate and Handoff — ai-sdlc-loop-code-review: Code Review

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

For user-facing chat, use this skill’s Chat Output Contract. Preserve the
owning artifacts, exact validation evidence, scope and unresolved risks.

Quality gate:

- Pass when every finding has a path, severity, impact, and fix; no-finding reports still include validation gaps.
- Fail when the review starts with a summary, lists style nits as findings, omits spec comparison for medium/large work, or hides missing validation.

## Examples

Finding example:

Chat example: use the normal, warning and blocked examples in
`references/chat-examples.md`; their evidence comes from explicit scenario fixtures.

Invalid counter-example:

```text
Looks good. Nice cleanup.
```

Reject this because it is not findings-first and does not mention validation.

## Edge Cases

- State `target unclear` and ask for the review boundary when no diff, commit, branch, or subsystem is available.
- Keep docs-only review lightweight unless docs change SDD policy, API contracts, setup, security, or validation behavior.
- Use deep-audit mode only when the user asks for a broad pass or the surface spans multiple high-risk areas.
- Do not spawn subagents when the active runtime requires explicit permission and the user did not request delegation.
- Report stale validation when files changed after tests ran.
- Treat hook-driven review as advisory-first; warnings do not replace human-readable findings.

## Scope Boundary

- Do not edit code during review unless the user explicitly asks for fixes.
- Do not perform security-focused exploitability review as a side effect; use `$ai-sdlc-loop-security-testing`.
- Do not choose final validation commands except to identify gaps; use `$ai-sdlc-loop-validation`.
- Do not approve scope changes that are missing from `tasks.md`; require a spec update first.

## Hook Policy

- Skip automatic review for docs-only or metadata-only changes with no code, config, hook, spec-runtime, or test behavior impact.
- Require review for non-trivial production code, repo-local automation logic, config, hook, workflow, provider, transport, schema, or test changes.
- Recommend deep audit for high-churn surfaces, multiple risk categories, or changes spanning handlers, services, providers, and config.
- Keep hook enforcement advisory-first; emit warnings before hard blocks.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.

## Chat presentation

Present the result using the owning `SKILL.md` Chat Output Contract and local [chat schema](../references/chat-output.toon). The machine handoff remains native; show its decision, evidence and owned action without dumping the journal.
