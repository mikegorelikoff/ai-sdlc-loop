# Shared hunter contract

Extends the existing quality-lens finding model: stable id, registered lens,
critical/high/medium/low/info severity, path/line/detail evidence, trace targets,
owner, resolution status and next action. Hunter fields add a bounded condition,
expected behavior, evidence kind, validation state and related findings.
The machine contract is `hunters.schema.toon`, enforced by `ai_sdlc_hunters.py`.

| Hunter | Search surface | Evidence gate | Consumer |
| --- | --- | --- | --- |
| edge-case-hunter | Conditions around known behavior | Applicable dimension; exact source anchor; testable expected result | Test cases / QA |
| blind-case-hunter | Missing model dimensions | Complete declared role search, no text matches, reviewed hypothesis, no sourced exclusion | Requirements / readiness / SDD |
| bug-hunter | Concrete implementation | Implementation anchor; supported review; current reproduced test failure for CONFIRMED | Code review / implementation / verification |

Candidate fields and enums are authoritative in the shared schema. Scope and
source role assignment are semantic inputs. Applicability comes from the
explicit dimension library and current source content, not free-form ranking.
Dimension selection is a discovery signal, not a new product requirement.

Prepare records 1–32 explicit files, at most 256 KB each and 1 MB total. Quote
anchors and trace IDs must resolve. A source change invalidates the snapshot.
Candidates are at most 100 and iterations 1–3. Python owns canonical TOON,
source hashes, IDs, ordering, counts and duplicate detection. Equivalent
signatures merge only when all normalized facts match; conflicts are errors.
Related findings from current source-bound reports retain separate hunter IDs.

The evidence vocabulary is OBSERVED, INFERRED, HYPOTHETICAL. Bug statuses are
UNVERIFIED, SUPPORTED, REPRODUCED, CONFIRMED or REJECTED. A test mapping is MAPPED,
not PASS. Blind omission claims are scoped: missing roles yield UNKNOWN; lexical
matches require semantic review; exclusions require exact source anchors.
Counts describe identified dimensions and proposed cases, never invented test
coverage percentages or whole-repository completeness.

Reproduction is explicit and runs a selected trusted unittest in a disposable
copy, with a 30-second deadline. This is not an OS sandbox. The caller must have
authority to execute that test. Log and receipt are source-bound and must not
overwrite source/input files. Assertion failures differ from infrastructure
errors/timeouts. Review and evidence kind are checked before confirmation.
Hashes prove integrity and freshness, not independent authorship: never author
or edit a process receipt to promote a finding. Rerun reproduction to challenge
its evidence. Semantic review must establish that the failure violates the
stated contract; failing tests alone are not product requirements.

Hunters do not mutate OKF, lifecycle state, requirements or production code.
Native handoffs retain findings, report/source fingerprints, consumer and false
authorizes_execution. Consumers verify the producer report before using a
finding. Quality-lens compatible fields need no prose reinterpretation.

| Boundary example | Edge | Blind | Bug |
| --- | --- | --- | --- |
| Empty list | Testable unusual input | Only if an entire input model is missing | Only with implementation evidence |
| Missing account deletion | No invented feature | Reviewed omission or explicit exclusion | Only when required implementation is defective |
| DST | Timing scenario | Missing temporal model | Reproduced incorrect behavior |
| Lost update | Concurrency hypothesis | Missing consistency decision | Evidence-backed implementation defect |

No automatic repair or silent promotion. Rejected candidates retain their
reason; unverified candidates remain visible. After three unsuccessful input
iterations stop with ANALYSIS_INCOMPLETE and preserve validated evidence.
