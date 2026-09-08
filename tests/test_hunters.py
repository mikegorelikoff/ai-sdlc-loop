"""Run the canonical shared hunter corpus in Loop CI."""
import subprocess
import sys
import unittest
from pathlib import Path
class HunterCorpusTests(unittest.TestCase):
    def test_shared_hunter_corpus(self):
        root=Path(__file__).resolve().parents[1]
        result=subprocess.run([sys.executable,str(root/'skills/ai-sdlc-loop-shared-runtime/tests/test_hunters.py'),'-v'],cwd=root,capture_output=True,text=True)
        self.assertEqual(0,result.returncode,result.stdout+result.stderr)
