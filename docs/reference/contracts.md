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

## Adaptive execution

Specify classifies execution depth automatically; explicit mode selection is a
minimum depth. FAST retains scope, quality and approval gates. STANDARD adds a
compact plan; DEEP retains the full workflow. `adapt` adds context, risk signals
and evidence without restarting the task. `next` reports remaining work.
Verification retries are bounded and unchanged passing evidence is reusable.
Independent verification commands can run concurrently only with an explicit
independence declaration. Missing host call and token counts remain unknown.
