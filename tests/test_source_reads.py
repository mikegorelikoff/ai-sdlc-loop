import sys
from pathlib import Path
from tests.helpers import ROOT
import tempfile
import unittest
from ai_sdlc_source_reads import read_bytes, read_text, source_scope

class SourceReadsTests(unittest.TestCase):
    def test_universal_newlines_preserve_raw_fingerprint_input(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "contract.md"
            for raw in (b"a\r\nb\r\n", b"a\rb\r", b"a\nb\n"):
                path.write_bytes(raw)
                @source_scope
                def check():
                    self.assertEqual(read_text(path), path.read_text(encoding="utf-8"))
                    self.assertEqual(read_text(path), "a\nb\n")
                    self.assertEqual(read_bytes(path), raw)
                check()

if __name__ == "__main__":
    unittest.main()
