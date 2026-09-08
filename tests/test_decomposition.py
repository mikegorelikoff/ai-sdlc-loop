"""Exercise installed hierarchical decomposition regressions."""
from pathlib import Path
import subprocess
import sys
import unittest
class DecompositionTests(unittest.TestCase):
    def test_product_skill_suite(self):
        root=Path(__file__).resolve().parents[1]
        result=subprocess.run([sys.executable,str(root/"skills/ai-sdlc-loop-hierarchical-decomposition/tests/test_scripts.py")],cwd=root,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
