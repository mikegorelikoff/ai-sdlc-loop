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
