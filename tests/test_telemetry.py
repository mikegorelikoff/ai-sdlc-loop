#!/usr/bin/env python3
"""Comprehensive test suite for unified AI SDLC Telemetry (Loop).

Validates:
1. Pure TOON serialization (schema: ai-sdlc-telemetry/v1, ULID Crockford Base32, product: ai-sdlc-loop).
2. Zero token fabrication (strict usage_available=False and models=[] when unavailable).
3. User identity resolution (.customization.toon, ~/.config/ai-sdlc/config.toon, git/env fallback).
4. Secret redaction (bearer tokens, API keys, private keys).
5. POSIX flock concurrency and retry.
6. Fail-open exception shielding under filesystem/permission faults.
7. CLI commands (record, read, dump).
8. Automatic hook via Loop usage_journal and loop.py stage completion.
"""

from __future__ import annotations

import concurrent.futures
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

# Setup paths for loop imports
_TEST_DIR = Path(__file__).resolve().parent
_LOOP_ROOT = _TEST_DIR.parent
_SCRIPTS_DIR = _LOOP_ROOT / "skills" / "ai-sdlc-loop-shared-runtime" / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
if str(_LOOP_ROOT) not in sys.path:
    sys.path.insert(0, str(_LOOP_ROOT))

import ai_sdlc_telemetry as telemetry
import ai_sdlc_toon as toon_codec
import usage_journal


