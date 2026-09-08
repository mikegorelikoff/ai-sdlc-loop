# Route structured findings

## Entry

Manifest prerequisites and the selected StepCard are satisfied.

## Procedure

Run handoff on the verified report. Send native findings to the recorded consumer. Related IDs preserve scenario-to-bug provenance; they do not auto-promote scope or grant approval. Unverified bugs and unknown omissions remain visible.

Read [execution](../references/execution.md) and use `scripts/hunt.py`.

## Exit

Return validated evidence or an explicit blocker; no lifecycle authority changes.

The invoking lifecycle owns ai-sdlc-handoff/v2, next_required and next_optional. Attach this validated report as evidence; do not replace the lifecycle handoff or change its approvals.
