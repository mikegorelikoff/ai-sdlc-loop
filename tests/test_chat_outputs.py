from pathlib import Path
import subprocess
import sys
import unittest

class ChatContractRegressionTests(unittest.TestCase):
    def test_all_loop_chat_scenarios(self):
        root = Path(__file__).resolve().parents[1]
        p = subprocess.run([sys.executable, str(root / "skills/ai-sdlc-loop-shared-runtime/tests/test_chat_output.py")], cwd=root, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
