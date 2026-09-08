# Command reference

Source `--help` output is authoritative.

| Purpose | Command |
| --- | --- |
| Install local checkout | `python3 install.py PROFILE` |
| Verify installation | `python3 install.py verify PROFILE` |
| Shared lifecycle CLI | `python3 .agents/skills/ai-sdlc-loop-shared-runtime/scripts/loop.py --help` |
| Guided Flow | `python3 .agents/skills/ai-sdlc-loop-flow/scripts/flow.py --help` |
| Installation Doctor | `python3 .agents/skills/ai-sdlc-loop-doctor/scripts/doctor.py --help` |

Flow exposes `explore` and `apply`. Doctor exposes `check` and `upgrade-plan`. Custom agents replace `.agents/skills` with their recorded project-relative skills root.

## Deterministic execution gates

Select the next dependency-ready node in a compact Loop lifecycle graph:

```sh
python3 .agents/skills/ai-sdlc-loop-shared-runtime/scripts/loop.py steps --skill ai-sdlc-loop-implement --phase execute
```

Pass each evidence-backed completed ID as `--completed-step <id>`. The selector
rejects unknown nodes, missing predecessors, cycles and missing step sources.
Its TOON result names selected paths and required references. `complete` means
the requested graph closure is exhausted; `authorizes_execution` remains false.
It checks the consistency of supplied completion claims, not their truth.
Implementation and commit still require their own current approval receipts.

Check current verification evidence before proposing a commit:

```sh
python3 .agents/skills/ai-sdlc-loop-shared-runtime/scripts/loop.py evidence-check --feature example
```

This read-only gate rejects non-passing commands, stale source snapshots,
invalid fingerprints and missing or stale engineering quality evidence. It
returns the verified fingerprint and `authorizes_commit: false`. Commit
preparation uses this gate; the Commit stage owns approval, staging and Git
execution. Verify also checks the snapshot after commands finish, so a passing
formatter or test that changes source cannot leave a ready result for the old
snapshot.
