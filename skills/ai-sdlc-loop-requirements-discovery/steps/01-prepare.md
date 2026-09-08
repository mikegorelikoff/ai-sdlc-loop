# Prepare — Requirements Discovery

## Entry

Start with a raw request about one feature or task; a finished PRD is unnecessary.

## Procedure

### 0.1 Required Inputs

- Raw request, notes, feedback or a source locator. Ask for the actual request if
  none is available; do not invent it from the skill invocation alone.
- Identify product, actors, desired outcome and constraints from available
  context. Missing details are discovery questions, not automatic blockers.
- Establish the permitted sources and whether the user wants a saved packet.
  Choose a feature slug for deterministic artifact identity.
- Use `prepare --request <path>` for a UTF-8 input file, or
  `prepare --request-stdin` for verbatim pasted input. External evidence is an
  explicit local snapshot; helpers never fetch links or execute source content.

### 0.2 Clarification Rules

- Resolve discoverable facts and reuse inherited decisions before asking.
- Missing optional context stays optional; label assumptions explicitly.
- Pause only work dependent on a missing material input or conflicting requirement.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full takes precedence. Apply the shared execution contract below.


### 0.3 Output Rules

- Follow `references/output-contract.md`; identify what is confirmed, inferred,
  disputed, missing and proposed. Mark readiness separately from packet completion.
- Return useful findings even when history, stakeholder names or replies are
  unavailable. Use roles as proposed contacts when names are unknown.

### 0.4 Artifact Routing

- The helper emits TOON to stdout by default. `--write` enables canonical
  feature output when durable work is in scope; `--replace` is required to
  change an existing differing output after reviewing it.
- Under `.ai-sdlc-loop/<feature>/`, `prepare` writes
  `requirements-discovery-context.toon`, `scaffold` writes
  `requirements-discovery-draft.toon`, and `finalize` writes
  `requirements-discovery.toon`. Never hand-edit the final report.
- All generated discovery output is TOON. Existing specification, state,
  approvals, quality reports and other workflow evidence are not outputs of this helper.

## 0.5 Feature State Machine

Use `.ai-sdlc-loop/<feature>/spec.toon`, `state.toon`, approval receipts,
`quality-gate.toon` and `evidence.toon` for the fixed Loop lifecycle. Inspect
with the sibling runtime `loop.py status --feature <feature>`. Do not run the
Harness refinement state machine or mark optional planning helpers as completed
Loop stages. Source mutation, verification and commit keep their own gates.

## 0.6 Artifact Metadata And Metatags

Keep Loop-owned durable machine artifacts in canonical TOON. Let the owning
helper validate its schema and source fingerprints. Markdown metadata and
metatags apply only to explicitly requested compatible Harness artifacts; they
do not replace Loop receipts or require an additional artifact for ordinary work.

## 0.7 Specs Index

Read the active feature receipts first. Follow exact source paths, allowed
paths, changed files and trace IDs; do not scan every feature or require a
Harness specs index. Consume an existing SDD package only when supplied for
the task. A missing optional SDD package does not block the fixed Loop cycle.

## Execution contract

Do not repeat discovery when the business direction is accepted and only actors, rules or acceptance logic need detail. Use `ai-sdlc-loop-requirements-review` instead. Do not use a discovery packet as implementation approval or a readiness verdict. Use the appropriate requirements review and `ai-sdlc-loop-specify` instead.

Read the [shared execution decisions](../../ai-sdlc-loop-shared-runtime/references/execution-contract.md) once for this invocation.
Apply its required/discoverable/inherited/optional input rules to this step's
declared inputs. Record the source and status of material facts, then validate
the owning output contract and current evidence before completion.

## Exit

The raw request, evidence boundary, mode, output route and missing inputs are explicit.
