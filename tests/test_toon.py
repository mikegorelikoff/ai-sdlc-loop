from __future__ import annotations

import unittest

from tests.helpers import ROOT

import sys

sys.path.insert(0, str(ROOT / "skills" / "ai-sdlc-loop-shared-runtime" / "scripts"))
from toon import ToonDecodeError, decode_toon, encode_toon


class ToonContractTests(unittest.TestCase):
    def test_embedded_named_headers_remain_scalar_content(self):
        for content in ('clarification[4]: a,b,c,d', 'rows[1]{name}:\n  value', 'quoted: \"items[1]: text\"'):
            value = {"content": content, "nested": [{"content": content}], "key:with:colon": ["x"]}
            self.assertEqual(decode_toon(encode_toon(value)), value)


    def test_tc025_canonical_round_trip(self) -> None:
        value = {
            "schema": "ai-sdlc-loop/v1",
            "allowed_paths": [".github/workflows", "src"],
            "ready": True,
            "commands": [{"argv": ["python3", "-m", "unittest"], "exit_code": 0}],
        }
        encoded = encode_toon(value)
        self.assertEqual(value, decode_toon(encoded))
        self.assertEqual(encoded, encode_toon(decode_toon(encoded)))

    def test_tc025_malformed_toon_is_rejected(self) -> None:
        for payload in ("schema: one\nschema: two\n", "items[2]: one\n"):
            with self.subTest(payload=payload), self.assertRaises(ToonDecodeError):
                decode_toon(payload)


if __name__ == "__main__":
    unittest.main()
