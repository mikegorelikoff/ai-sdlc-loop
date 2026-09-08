# Clarify raw requirements

## Goal

Turn rough feature or task notes into a problem brief, business alternatives
and questions that stakeholders can answer to choose a direction.

## When to use it

Use this before Specify when the request is unclear or a suggested solution
needs comparison with other ways to meet the business need. If the direction is
already accepted, use the requirements-review skill for delivery gaps.

## Prerequisites

- A current source installation containing `ai-sdlc-loop-requirements-discovery`.
- The raw request or notes. Past tickets, policies and previous decisions help
  when available; a finished PRD is unnecessary.

## Procedure

Ask the agent:

```text
Use ai-sdlc-loop-requirements-discovery --quick-flow.
Analyze these raw feature requirements: <paste the request>.
Compare business options using the available past decisions: <source paths>.
Prepare stakeholder questions and explain where and how to obtain the answers.
```

The assistant separates evidence, assumptions and contradictions; compares
business options and the limits of historical precedents; and prepares questions
with an owner role, priority, evidence method and decision consequence.

For example, a request for bulk approval may lead to comparing better assignment
with a limited batch pilot. The process owner can confirm policy exceptions;
an analyst can inspect timestamps to determine where waiting occurs. Each
answer changes which option is viable.

Use `--full-flow` for a more thorough evidence and question pass. Missing
stakeholder replies remain unresolved decisions. To retain the packet, ask to
save it for a named feature; Loop uses
`.ai-sdlc-loop/<feature>/requirements-discovery.toon`.

The assistant uses `scripts/requirements_discovery.py` inside its installed
skill: `prepare` binds raw files or a fixed stdin snapshot to source IDs and
digests; `scaffold` creates a draft with an explicit date; `validate` checks the
completed analysis; `finalize` creates canonical TOON; and `verify` detects
source drift or report changes. The model fills the draft. The helper owns the
final report.

Commands emit to stdout by default. `--write` persists only canonical feature
files; `--replace` permits replacement after reviewing an existing differing
output. Identical inputs and date give identical bytes. Neither hashing nor
schema validation proves the business judgment is correct.

## Verify

Check that each option has evidence or is explicitly hypothetical, and every
important question names a stakeholder role, an evidence location/method and
the decision its answer affects. Unknown historical outcomes must remain unknown.
Packet completion and acceptance of a business choice are separate statuses.

Require a passing `validate` result before finalization and a passing `verify`
result for a saved report. Missing source references, uncovered material gaps
or options, incomplete questions and unsupported acceptance records must fail.

## Troubleshooting

If prior cases cannot be found, supply a ticket or decision-log location or
continue with labeled hypotheses. Resolve conflicting policies with their
accountable owner. Drafted questions are not sent automatically.

For stale sources, prepare a new context and update the draft's analysis and
evidence references before finalizing again. Narrow oversized source sets
instead of truncating them. Preserve differing existing reports until reviewed.

## Next step

Use `ai-sdlc-loop-requirements-review` to check the selected direction, then
follow [Deliver a first change](first-change.md) to specify the accepted scope.
