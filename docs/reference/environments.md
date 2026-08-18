# Supported environments

| Profile | Skills root | Invocation |
| --- | --- | --- |
| `codex-project` | `.agents/skills` | POSIX bootstrap or Python |
| `claude-code-project` | `.claude/skills` | POSIX bootstrap or Python |
| `agent-project` | Explicit safe relative root | POSIX bootstrap or Python with `--skills-root` |

CI validates Python 3.11 on Linux, macOS, and Windows. The runtime uses the Python standard library and Git. The POSIX bootstrap is not the native Windows path; use `python install.py` there.
