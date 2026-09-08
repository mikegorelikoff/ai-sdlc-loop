# Framework Doctor

Doctor proves local framework checks and routes repairs. It does not diagnose
application business logic or grant permission to apply changes.

```sh
python3 skills/ai-sdlc-loop-doctor/scripts/doctor.py framework --root . --mode quick --format markdown
```

Use `--mode standard` for isolated execution and chat scenarios, `--mode deep`
for repeated diagnostics, and `--skill ai-sdlc-loop-doctor` for a targeted scope.
Machine output defaults to canonical TOON; Markdown is a bounded chat projection.

| Scope | Verification |
| --- | --- |
| Source | Native inventory, contracts, scripts, graph, TOON and eval checks |
| Artifacts | Explicit typed arguments; no implicit scan of project documents |
| Installation | Existing Doctor installation check remains unchanged |
| Health | Objective HEALTHY/DEGRADED/UNHEALTHY/BLOCKED rules |
| Safety | No candidate script imports, application tests, network or project writes |

Exit 0 means healthy requested scope, 2 means a completed non-healthy diagnosis,
and 1 means Doctor could not construct a valid result. Unexecuted checks never
count as passed tests. Optional absence and unsupported coverage are explicit.

See the installed skill's `references/framework-contract.md` for artifact
adapter syntax, stable IDs, dependency handling, limits and repair ownership.
