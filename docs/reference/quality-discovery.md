---
title: Quality discovery
description: Three bounded hunter surfaces with shared deterministic evidence contracts.
---

# Quality discovery

| Skill | Question | Accepted evidence | Handoff |
| --- | --- | --- | --- |
| Edge-case hunter | Under what unusual conditions could this fail? | Source anchor, applicable dimension, testable expected behavior | Test cases / QA |
| Blind-case hunter | What important dimension is absent from the model? | Search all required declared source roles, review exclusions; otherwise UNKNOWN | Requirements / readiness / SDD |
| Bug hunter | What is concretely wrong in implementation? | Code anchor and reviewed violation; CONFIRMED also needs current test reproduction | Code review / implementation / verification |

The shared runtime owns canonical TOON, stable HUNT IDs, deterministic ordering,
source fingerprints, exact quote/trace checks, deduplication and bounded linked
report validation. Each skill uses the native five-step graph. Explicit writes
belong to execute; verification and rendering can use stdout. Reproduction runs
only a selected authorized unittest in a disposable copy, with a deadline; it
is not an OS security sandbox. Structured unittest results distinguish failures
from execution errors. No hunter grants approval or modifies product code.

Downstream consumers validate both producer report and handoff packet. Separate
hunter identities preserve provenance when a blind concern becomes an edge
scenario and later a supported or confirmed bug. OKF retains its existing
provenance meaning; no new lifecycle or state engine is introduced.

| Limit | Consequence |
| --- | --- |
| Lexical dimension and absence library | Scope/search hints, not proof of semantic completeness |
| Supplied semantic review | Must establish requirement violation; a failing test alone is insufficient |
| Authored eval candidates | Structural and seeded-defect evidence, not live-model precision/recall |
| At most 3 repair iterations | Preserve unresolved evidence and stop; never weaken a gate |

Run the installed skill's `scripts/hunt.py --help` for exact input/output flags.
Its `references/execution.md` defines the source inventory and candidate path;
`references/chat-examples.md` shows normal, warning and blocked tables.
