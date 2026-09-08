# Authorize commit

## Entry

Current verification passed and the user requested a commit.

## Procedure

Use `ai-sdlc-loop-commit-prep` to establish the exact boundary and `ai-sdlc-loop-conventional-commit` to validate the message. Show the verified fingerprint and exact commit boundary. After separate explicit approval, run `approve --action commit`. Never infer approval from Implement.

## Execution contract

Use only for an explicit commit with current verification and separate commit approval; use commit-prep for readiness and conventional-commit for message content.

Read the [shared execution decisions](../../ai-sdlc-loop-shared-runtime/references/execution-contract.md) once for this invocation.
Apply its required/discoverable/inherited/optional input rules to this step's
declared inputs. Record the source and status of material facts, then validate
the owning output contract and current evidence before completion.

## Exit

Proceed only with a matching current receipt.
