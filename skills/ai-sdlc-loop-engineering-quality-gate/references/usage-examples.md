# Engineering quality gate usage examples

These examples assume a Loop project installation under `.agents/skills/`.
Replace only repository-relative feature, request, base, draft, and output paths.
Do not copy an example verdict or fingerprint into a real review.

## Example 1 — Python service correctness fix

The accepted `invoice-retry` implementation changes `src/billing/` and its
tests. The current Implement receipt is approved for those paths. Review the
retry state transition against nearby service implementations, fix a seeded
High duplicate-charge defect, and rerun the focused unit test before the full
billing suite.

```sh
python3 .agents/skills/ai-sdlc-loop-shared-runtime/scripts/loop.py \
  --project-root . implement-check --feature invoice-retry
python3 .agents/skills/ai-sdlc-loop-engineering-quality-gate/scripts/engineering_quality_gate.py \
  context --root . --feature invoice-retry \
  --request "Make invoice retries idempotent after a provider timeout" \
  --base HEAD --max-candidates 5 \
  --output .ai-sdlc-loop/invoice-retry/quality-context.toon --full-flow
```

Inspect 2–5 ranked billing/service/test examples, create findings before the
fix, and record actual checks such as:

```yaml
- command: [python3, -m, unittest, tests.billing.test_invoice_retry]
  phase: before_fix
  status: fail
- command: [python3, -m, unittest, tests.billing.test_invoice_retry]
  phase: after_fix
  status: pass
- command: [python3, -m, unittest, discover, -s, tests/billing]
  phase: final
  status: pass
```

Regenerate `quality-context.toon` after the fix, prepare
`.ai-sdlc-loop/invoice-retry/quality-draft.toon`, then finalize and verify:

```sh
python3 .agents/skills/ai-sdlc-loop-engineering-quality-gate/scripts/engineering_quality_gate.py \
  finalize --root . \
  --context .ai-sdlc-loop/invoice-retry/quality-context.toon \
  --draft .ai-sdlc-loop/invoice-retry/quality-draft.toon \
  --output .ai-sdlc-loop/invoice-retry/quality-gate.toon
python3 .agents/skills/ai-sdlc-loop-engineering-quality-gate/scripts/engineering_quality_gate.py \
  verify --root . \
  --report .ai-sdlc-loop/invoice-retry/quality-gate.toon
```

Expected decision: `PASS` when the defect is fixed, no finding remains, the
post-fix context is current, and all required checks pass.

## Example 2 — TypeScript repository-fit finding

The `profile-email` implementation adds validation in a controller even though
neighboring controllers delegate to an existing schema/service pattern. The
approved scope includes `src/profile/` and `test/profile/`.

```sh
python3 .agents/skills/ai-sdlc-loop-shared-runtime/scripts/loop.py \
  --project-root . implement-check --feature profile-email
python3 .agents/skills/ai-sdlc-loop-engineering-quality-gate/scripts/engineering_quality_gate.py \
  context --root . --feature profile-email \
  --request "Validate and persist a user's changed email address" \
  --base HEAD --output .ai-sdlc-loop/profile-email/quality-context.toon \
  --quick-flow
```

Compare the changed controller with nearby profile and account controllers,
their shared validation schema, service error contract, and Vitest tests. Record
the duplicated validation as a Medium `repository-fit` finding before editing.
If reuse of the existing schema is localized, fix it and add the missing
negative behavior test in the existing framework. Run focused typecheck and
Vitest targets before any repository-required broad check, then rerun relevant
checks after the fix.

Expected decision: `PASS_WITH_FINDINGS` is permitted only if any remaining
finding is explicitly non-blocking and all required available checks pass.
Opinion-only style preferences do not justify source edits.

## Example 3 — Fix blocked by Loop scope

The `provider-timeout` change exposes a High retry race. The correct fix also
requires `src/shared/idempotency.ts`, but the current `spec.toon` allows only
`src/providers/acme/` and `test/providers/acme/`.

Run context and review as usual with `--feature provider-timeout`, but do not
edit the shared file or broaden `allowed_paths`. Preserve the finding as:

```yaml
id: QG-001
severity: high
category: correctness
file: src/providers/acme/client.ts
blocking: true
resolution: remaining
fix: ""
reason_not_fixed: The evidence-backed fix requires src/shared/idempotency.ts, which is outside the current Loop allowed_paths.
```

Record verification truthfully even when focused tests pass; passing tests do
not erase the unresolved race. Finalize a `FAIL` report with
`ready_for_next_stage: false` and a blocking reason that requests a separately
approved specification/scope update. Do not route to Verify until a new current
Implement receipt authorizes the required path, the fix is applied, context is
regenerated, and checks pass.
