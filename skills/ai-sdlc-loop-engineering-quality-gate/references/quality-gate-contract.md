# Engineering quality gate contract

## Core rule

Do not evaluate generated code in isolation. Decide whether it is the smallest
correct implementation for this repository using current repository evidence
and actually executed checks.

This skill owns a post-implementation gate that combines adversarial review,
authorized localized remediation, verification reruns, and one current delivery
decision. It does not replace a read-only code review, a security deep dive, or
the next-stage Loop Verify receipt.

## Required sequence

Perform these activities in order:

1. Bind the requested change to the current Git diff and approved Loop scope.
2. Build the smallest relevant deterministic context profile.
3. Select and inspect 2–5 comparable repository implementations where
   practical, or record evidence for the shortfall.
4. Infer only repository-supported architecture, validation, error, naming,
   testing, mocking, dependency, and layer conventions.
5. Review the implementation adversarially and record the complete typed
   finding set before mutation.
6. Detect repository-owned verification and run the smallest relevant allowed
   checks first.
7. Fix evidenced High and safe localized Medium findings only when the current
   Loop Implement receipt and `allowed_paths` authorize every edit.
8. Rebuild context against the post-fix diff and rerun relevant checks.
9. Finalize and current-state verify the canonical report, then render concise
   human YAML from the same facts.

Do not reorder the sequence to make a clean result easier to obtain. A report
created before the last source change is stale.

## Inputs and authority

Required review inputs are one requested change or accepted specification, one
Git repository, and one current diff or explicit base revision. Repository
instructions, requirements, acceptance criteria, design, tasks, and tests are
evidence when present.

For AI SDLC Loop:

- routed use requires `--feature <slug>`;
- `.ai-sdlc-loop/<feature>/spec.toon` defines the request fingerprint and
  maximum `allowed_paths`;
- `.ai-sdlc-loop/<feature>/approvals/implement.toon` must be a current matching
  approval before any gate fix;
- `implement-check` must succeed immediately before remediation;
- direct invocation, a finding, or this contract never grants write authority;
- Implement approval does not authorize command escalation, dependency
  installation, staging, commit, publication, or broader paths.

When authority is absent, complete a read-only review, preserve findings, and
set readiness according to their blocking state. Never guess or self-approve.

The standard `--state-check` flag is accepted as a compatibility boundary, but
this helper does not advance Loop state. `--begin-state` and `--complete-state`
are rejected; the Loop orchestrator owns stage transitions.

## Deterministic context

Use `scripts/engineering_quality_gate.py context` for the bounded profile. The
stable context contract is `ai-sdlc-engineering-quality-gate-context/v1` and is
defined in `context-schema.toon`.

The context includes the normalized request and flow mode; optional Loop
feature/spec identity; resolved Git base and head; sorted changed-file records;
computed file/line scope; sorted repository instruction sources; bounded
2–5 candidate examples; detected verification candidates; a change fingerprint;
and a context fingerprint.

The implementation diff must be non-empty. Durable artifacts use only
`.ai-sdlc-loop/<feature>/` and the canonical names `quality-context.toon`,
`quality-gate-draft.toon`, and `quality-gate.toon`. The scanner excludes that
Loop state, but does not hide same-named implementation files elsewhere.
Changed regular-file identity includes content and canonical Git mode
(`100644` or `100755`). Repository configuration symlinks are not command
evidence, and case aliases for one configuration file emit one command. A dirty
nested Git worktree requires its own gate before a parent review can bind the
clean Git-link revision.

Apply these determinism rules:

- use normalized repository-relative `/` paths, never absolute paths;
- use Git/source content rather than filesystem enumeration order;
- sort changed paths and instruction sources lexically;
- sort candidate examples by descending deterministic score, then kind and
  normalized path; use stable sequential IDs after sorting;
- sort verification candidates by numeric priority, kind, argv, source, and ID;
- deduplicate set-like values before fingerprinting;
- use canonical newline-terminated TOON and `sha256:<64 lowercase hex>` with
  the artifact's own fingerprint field omitted;
- exclude timestamps, durations, process IDs, temp roots, raw command output,
  and secrets from signed identity.

