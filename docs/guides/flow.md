# Guide: use guided Flow

## Goal

Select one current Loop owner without guessing skill order or broadening authority.

## When to use it

Use Flow for a new request, ambiguous next step, or full-flow handoff review.

## Prerequisites

Loop is installed; the intent and lowercase kebab-case feature slug are known.

## Procedure

Run Explore through the installed `flow.py` with `--intent`, `--feature`, and the appropriate rigor flag. Save the TOON card only when a later Apply is needed. Review it, then run Apply against the same repository. `--execute --approve` confirms only the handoff selection.

## Verify

The Apply artifact uses `ai-sdlc-loop-flow-apply/v1`, matches the decision fingerprint, selects one owner, and reports `owner_action_executed: false`.

## Troubleshooting

`FLOW_ROUTE_DRIFT` means intent, evidence, route, or owner files changed. Run Explore again. A missing owner requires installation repair, not an implicit fallback.

## Next step

Follow the selected owning skill and honor every downstream approval gate.
