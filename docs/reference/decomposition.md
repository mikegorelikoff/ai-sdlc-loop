# Hierarchical delivery decomposition

Use `ai-sdlc-loop-hierarchical-decomposition` to turn sourced initiative, Epic or Story scope into the
smallest safe outcome hierarchy. It is a five-step utility: prepare, context,
execute, validate, handoff. Existing lifecycle state and implementation approvals
remain owned by their established skills.

| Contract | Behavior |
| --- | --- |
| Inputs | Explicit UTF-8 source snapshots, scope, input level, target level |
| Machine state | Versioned canonical TOON candidate and recomputed report |
| Identity | SHA-256 of stable scope/type/key; titles and input order do not change identity |
| Unknowns | Block affected descendants; never invent precision |
| Reviews | Independent Product, Delivery, Architecture and QA receipts |
| Repair | Three candidates maximum; only affected branches change |
| Outputs | Semantic tables, traceability, acceptance and sourced branch handoff |
| Side effects | Explicit root-bounded artifact writes only; no tickets or source execution |

## Commands

Run help from the source checkout:

```bash
python3 skills/ai-sdlc-loop-hierarchical-decomposition/scripts/decompose.py --help
```

`prepare` snapshots a source and leaves semantic decisions unresolved. `evaluate`
validates a supplied candidate and returns exit 3 for a valid blocked report.
`fingerprint` emits current branch identities for review. `verify` rechecks source
bytes and recomputes saved results. `render` produces the chat preview. `handoff`
exports a passing branch without granting execution authority. `verify-handoff`
checks the packet against its recomputed report and current source bytes before
a downstream skill consumes it. All paths use
explicit `--root`, `--input` and optional `--output`; prepare also requires
`--scope` and `--input-level`. Input defaults never guess product requirements.

## Integration

Requirements review supplies source authority and missing decisions. Backlog or
Specify consumes the verified branch, preserving ancestor WHY, requirement IDs,
AC and dependency evidence. Implementation planning owns file/task decisions;
verification owns executed results. Jira issue mappings remain an external,
explicitly authorized consumer rather than an automatic write.

## Limits

Structural evaluation does not prove semantic source completeness or independent
reviewer identity. The included corpus uses labeled property fixtures and actual
compiler execution, not a live provider benchmark. No numeric quality scores,
estimates or critical path are invented without supporting data.
