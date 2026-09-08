# Framework diagnosis contract

Doctor diagnoses framework machinery. It preserves the existing installation
check and upgrade plan; it never invokes installation or applies a repair.

| Profile | Executed checks | Exclusions |
| --- | --- | --- |
| quick | Source inventory, native graph validation/reachability, script references, Python AST/local imports, chat contract, TOON parse/round-trip, test/eval presence | Arbitrary imports, tests, network |
| standard | Quick plus eight chat scenarios per skill, native execution scenarios in isolated fixtures, legal/illegal in-memory lifecycle transitions | Application execution and production mutations |
| deep | Standard plus two complete standard diagnoses with byte comparison | Live model behavior and external services |

Targeted scope includes the requested skill, Doctor, shared runtime and global
inventory/selector prerequisites. Unknown skill IDs fail explicitly. Every
registered skill and unregistered source skill receives structural checks in
full scope. Direct-entry utilities are not incorrectly classified as unreachable
because they have no lifecycle predecessor. Native step validators own cycle,
reachability, completion and declared handoff checks.

## Execution

1. DISCOVER: validate the explicit source root and authoritative inventory.
2. VALIDATE: run dependent registered checks. A failed prerequisite blocks its
   dependents and links their IDs; dependent symptoms are not independent roots.
3. EVALUATE: in standard/deep, copy bounded skill inputs and runtime references
   into a temporary source fixture; never execute candidate Python. Invoke the
   installed native selectors/renderers. Temporary fixture files are removed.
4. AGGREGATE: sort, derive health, validate report shape/policy/references/hash.
5. HANDOFF: render through the shared chat contract; route findings to the
   recorded owner. No repair, package installation or lifecycle write occurs.

The check registry is `scripts/framework.py:REGISTRY`; the report contract is
`framework-report.schema.toon`, enforced by `validate_report`. Each check records
stable identity, layer, status, severity, component, code, evidence, repair route
and blocked prerequisite IDs. No timestamps or environment values enter IDs.

## Health and failure policy

| Condition | Health | Exit |
| --- | --- | ---: |
| Critical prerequisite blocked | BLOCKED | 2 |
| High/critical check fails | UNHEALTHY | 2 |
| Other failures, blocked checks or unknown coverage | DEGRADED | 2 |
| All requested checks pass or are explicitly inapplicable | HEALTHY | 0 |
| Invalid invocation/report construction | UNKNOWN; execution FAIL | 1 |

PASS means the named check passed, not that unexecuted application tests passed.
Source syntax and local import resolution do not prove third-party dependency
availability. Test presence is not a test run. Core runtime self-tests and
product regression tests remain separate CI commands. Missing optional hunters are N/A. Registered hunters receive shared schema, wrapper and chat-contract checks; standard/deep also run pure scoped-absence, evidence-state, cross-ID and repeated-report fixtures. Semantic discovery quality is not inferred from those structural checks.

Root cause is asserted only for directly observed contract failures. Dependency
edges identify causal blockers; unrelated symptoms are never merged by an LLM.
Semantic interpretation may suggest repairs but cannot edit objective results.
No numeric health score, persistent history store, or automatic fix mode exists.

## Explicit artifact adapters

Pass repeatable `--artifact <kind>:<root-relative-value>` arguments:

| Kind | Value | Native authority |
| --- | --- | --- |
| toon | file | Parse and canonical round-trip only; no arbitrary schema claim |
| okf | bundle directory | OKF v0.2 document provenance validator |
| state | file | Backbone lifecycle state shape validator |
| loop-state | feature ID; Loop only | Loop stage reader and current spec fingerprint |
| decomposition | report file | Decomposition schema, source freshness, gates/references |
| handoff | packet file@report file | Recompute source-bound decomposition branch handoff |

OKF is provenance, not the lifecycle engine. Transition simulation tests the
native Backbone engine in memory; Loop approval state remains independently
owned by Loop. Historical transitions absent from source cannot be invented.
Files must be regular, contained, UTF-8 and at most 4 MB; symlinks are rejected.
Invalid fixture files under tests/fixtures are not production corruption.

## Examples

| Situation | Result | Next action |
| --- | --- | --- |
| All requested checks pass | HEALTHY; execution PASS | Continue selected workflow |
| Skill exists but registry omits it | INVENTORY_DRIFT; UNHEALTHY | SKILL_CONTRACT owner reviews registration |
| Python cannot parse | PYTHON_SYNTAX_FAILED; UNHEALTHY | PYTHON owner repairs exact component |
| Source root absent | BLOCKED; execution PASS | Supply readable source package |
| No local test evidence | UNKNOWN check; DEGRADED | TEST owner supplies coverage evidence |

Native TOON retains all checks. Chat uses bounded layer previews and findings;
extra rows reference the same invocation with `--format toon`. Preserve artifact
formats and omit duplicate prose. No health conclusion is based on chat alone.
