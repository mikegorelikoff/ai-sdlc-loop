# Hunter execution

Use the shared `references/hunters-contract.md` and `scripts/ai_sdlc_hunters.py`
from the sibling shared-runtime package. The shared finding shape extends the
quality-lens model; common severity/evidence/owner/trace/resolution fields remain.

```sh
python3 scripts/hunt.py prepare --root . --input sources.toon --scope payment-retry --output candidates.toon
python3 scripts/hunt.py evaluate --root . --input candidates.toon --output report.toon
python3 scripts/hunt.py verify --root . --input report.toon
python3 scripts/hunt.py render --root . --input report.toon
python3 scripts/hunt.py handoff --root . --input report.toon --output handoff.toon
```

The source inventory is a TOON array of path/role records. Prepare owns snapshots
and dimensions; semantic reasoning supplies only candidate fields. Candidate
quotes must match the named source line. Referenced trace IDs must exist in the
bounded source set. Coverage exclusions need a source anchor. Review ACCEPT is
semantic evidence, not independent proof or authorization.

Bug reproduction is a separate explicit command, only for trusted tests:
`reproduce --root . --input candidates.toon --test test_case.py --log repro.log --output repro.toon`.
It copies declared source files into a disposable directory and runs unittest
with a 30-second deadline. It is not a security sandbox; never execute unknown
or unapproved code. Test failures require semantic review before CONFIRMED;
errors/timeouts remain UNVERIFIED. No automatic production repair occurs.

| Situation | Result | Route |
| --- | --- | --- |
| Boundary condition with current anchors | PROPOSED; mapped tests are not executed coverage | Test-case design |
| Missing concern with incomplete search roles | UNKNOWN | Context acquisition |
| Explicit sourced exclusion | REJECTED / OUT_OF_SCOPE | Preserve exclusion |
| Matching text found elsewhere | UNVERIFIED; review coverage | Requirements/SDD |
| Current test failure plus accepted code review | CONFIRMED | Code review and verification |
| Test cannot execute | UNVERIFIED | Reproduction or environment investigation |

All outputs are proposals; none mutate OKF, approve code, or waive a gate.
