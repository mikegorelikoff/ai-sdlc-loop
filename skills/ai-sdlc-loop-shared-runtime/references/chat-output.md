# Chat presentation guardrail

User-facing AI SDLC chat is table-first under the selected skill's local
`Chat Output Contract`. This does not replace that domain schema.

Use PASS for checked success, FAIL for executed failed checks, WARNING for
nonblocking limitations, BLOCKED for a missing prerequisite or rejected gate,
PENDING for unexecuted/unresolved work, and N/A for an explicitly inapplicable
check. Preserve native domain states (proposed, accepted, ready, leased) in
their own columns. Completed review work can leave delivery BLOCKED.

Read only `references/chat-output.toon` for the selected skill. Render verified
facts with the sibling `scripts/chat_output.py render --skill-root <skill>
--input <chat-result.toon>`; check a draft with `check --skill-root <skill>
--response <response.md>`. CLI machine outputs remain native. The helper
never executes commands, collects evidence, changes state or grants approval.

Use at most six columns and eight preview rows per semantic table. Put
blocking/severe items first using source evidence, then preserve dependency
order or stable IDs. For overflow, show the full total and a full-artifact
reference; summarize blocking totals in the decision. Never omit the existence
of blockers. Keep cells within 180 characters by summarizing and linking; do
not silently truncate facts. Omit empty secondary/action tables. A no-findings
result names the reviewed scope and its limits instead of inventing a row.

Clarifications use local missing-input columns and an owned next-action row;
use host question tools where available. Native commands, patches, TOON, configuration,
code and commit messages keep their original syntax in fenced blocks or
linked artifacts. A request for only a native artifact overrides chat framing.
Do not dump machine journals or repeat tables as prose.

Repair only evaluator failures: baseline, then at most three iterations. Keep
failed response captures and codes; if unresolved, report BLOCKED and its
evidence. Structural validity does not establish truthful content or semantic
readiness. Distinguish simulated response tests from live agent executions.
