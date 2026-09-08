"""Exercise packaged runtime regressions in the normal product test suite."""
from pathlib import Path
import subprocess
import sys
import unittest

class PackagedDeterminismTests(unittest.TestCase):
    def test_packaged_runtime(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run([sys.executable, str(root / "skills/ai-sdlc-loop-shared-runtime/tests/test_determinism.py")], cwd=root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
