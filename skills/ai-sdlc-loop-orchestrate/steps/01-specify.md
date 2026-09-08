# Specify route

## Entry

A bounded repository change is requested.

## Procedure

Load `ai-sdlc-loop-specify`, follow its manifest, and return its exact spec fingerprint for human review.

## Execution contract

Route a bounded repository change through the fixed Loop lifecycle; do not substitute orchestration for the owning stage or its approval gates.

Read the [shared execution decisions](../../ai-sdlc-loop-shared-runtime/references/execution-contract.md) once for this invocation.
Apply its required/discoverable/inherited/optional input rules to this step's
declared inputs. Record the source and status of material facts, then validate
the owning output contract and current evidence before completion.

## Exit

Stop before source mutation. The next owner is `ai-sdlc-loop-implement` only after explicit approval.
