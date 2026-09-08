"""Loop installation and routing boundaries for the inherited context graph."""
import hashlib
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.helpers import ROOT, read_toon
from toon import decode_toon
from ai_sdlc_steps import _context_cache_root

SKILL = "ai-sdlc-loop-context-cache"
SOURCE = ROOT / "skills" / SKILL


class ContextGraphTests(unittest.TestCase):
    def test_engine_is_the_reviewed_backbone_source(self):
        provenance = read_toon(SOURCE / "references/upstream.toon")
        for source in provenance["sources"]:
            text = (SOURCE / source["path"]).read_text(encoding="utf-8")
            text = text.replace("ai-sdlc-loop-shared-runtime", "ai-sdlc-shared-runtime")
            text = text.replace("ai-sdlc-loop-context-cache", "ai-sdlc-context-cache")
            text = text.replace(".ai-sdlc-loop/cache/", ".ai-sdlc/cache/")
            self.assertEqual(hashlib.sha256(text.encode()).hexdigest(), source["sha256"], source["path"])

    def test_missing_parser_runtime_fails_closed(self):
        # The complete inherited suite runs in the hash-locked graph CI jobs.
        # Base-profile CI explicitly tests the no-parser contract instead.
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, "-S", str(SOURCE / "scripts/context_cache.py"),
                                     "graph-preflight", "--root", directory],
                                    cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            report = decode_toon(result.stdout)
            self.assertEqual(report["status"], "error")
            self.assertEqual(report["strategy"], "direct_read")
            self.assertEqual(report["reason"], "graph-parser-preflight-incomplete")
            self.assertFalse((Path(directory) / ".ai-sdlc-loop/cache/context-cache.sqlite3").exists())

    def test_context_intent_routes_before_generic_build(self):
        path = ROOT / "skills/ai-sdlc-loop-flow/scripts/flow.py"
        spec = importlib.util.spec_from_file_location("context_flow", path)
        flow = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(flow)
        for intent in ("build repository graph", "build context-graph", "refresh context-cache", "open graph explorer"):
            self.assertEqual(flow.select_route(intent), ("context", SKILL))
        self.assertEqual(flow.select_route("build a graph database feature")[0], "implement")

    def test_source_checkout_does_not_implicitly_activate_cache(self):
        self.assertIsNone(_context_cache_root(ROOT))

    def test_installed_profiles_have_self_contained_cache(self):
        for profile, relative in (("codex-project", ".agents/skills"),
                                  ("claude-code-project", ".claude/skills"),
                                  ("agent-project", "tools/skills")):
            with self.subTest(profile=profile), tempfile.TemporaryDirectory() as directory:
                root = Path(directory).resolve()
                command = [sys.executable, str(ROOT / "install.py"), "install", profile,
                           "--project-root", str(root)]
                if profile == "agent-project":
                    command += ["--skills-root", relative]
                result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                subprocess.run(["git", "init", str(root)], capture_output=True, check=True)
                (root / "source.py").write_text("def greeting():\n    return 'hello'\n", encoding="utf-8")
                subprocess.run(["git", "-C", str(root), "add", "source.py"], check=True)
                script = root / relative / SKILL / "scripts/context_cache.py"
                result = subprocess.run([sys.executable, str(script), "build", "--root", str(root)],
                                        cwd=Path(directory).parent, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertTrue((root / ".ai-sdlc-loop/cache/context-cache.sqlite3").is_file())
                self.assertFalse((root / ".ai-sdlc").exists())
                self.assertFalse((root / ".ai-sdlc-loop/state.toon").exists())
                result = subprocess.run([sys.executable, str(script), "query", "--root", str(root),
                                         "--query", "greeting"], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                response = decode_toon(result.stdout)
                if response["strategy"] == "cached":
                    self.assertIn("source.py", result.stdout)
                else:
                    # A Python with no pinned AST parsers must expose the
                    # inherited fail-closed path, never manufacture graph hits.
                    self.assertEqual(response["strategy"], "direct_read")
                    self.assertEqual(response["reason"], "graph-incomplete")
                    self.assertEqual(response["results"], [])
                    self.assertTrue(response["direct_read_paths"])
                # Resolve using the installed runtime, including custom skills roots.
                probe = "import sys;from pathlib import Path;sys.path.insert(0,sys.argv[1]);from ai_sdlc_steps import _context_cache_root;print(_context_cache_root(Path(sys.argv[2])))"
                runtime = root / relative / "ai-sdlc-loop-shared-runtime/scripts"
                found = subprocess.run([sys.executable, "-c", probe, str(runtime), str(root)],
                                       capture_output=True, text=True, check=True)
                self.assertEqual(found.stdout.strip(), str(script.parents[1]))


if __name__ == "__main__":
    unittest.main()
