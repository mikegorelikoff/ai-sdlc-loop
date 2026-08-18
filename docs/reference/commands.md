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
