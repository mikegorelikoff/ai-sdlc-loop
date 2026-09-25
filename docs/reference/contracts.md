# Contracts

| Contract | Schema | Authority |
| --- | --- | --- |
| Guided decision | `ai-sdlc-loop-flow/v1` | Read-only evidence |
| Flow handoff | `ai-sdlc-loop-flow-apply/v1` | Selects one owner; executes no owner action |
| Doctor report | `ai-sdlc-loop-doctor-report/v1` | Read-only evidence |
| Upgrade plan | `ai-sdlc-loop-upgrade-plan/v1` | Planning only; apply is false |
| Install record | `ai-sdlc-loop-install/v1` | Verification evidence |
| Lifecycle state | `ai-sdlc-loop/v1` | Local stage state and fingerprints |
| Promotion | `ai-sdlc-harness-promotion/v1` | Compatibility artifact only |

Canonical Loop machine artifacts use deterministic TOON. Fingerprints detect drift; they do not authenticate people or bypass host policy.

## Adaptive coordination

`specify` automatically records FAST, STANDARD or DEEP in
`state.toon:execution.decision`. `--mode` sets a minimum; `--full-flow` selects
DEEP, and observed `--signal key=value` facts can raise depth. Unknown scope or
confidence requires at least STANDARD. The existing specification, authorization,
quality report and passing verification receipts retain their authority.

`next --feature <feature>` selects missing adaptive work. `adapt` extends the
same context with `--context-file`, records compact decisions with `--plan-step`,
and escalates with `--signal`. Completed stages retain their evidence references;
escalation adds only missing analysis. Neither escalation nor respecification
resets verification attempts for the feature.

`verify --jobs 2 --independent` permits concurrent explicit commands only after
checking that they do not share mutable resources. Default execution is serial.
Three attempts allow initial verification and two changed repairs. Unchanged
failures stop; current passing checks return existing evidence. A concrete
`--retry-condition` records an environmental change that justifies retrying.
Source snapshots and current quality evidence still gate both paths.

`adapt --record-stage <name> --elapsed <seconds>` records measured host timing;
optional `--model-calls`, `--tool-calls`, `--context-tokens` and `--skill` record
actual host telemetry. Unknown counters remain null. Helpers do not invoke models;
helper timings cannot establish end-to-end agent latency.
