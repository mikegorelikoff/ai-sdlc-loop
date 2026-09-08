# Context graph

`ai-sdlc-loop-context-cache` is the Backbone context-cache engine packaged under
Loop’s namespace. It builds a disposable repository index, twelve-language AST
graph, bounded source-evidence packs and a standalone offline HTML explorer.
Repository files and the selected owning Loop step remain authoritative.

| Contract | Behavior |
| --- | --- |
| Discovery | Explicit repository root; excluded secrets, links, generated files and bounds are recorded |
| Storage | `.ai-sdlc-loop/cache/`; SQLite is local disposable state |
| Graph runtime | Exact Tree-sitter and twelve grammar versions; installation uses verified wheel hashes |
| Missing parser / invalid source | Explicit incomplete graph or direct-read fallback; `--require-graph` never silently accepts lexical retrieval |
| Reproducibility | Stable graph and repository fingerprints, ordering and TOON output |
| Viewer | Local HTML, no network; source bodies require `--include-source` |
| Lifecycle | No specification, approval, verification or commit authority |

## Commands

From a source checkout, check graph availability and build only when it passes:

```sh
python3 skills/ai-sdlc-loop-context-cache/scripts/context_cache.py graph-preflight --root .
python3 skills/ai-sdlc-loop-context-cache/scripts/context_cache.py build --root . --require-graph
python3 skills/ai-sdlc-loop-context-cache/scripts/context_cache.py graph-stats --root .
python3 skills/ai-sdlc-loop-context-cache/scripts/context_cache.py visualize --root .
```

Use `.agents/skills/` for an installed Codex project, `.claude/skills/` for Claude,
or the recorded custom skill root for an agent-project installation. The HTML
is `.ai-sdlc-loop/cache/context-graph.html`. The viewer reads an existing cache;
it does not build, repair or fetch data.

```sh
python3 skills/ai-sdlc-loop-context-cache/scripts/context_cache.py query --root . --query "customer onboarding"
```

`pack` targets an owning v2 skill step and validates its critical anchors and
budget. Compact Loop stage selection remains read-only; use queried source
evidence alongside its selected instructions and shared references. Installing
the package does not install native parsers or grant automatic source mutation.
The project cache-policy override is `.ai-sdlc-loop/context-cache-policy.toon`.

## Parser installation

Use a pre-populated wheelhouse matching the exact platform lock shipped with
the skill. No runtime download or implicit unpinned installation is performed.
The default lock is CPython 3.11/macOS arm64; Linux CI uses CPython 3.10 and 3.13 locks.

```sh
python3 skills/ai-sdlc-loop-context-cache/scripts/install_graph_runtime.py --lock skills/ai-sdlc-loop-context-cache/references/parser-lock.toon --wheelhouse /path/to/verified-wheelhouse
```

The installer verifies filenames and SHA-256 before invoking offline pip. An
unsupported platform stays blocked for AST graph mode; direct repository reads
remain available. Rebuild after source drift; never treat a stale pack
or diagnostic HTML as current evidence.