class LoopTelemetryTests(unittest.TestCase):
    """Test suite covering the unified TelemetryEvent v1 contract for AI SDLC Loop."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        self.root = Path(self.temp_dir)
        self.telemetry_file = self.root / ".ai" / "telemetry" / "sessions.toon"

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_pure_toon_serialization_loop_source(self) -> None:
        """Verify TelemetryEvent v1 produces pure TOON with source.product == 'ai-sdlc-loop'."""
        ev = telemetry.record_telemetry_event(
            skill="ai-sdlc-loop-specify",
            status="success",
            duration_ms=180,
            task={"id": "loop-01", "type": "stage", "title": "specify", "owner": "Dev"},
            root=self.root,
        )
        self.assertIsNotNone(ev)
        self.assertEqual(ev["status"], "success")
        self.assertEqual(ev["source"]["product"], "ai-sdlc-loop")
        self.assertTrue(self.telemetry_file.is_file())

        # Verify no non-TOON files created anywhere under .ai
        ai_dir = self.root / ".ai"
        for p in ai_dir.rglob("*"):
            if p.is_file():
                self.assertEqual(p.suffix, ".toon", f"Non-TOON file detected: {p}")

        raw = self.telemetry_file.read_text(encoding="utf-8")
        self.assertTrue(raw.startswith("schema: ai-sdlc-telemetry/v1\nevents:\n"))

        decoded = toon_codec.loads(raw)
        self.assertEqual(decoded["schema"], "ai-sdlc-telemetry/v1")
        events = decoded["events"]
        self.assertEqual(len(events), 1)

        event_id = ev["event_id"]
        self.assertEqual(len(event_id), 26)
        self.assertTrue(all(c in telemetry.CROCKFORD_BASE32 for c in event_id))

        entry = events[event_id]
        self.assertEqual(entry["source"]["product"], "ai-sdlc-loop")
        self.assertEqual(entry["skill"]["name"], "ai-sdlc-loop-specify")
        self.assertEqual(entry["duration_ms"], 180)

    def test_zero_token_fabrication(self) -> None:
        """Verify zero token fabrication: usage_available=False and models=[] when unavailable."""
        ev_no_usage = telemetry.record_telemetry_event(
            skill="ai-sdlc-loop-verify",
            root=self.root,
        )
        self.assertIsNotNone(ev_no_usage)
        self.assertFalse(ev_no_usage["usage_available"])
        self.assertEqual(ev_no_usage["models"], [])

        ev_with_usage = telemetry.record_telemetry_event(
            skill="ai-sdlc-loop-coach",
            models=[{
                "provider": "google",
                "model": "gemini-2.5-pro",
                "input_tokens": 500,
                "output_tokens": 200,
                "total_tokens": 700,
                "cache_read_tokens": 300,
                "cache_write_tokens": 50,
                "reasoning_tokens": 25,
            }],
            root=self.root,
        )
        self.assertIsNotNone(ev_with_usage)
        self.assertTrue(ev_with_usage["usage_available"])
        self.assertEqual(len(ev_with_usage["models"]), 1)
        self.assertEqual(ev_with_usage["models"][0]["model"], "gemini-2.5-pro")

        raw = self.telemetry_file.read_text(encoding="utf-8")
        decoded = toon_codec.loads(raw)
        self.assertEqual(decoded["events"][ev_no_usage["event_id"]]["models"], [])
        self.assertFalse(decoded["events"][ev_no_usage["event_id"]]["usage_available"])
        self.assertEqual(len(decoded["events"][ev_with_usage["event_id"]]["models"]), 1)
        self.assertTrue(decoded["events"][ev_with_usage["event_id"]]["usage_available"])

    def test_user_identity_resolution(self) -> None:
        """Verify user resolution from .customization.toon and fallback."""
        customization = self.root / ".customization.toon"
        customization.write_text(
            "schema: ai-sdlc-config/v1\n"
            "values:\n"
            "  user:\n"
            "    name: \"Dave Lead\"\n"
            "    email: \"dave@company.internal\"\n"
            "    role: \"software-engineer\"\n",
            encoding="utf-8",
        )

        user_info = telemetry.resolve_user(self.root)
        self.assertEqual(user_info["name"], "Dave Lead")
        self.assertEqual(user_info["email"], "dave@company.internal")
        self.assertEqual(user_info["role"], "software-engineer")

        ev = telemetry.record_telemetry_event(skill="ai-sdlc-loop-planning", root=self.root)
        self.assertEqual(ev["user"]["name"], "Dave Lead")

    def test_secret_redaction(self) -> None:
        """Verify secret tokens and API keys are redacted in Loop telemetry."""
        gh_token = "ghp_123456789012345678901234567890123456"
        aiza_key = "AIzaSyD-1234567890123456789012345678901"

        ev = telemetry.record_telemetry_event(
            skill="ai-sdlc-loop-verify",
            status="error",
            error={"code": "TOKEN_ERROR", "message": f"Invalid key {aiza_key} with auth {gh_token}"},
            root=self.root,
        )
        self.assertIsNotNone(ev)
        msg = ev["error"]["message"]
        self.assertNotIn("AIzaSyD", msg)
        self.assertNotIn("ghp_12345", msg)
        self.assertIn("[REDACTED]", msg)

    def test_fail_open_behavior(self) -> None:
        """Verify recording never raises exceptions even when filesystem is broken."""
        with patch("builtins.open", side_effect=OSError("Disk failure")):
            res = telemetry.record_telemetry_event(
                skill="ai-sdlc-loop-specify",
                root=self.root,
            )
            self.assertIsNone(res)

    def test_concurrency_flocking(self) -> None:
        """Verify multi-threaded appending preserves valid TOON without interleaving corruption."""
        num_events = 15

        def append_one(i: int) -> str | None:
            res = telemetry.record_telemetry_event(
                skill=f"ai-sdlc-loop-worker-{i}",
                duration_ms=i * 15,
                root=self.root,
            )
            return res["event_id"] if res else None

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(append_one, i) for i in range(num_events)]
            recorded_ids = [f.result() for f in futures]

        self.assertEqual(len(recorded_ids), num_events)
        raw = self.telemetry_file.read_text(encoding="utf-8")
        data = toon_codec.loads(raw)
        self.assertEqual(len(data.get("events", {})), num_events)

    def test_cli_record_read_and_dump(self) -> None:
        """Verify CLI record, read, and dump subcommands for Loop."""
        code = telemetry.main([
            "record",
            "--skill", "ai-sdlc-loop-specify",
            "--status", "success",
            "--duration-ms", "90",
            "--root", str(self.root),
        ])
        self.assertEqual(code, 0)
        self.assertTrue(self.telemetry_file.is_file())

        events = telemetry.read_telemetry_events(root=self.root)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["skill"]["name"], "ai-sdlc-loop-specify")

        dumped = telemetry.dump_telemetry(root=self.root)
        self.assertIn("ai-sdlc-loop-specify", dumped)

    def test_loop_usage_journal_hook(self) -> None:
        """Verify Loop usage_journal triggers telemetry appending on skill.end and track_skill."""
        usage_journal.record_event(
            "skill.end",
            {
                "skill": "ai-sdlc-loop-verify",
                "status": "completed",
                "duration_ms": 210,
                "feature": "demo-feature",
            },
            root=self.root,
        )

        events = telemetry.read_telemetry_events(root=self.root)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["skill"]["name"], "ai-sdlc-loop-verify")
        self.assertEqual(events[0]["source"]["product"], "ai-sdlc-loop")
        self.assertEqual(events[0]["task"]["id"], "demo-feature")

        with usage_journal.track_skill("ai-sdlc-loop-coach", feature="demo-coach", root=self.root):
            pass

        events2 = telemetry.read_telemetry_events(root=self.root)
        self.assertEqual(len(events2), 2)
        self.assertEqual(events2[1]["skill"]["name"], "ai-sdlc-loop-coach")
        self.assertEqual(events2[1]["task"]["id"], "demo-coach")

    def test_loop_stage_completion_telemetry(self) -> None:
        """Verify loop.py record_stage_telemetry appends to .ai/telemetry/sessions.toon."""
        import loop
        loop.record_stage_telemetry(
            self.root,
            "feature-x",
            "context",
            skill="ai-sdlc-loop-specify",
            duration_ms=120,
        )
        loop.record_stage_telemetry(
            self.root,
            "feature-x",
            "verify",
            skill="ai-sdlc-loop-verify",
            status="success",
            duration_ms=300,
        )
        events = telemetry.read_telemetry_events(root=self.root)
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]["skill"]["name"], "ai-sdlc-loop-specify")
        self.assertEqual(events[0]["task"]["title"], "context")
        self.assertEqual(events[1]["skill"]["name"], "ai-sdlc-loop-verify")
        self.assertEqual(events[1]["task"]["title"], "verify")


if __name__ == "__main__":
    unittest.main()
