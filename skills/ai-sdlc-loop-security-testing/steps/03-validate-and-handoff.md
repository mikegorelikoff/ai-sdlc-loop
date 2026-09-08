# Validate and Handoff — ai-sdlc-loop-security-testing: Security Testing

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

For user-facing chat, use this skill’s Chat Output Contract. Preserve the
owning artifacts, exact validation evidence, scope and unresolved risks.

Quality gate:

- Pass when every finding is tied to a concrete path, exploit condition, impact, and fix.
- Fail when the output recites generic OWASP categories, cites standards from memory without verification, inflates speculative issues, omits severity, or hides missing validation.

## Examples

Finding example:

Chat example: use the normal, warning and blocked examples in
`references/chat-examples.md`; their evidence comes from explicit scenario fixtures.

Invalid counter-example:

```text
Security looks fine.
```

Reject this because it omits reviewed boundaries, findings status, and validation gaps.

## Edge Cases

- Stop and warn immediately if real secrets, bearer tokens, private keys, or production-only values appear in the diff; do not paste them back.
- State `target unclear` when no diff, endpoint, workflow, or subsystem is provided and local context cannot infer one safely.
- Use `$ai-sdlc-loop-code-review` when the main ask is correctness, regression, or maintainability rather than exploitability.
- If browsing or primary-source verification is unavailable, report `standards verification blocked` and limit the output to locally supported exploitability findings instead of presenting unverified OWASP guidance.
- Mark validation as blocked when required credentials, fixtures, or environment are unavailable.
- Do not lower severity because a path is "internal" unless the trust boundary proves only trusted callers can reach it.

## Scope Boundary

- Do not perform general code review unless security is the primary question.
- Do not run production attacks, live exploitation, or credentialed provider actions.
- Do not expose sensitive values in findings, tests, comments.
- Do not decide business acceptance; return requirement gaps to `ai-sdlc-loop-specify` and verification gaps to `ai-sdlc-loop-verify`.
- Do not cite OWASP categories, ASVS controls, or standards versions from memory when current-source verification is required.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.

## Chat presentation

Present the result using the owning `SKILL.md` Chat Output Contract and local [chat schema](../references/chat-output.toon). The machine handoff remains native; show its decision, evidence and owned action without dumping the journal.
