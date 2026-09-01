# Validate — Engineering Quality Gate

> Executable checkpoint: validate

## Entry

A post-fix context artifact and TOON draft exist. All attempted fixes and checks
are represented; no required evidence lives only in conversational prose.

## Procedure

1. Read `references/report-schema.toon`. Finalize the draft atomically:

   ```sh
   python3 <skills-root>/ai-sdlc-loop-engineering-quality-gate/scripts/engineering_quality_gate.py \
     finalize --root . \
     --context .ai-sdlc-loop/<feature>/quality-context.toon \
     --draft <repository-relative-draft.toon> \
     --output .ai-sdlc-loop/<feature>/quality-gate.toon
   ```

2. Verify the canonical report against the current repository state:

   ```sh
   python3 <skills-root>/ai-sdlc-loop-engineering-quality-gate/scripts/engineering_quality_gate.py \
     verify --root . \
     --report .ai-sdlc-loop/<feature>/quality-gate.toon
   ```

3. Treat helper rejection as blocking. Do not hand-edit the canonical report,
   copy an old fingerprint, weaken a decision, or leave a partial output.
4. Confirm stable unique IDs and ordering, repository-relative contained paths,
   non-empty evidence, current context/change identity, truthful verification,
   consistent `status` and `ready_for_next_stage`, and a valid
   `report_fingerprint`.
5. Enforce the decision policy:
   - `PASS`: no remaining finding or verification gap and every required check
     passed;
   - `PASS_WITH_FINDINGS`: only explicit non-blocking findings remain, every
     required check passed, optional unavailable gaps are explicit, and
     readiness is supported by evidence;
   - `FAIL`: any unresolved High, blocking Medium, failed required check,
     required check that should have run but is `not_run`, stale fingerprint,
     authority/scope/preservation failure, or decision inconsistency.
   An unavailable check must state why and may only describe an optional kind
   for which the repository exposes no applicable command/source. An applicable
   command blocked by authority or environment is `not_run`; every required
   `not_run` or `unavailable` result keeps readiness false.
6. Quality scores are optional. When present, every score must cite concrete
   repository or executable evidence. Never produce an opinion-only number.
7. Render a concise human report in the active response as YAML with this
   practical shape:

   ```yaml
   status: PASS | PASS_WITH_FINDINGS | FAIL
   summary: concise evidence-based assessment
   repository_profile:
     representative_examples: []
     applicable_patterns: []
   findings_fixed: []
   remaining_findings: []
   verification: []
   change_scope:
     files_changed: 0
     lines_added: 0
     lines_removed: 0
     new_dependencies: []
     unrelated_changes: []
   quality_evidence:
     repository_consistency: []
     correctness: []
     testing: []
     simplicity: []
   final_decision:
     ready_for_next_stage: false
     blocking_reasons: []
   ```

   Mirror canonical facts and exact command outcomes. Do not persist this human
   rendering as a second durable report.

## Exit

Return a helper-verified canonical TOON report, current fingerprints, final
status/readiness, exact verification outcomes, and concise human YAML. If the
finalize or verify action fails, status cannot be `PASS` and the next stage is
blocked.