Candidate ranking narrows what the agent should inspect; it does not prove
semantic comparability. Select 2–5 genuinely relevant implementations and
record why each is representative. If fewer than two exist, document the
bounded candidates inspected and why the rest were rejected. Never invent a
pattern or broaden into a full-repository scan merely to reach a count.

Regenerate context after every fix batch. Finalization must bind the report to
the current post-fix `change_fingerprint` and `context_fingerprint`.

## Repository engineering profile

Keep the profile lightweight and affected-area-specific:

- `architecture.pattern` and only relevant layers;
- concrete conventions as `name`, `value`, and non-empty repository evidence;
- 2–5 representative example paths where practical;
- an explicit `example_shortfall_reason` when fewer than two examples are used;
- concise applicable rules supported by those sources.

Evidence must cite repository-relative paths and useful anchors or observed
facts. A convention based solely on model preference is invalid. Do not invent
architecture, abstractions, layers, utilities, or framework conventions.

## Mandatory review dimensions

Review each applicable dimension and keep evidence in the draft even when it
does not produce a finding.

### Correctness

Check requirement interpretation, acceptance coverage, boundary and empty
states, null/undefined handling, invalid assumptions, off-by-one behavior,
state transitions, transactions, races, concurrency, retries, async control,
resource lifetime, API/serialization contracts, and fallback behavior.

### Repository fit

Compare existing helpers, business logic, interfaces, validation, errors,
logging, dependency injection, data access, naming, testing, mocking, and layer
boundaries. Flag duplicated utilities, new patterns without need, cross-layer
coupling, and casual dependencies using concrete examples.

### Simplicity and maintainability

Prefer the smallest coherent implementation. Check responsibilities, naming,
control flow, public contracts, duplication, hidden side effects, magic values,
misleading comments, generic one-use helpers, wrappers/factories, speculative
extension points/configuration, excessive indirection, and large change surface.
Comments should explain non-obvious reasoning, not narrate code.

### Testing

Check behavior coverage, negative and boundary cases, changed behavior without
tests, tests that can pass while behavior is wrong, excessive mocking, brittle
implementation coupling, and repository test style. Reuse the existing test
framework; never introduce one merely for this gate.

### Security and reliability

When relevant, inspect validation, authorization, injection, file/path safety,
secrets, defaults, deserialization, races, external calls, failures, retries,
and idempotency. Do not invent a security claim without local evidence.

### Scope and anti-AI checks

Treat every extra file, line, dependency, abstraction, and public API change as
risk. Inspect for obvious narration comments, generic one-use abstractions,
invented architecture, excessive helper extraction or wrappers, duplicate
utilities, silent/catch-all fallback, excessive mocking, TODO placeholders,
unnecessary compatibility, speculative configurability, unrelated refactors,
oversized implementation, impossible-state defenses, and over-general
solutions. Remove only unrelated changes made by this gate; preserve preexisting
user work byte-for-byte.

## Finding contract

Create the full finding set before any gate source edit. Canonically sort by
severity (`high`, `medium`, `low`), category (`correctness`, `architecture`,
`repository-fit`, `maintainability`, `testing`, `security`, `performance`,
`scope`), file, location, then stable ID. IDs use `QG-###` and are unique.

Every fixed and remaining finding contains exactly:

```yaml
id: QG-001
severity: high | medium | low
category: correctness | architecture | repository-fit | maintainability | testing | security | performance | scope
file: repository/relative/path
location: line, function, class, or empty string
issue: concise observed problem
evidence: [non-empty repository or executed-check evidence]
impact: concrete delivery or maintenance impact
recommended_fix: concrete corrective action
blocking: true | false
resolution: fixed | remaining
fix: applied correction or empty string
reason_not_fixed: explicit reason or empty string
```

Use High only for likely defects, security/data integrity risk, broken
requirements, major regression, or runtime-significant architecture violation.
Use Medium for material maintainability/test gaps, repository inconsistency,
unnecessary complexity, or a likely future defect. Use Low for non-blocking
readability or improvement opportunities. Do not inflate severity.

A fixed finding must have `resolution: fixed`, a non-empty `fix`, and an empty
`reason_not_fixed`. A remaining finding uses `resolution: remaining`, an empty
`fix`, and a non-empty reason when it could not safely be resolved. Product
clarification, missing authority, path scope, required broad refactoring, or a
new-dependency decision are reasons to leave a material finding explicit rather
than guess.

