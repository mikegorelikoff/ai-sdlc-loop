# Authorize implementation

## Entry

A current `spec.toon` fingerprint has been shown to the user.

## Procedure

Use `ai-sdlc-loop-approvals-sandbox` to classify any required command authority. After explicit approval, run `approve --action implement`, followed by `implement-check`. Missing, rejected, stale, or mismatched authority blocks mutation.

## Execution contract

Use only after implement-check accepts current approval; route the resulting diff to engineering-quality-gate. This stage does not authorize commit.

Read the [shared execution decisions](../../ai-sdlc-loop-shared-runtime/references/execution-contract.md) once for this invocation.
Apply its required/discoverable/inherited/optional input rules to this step's
declared inputs. Record the source and status of material facts, then validate
the owning output contract and current evidence before completion.

## Exit

Proceed only after the runtime prints `implement eligible` for the current fingerprint.
