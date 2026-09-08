"""All-product-skill structural evals and compact graph mutation scenarios."""

import shutil
import tempfile
import unittest
from pathlib import Path

from tests.helpers import ROOT, read_toon, run_cli
from toon import encode_toon
from loop_steps import select_steps
from ai_sdlc_skill_eval import evaluate_skill


class SkillGraphTests(unittest.TestCase):
    def test_every_skill_graph_reaches_exact_terminal_closure(self):
        count = 0
        for manifest_path in sorted((ROOT / "skills").glob("*/steps/manifest.toon")):
            manifest = read_toon(manifest_path)
            skill = manifest["skill"]
            with self.subTest(skill=skill):
                if manifest["schema"] == "ai-sdlc-skill-steps/v2":
                    receipt = evaluate_skill(ROOT, skill)
                    self.assertEqual(receipt["failed"], 0, receipt)
                else:
                    receipt = evaluate_skill(ROOT, skill)
                    self.assertEqual(receipt["failed"], 0, receipt)
                    for phase in manifest["entrypoints"]:
                        done = []
                        for _ in range(len(manifest["steps"]) + 1):
                            result = select_steps(ROOT / "skills", skill, phase, done)
                            self.assertEqual(encode_toon(result), encode_toon(select_steps(ROOT / "skills", skill, phase, done)))
                            self.assertFalse(result["authorizes_execution"])
                            if result["complete"]:
                                self.assertEqual(set(done), set(result["execution_order"]))
                                self.assertFalse(result["ready_steps"])
                                break
                            self.assertTrue(result["ready_steps"])
                            done.extend(result["ready_steps"])
                        else:
                            self.fail("graph did not terminate within its node count")
                count += 1
        self.assertEqual(count, 22)
        self.assertTrue((ROOT / "skills/ai-sdlc-loop-shared-runtime/references/execution-contract.md").is_file())

    def test_compact_graph_rejects_inconsistent_completion_and_unknown_phase(self):
        skill = "ai-sdlc-loop-implement"
        for phase, completed, code in (("validate", ["implement"], "STEP_INVALID_COMPLETION"),
                                       ("unknown", [], "STEP_UNKNOWN_PHASE"),
                                       ("validate", ["missing"], "STEP_UNKNOWN_COMPLETION")):
            with self.subTest(code=code), self.assertRaisesRegex(ValueError, code):
                select_steps(ROOT / "skills", skill, phase, completed)

    def test_mutated_cycle_missing_step_and_stale_source(self):
        with tempfile.TemporaryDirectory() as directory:
            skills = Path(directory)
            skill = "ai-sdlc-loop-implement"
            shutil.copytree(ROOT / "skills" / skill, skills / skill)
            # Shared execution instructions are an installed dependency.
            shutil.copytree(ROOT / "skills/ai-sdlc-loop-shared-runtime/references",
                            skills / "ai-sdlc-loop-shared-runtime/references")
            manifest_path = skills / skill / "steps/manifest.toon"
            original = read_toon(manifest_path)
            first = select_steps(skills, skill, "validate")
            document = skills / skill / original["steps"][0]["path"]
            document.write_text(document.read_text() + "\nAdditional bounded evidence.\n")
            self.assertNotEqual(first["graph_fingerprint"], select_steps(skills, skill, "validate")["graph_fingerprint"])
            original["steps"][0]["depends_on"] = original["steps"][-1]["id"]
            manifest_path.write_text(encode_toon(original))
            with self.assertRaisesRegex(ValueError, "cyclic"):
                select_steps(skills, skill, "validate")
            original["steps"][0]["depends_on"] = ""
            manifest_path.write_text(encode_toon(original))
            document.unlink()
            with self.assertRaisesRegex(ValueError, "missing regular"):
                select_steps(skills, skill, "validate")

    def test_compact_selector_cli_is_read_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = run_cli(root, "steps", "--skill", "ai-sdlc-loop-implement", "--phase", "execute")
            self.assertIn("authorizes_execution: false", result.stdout)
            self.assertEqual(list(root.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