## Fix policy and preservation

Automatically fix:

- each High finding with one safe evidence-backed correction inside current
  authority;
- each safe localized Medium finding inside current authority.

Do not automatically fix Low findings or use a finding to justify application
redesign, style-only cleanup, public behavior changes outside the request, new
architecture, casual dependencies, configuration weakening, test suppression,
test deletion, or unrelated rewrites.

Immediately before remediation, require a successful Loop `implement-check`.
Check every edited path against current `allowed_paths`. After each batch,
compare tracked, staged, unstaged, and untracked state with the preflight
baseline. Any new out-of-scope or unrelated byte makes readiness false until
the gate-created change is safely removed.

## Verification contract

Detect commands only from repository-owned instructions, contributor guides,
scripts, task runners, package manifests, CI, or build/lint/type configuration.
Human-review argv before execution and follow active sandbox/host authority.
Never execute a repository-derived shell string.

Order verification deterministically: focused affected checks before broader
required build, typecheck, lint, unit/integration tests, and static analysis.
Sort records by phase (`before_fix`, `after_fix`, `final`), required before
optional, kind (`build`, `typecheck`, `lint`, `tests`, `static_analysis`,
`integration`, `other`), then stable ID. Preserve command argv order.

Each record contains exact argv and one status:

- `pass`: command actually ran successfully;
- `fail`: command actually ran and failed;
- `not_run`: an applicable command was skipped, blocked, interrupted, timed
  out, or could not run in the current environment; include the reason;
- `unavailable`: the repository exposes no applicable command/source for that
  optional verification kind; include the reason.

The `command` field is an argv array, never a shell command string. It may be
empty only for `status: unavailable`, when no applicable repository command
exists. An empty command for `pass`, `fail`, or `not_run` is invalid.

Use `exit_code` only when a process returned one. Keep evidence concise and
deterministic, such as exit result and stable test counts/digests; exclude raw
nondeterministic logs. If fixes occur, record relevant `after_fix` results; do
not overwrite `before_fix` evidence. Never claim passed based on configuration,
prior output, or expectation.

A required `before_fix` failure remains historical evidence after remediation;
it no longer blocks readiness only when the finding is fixed and all applicable
required `after_fix` or `final` checks pass.

## Report and readiness

The agent writes a draft conforming to
`ai-sdlc-engineering-quality-gate-draft/v1`. The helper validates it against the
current context, computes final scope and fingerprints, canonicalizes all
collections, and atomically writes `ai-sdlc-engineering-quality-gate/v1` TOON.
See `report-schema.toon`.

The final report also records repository-relative `context_path` so standalone
verification can reload the exact context, plus `context_fingerprint`,
`change_fingerprint`, and `report_fingerprint`. Output location and absolute
checkout root never enter signed identity.

Decision invariants:

- `PASS` and `ready_for_next_stage: true` require no remaining finding, no
  verification gap, no unrelated change, and every required available
  deterministic check passing.
- `PASS_WITH_FINDINGS` may be ready only when no High or blocking Medium
  remains, all required available checks pass, unrelated changes are empty,
  and only explicit non-blocking Low/Medium findings or optional unavailable
  checks remain.
- `FAIL` and `ready_for_next_stage: false` are required for any unresolved High,
  blocking Medium, required non-pass check, missing evidence, authority/scope or
  preservation failure, stale fingerprint, malformed report, or status/decision
  disagreement. Include at least one blocking reason.
- `unavailable` is never valid for a required check. An applicable required
  command that could not run is `not_run` and blocks readiness.

Scores are optional and may not replace the four required evidence lists:
repository consistency, correctness, testing, and simplicity. Every score that
is included must cite concrete evidence.

Run `finalize` and then `verify` against the unchanged current repository. A
failed helper command writes no partial canonical report and status cannot be
PASS.

## Human output and handoff

Render a concise YAML projection of the canonical facts in the active response:
status, summary, repository examples/patterns, fixed and remaining findings,
verification commands/outcomes, change scope, four quality evidence lists, and
the readiness decision/blockers. Do not persist this projection as a second
report.

Only a current ready report may hand off to `ai-sdlc-loop-verify`. This gate
never stages, commits, publishes, or performs the next skill automatically.
