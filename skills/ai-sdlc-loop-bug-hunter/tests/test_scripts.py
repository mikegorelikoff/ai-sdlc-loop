"""Owning hunter CLI contract; shared corpus covers evidence semantics."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
SKILL=Path(__file__).resolve().parents[1]
class HunterCommandTests(unittest.TestCase):
    def test_help_exposes_bounded_commands(self):
        result=subprocess.run([sys.executable,str(SKILL/'scripts/hunt.py'),'--help'],capture_output=True,text=True)
        self.assertEqual(0,result.returncode,result.stderr)
        for command in ['prepare','evaluate','verify','render','reproduce','handoff','--root']:
            self.assertIn(command,result.stdout)
    def test_missing_evidence_is_structured(self):
        with tempfile.TemporaryDirectory() as directory:
            result=subprocess.run([sys.executable,str(SKILL/'scripts/hunt.py'),'evaluate','--root',directory,'--input','absent.toon'],capture_output=True,text=True)
            self.assertEqual(1,result.returncode)
            self.assertIn('ai-sdlc-hunter-error/v1',result.stdout)
            self.assertNotIn('Traceback',result.stderr)
if __name__=='__main__':unittest.main()
