# Hierarchical decomposition execution contract

| Level | Meaning | Boundary |
| --- | --- | --- |
| Initiative | Why: business/product outcome | No implementation-component split |
| Epic | Major demonstrable outcome | Technical outcome needs explicit justification |
| Feature | Coherent user/system capability | Omit between Epic and Story when it adds no information |
| Story | Actor, behavior, expected outcome | Acceptance, assumptions, dependencies and verification required |
| Task | Necessary engineering obligation | Cannot expand parent product requirements |
| Acceptance / Verification | Observable success and checking approach | Attached obligations; not artificial Jira hierarchy nodes |

The legal structural edges are Initiative→Epic, Epic→Feature/Story, Feature→Story,
Story→Task. Starting at any supplied level is valid. Never invent parent layers.
The maximum tree is 128 nodes and 16 sources. `prepare` accepts 64,000 source bytes;
structured source snapshots allow 64,000 characters (at most 256 KiB of UTF-8).
Each machine artifact is bounded to 2 MiB.
Large requests must be scoped into explicit related runs before expansion.

## Semantic boundary

Input: exact supplied sources and candidate schema. Output: sourced requirements,
node keys, proposed axis, outcomes, obligations, assumptions, acceptance and review
receipts. Allowed axes: business capability, user journey, workflow stage, domain,
lifecycle, integration, operational outcome; implementation obligations below Story.
Front/back/team/repository splits require meaningful sourced technical outcome.

Keys are stable explicit source/issue identities, not display positions. Preserve
keys across title edits; new scope gets a new key. Python hashes scope/type/key with
SHA-256 and emits 16 hex digits; input reorder does not change IDs. Parent and dependency
references are explicit. All collections are canonical sets except derived sequence,
which retains stable topological order. Business priority remains UNKNOWN without
source evidence. No duration means no fabricated critical-path or effort calculation.

Acceptance criteria cover sourced happy, validation, error, permission, transition
and boundary behavior; QA decides applicability from evidence. NFRs propagate to
children unless a cited, Architecture-reviewed exclusion explains non-applicability.
A string match cannot prove a requirement or test correctly interprets its source.

## Independent review rubric

| Reviewer | Mandatory semantic checks |
| --- | --- |
| Product | Input level; every meaningful source clause accounted for; value; parent coverage; unsupported behavior; vertical slicing; overlap |
| Delivery | Independently demonstrable scope; too large/small; dependency sequence; estimation uncertainty; unnecessary layers |
| Architecture | Technical feasibility; integration and shared contracts; NFR applicability; hidden engineering obligations |
| QA | Actor/behavior; observable criteria; relevant error/permission/state conditions; requirement-to-AC coverage; INVEST |

Each role reviews the current branch and cites concrete source/requirement/AC evidence.
Reviewer UNKNOWN blocks; confidence never controls state. Real dependencies qualify
Independent only when explicit graph relations exist. Other INVEST dimensions cannot
be N/A for a Story. Reviews are assertions, not cryptographic proof of human independence.

## Failure and repair policy

| Condition | Deterministic action |
| --- | --- |
| Invalid shape/reference/digest | Exit 2; preserve previous artifact |
| Material unknown or pending assumption | Block branch; reject speculative descendants |
| Missing coverage, AC, review or source support | Exit 3 with named defect and repair action |
| Source/branch changed | Reject stale source/review; refresh affected evidence |
| Sequencing cycle | No sequence; report explicit defect |
| Candidate iteration 3 still blocked | STOP_AND_REPORT; no implicit fourth attempt |
| Valid report and passing selected branch | Emit sourced handoff; execution remains unauthorized |

There is no autonomous LLM retry service: the selected agent supplies semantic repairs.
For a durable `evaluate --output` run Python requires iteration 1 initially, then exactly
one increment for changed content; unchanged reruns preserve the iteration. Rewinding
or overwriting another scope is rejected. Keep the same output path throughout a run.
Read-only stdout evaluation does not persist or advance a repair run.
Native machine truth is canonical TOON. Human tables are reproducible projections.
Fixture evals are explicitly simulations and do not establish live-model reliability.
