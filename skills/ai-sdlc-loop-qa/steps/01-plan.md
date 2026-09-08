# Plan

## Entry

Read the active specification, changed-path boundary, acceptance criteria, and existing validation evidence. Separate confirmed facts from assumptions.

## Procedure

Rank risks by user impact, security impact, data loss, regression likelihood, and operational cost. Define observable acceptance scenarios and existing behavior that must remain stable. Use `references/qa-plan.md` as the quality gate.

## Execution contract

Plan observable acceptance and inspect current evidence; use test-cases for scenario detail and Verify for executed command readiness.

Read the [shared execution decisions](../../ai-sdlc-loop-shared-runtime/references/execution-contract.md) once for this invocation.
Apply its required/discoverable/inherited/optional input rules to this step's
declared inputs. Record the source and status of material facts, then validate
the owning output contract and current evidence before completion.

## Exit

Return a bounded QA scope with explicit evidence gaps and owners.
