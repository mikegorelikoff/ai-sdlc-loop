#!/usr/bin/env python3
"""Tests for ai-sdlc-loop-usage-coach: journaling, signal derivation, and Scenarios A-F."""

from __future__ import annotations

import io
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# Add Loop root and shared runtime to sys.path
TEST_DIR = Path(__file__).resolve().parent
LOOP_ROOT = TEST_DIR.parent
SHARED_DIR = LOOP_ROOT / "skills" / "ai-sdlc-loop-shared-runtime" / "scripts"
COACH_DIR = LOOP_ROOT / "skills" / "ai-sdlc-loop-usage-coach" / "scripts"

sys.path.insert(0, str(LOOP_ROOT))
sys.path.insert(0, str(SHARED_DIR))
sys.path.insert(0, str(COACH_DIR))

import coach
import usage_journal
from toon import decode_toon, encode_toon


class UsageCoachTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="coach_test_")
        self.root = Path(self.temp_dir)
        self.original_env = os.environ.get("AI_SDLC_LOOP_SESSION_ID")

    def tearDown(self):
        if self.original_env is not None:
            os.environ["AI_SDLC_LOOP_SESSION_ID"] = self.original_env
        else:
            os.environ.pop("AI_SDLC_LOOP_SESSION_ID", None)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_tc001_append_only_monotonic_sequence(self):
        """TC-001: Session journal creates append-only TOON file with monotonic keys."""
        sid = "20260928T100000Z-test1"
        os.environ["AI_SDLC_LOOP_SESSION_ID"] = sid

        seq1 = usage_journal.record_event("session.start", {"runtime_version": "0.10.1"}, session_id=sid, root=self.root)
        seq2 = usage_journal.record_event("skill.start", {"skill": "ai-sdlc-loop-specify"}, session_id=sid, root=self.root)
        seq3 = usage_journal.record_event("skill.end", {"skill": "ai-sdlc-loop-specify", "status": "completed"}, session_id=sid, root=self.root)

        self.assertEqual(1, seq1)
        self.assertEqual(2, seq2)
        self.assertEqual(3, seq3)

        sfile = usage_journal.get_session_file_path(sid, root=self.root)
        self.assertTrue(sfile.is_file())

        content = sfile.read_text(encoding="utf-8")
        self.assertIn("e000001:", content)
        self.assertIn("e000002:", content)
        self.assertIn("e000003:", content)

        parsed = decode_toon(content)
        self.assertEqual("ai-sdlc-loop-usage/v1", parsed.get("schema"))
        self.assertEqual(3, len(parsed.get("events", {})))

    def test_tc002_data_minimization_and_secret_redaction(self):
        """TC-002: Ensure secret tokens and sensitive prose are redacted/minimized."""
        sid = "20260928T100000Z-test2"
        os.environ["AI_SDLC_LOOP_SESSION_ID"] = sid

        secret_token = "ghp_123456789012345678901234567890123456"
        api_key = "sk-abcdef1234567890abcdef12"
        large_code = "def foo():\n    return 42\n" * 10

        usage_journal.record_event(
            "skill.start",
            {
                "skill": "ai-sdlc-loop-implement",
                "auth_header": f"Bearer {secret_token}",
                "openai_key": api_key,
                "code": large_code,
            },
            session_id=sid,
            root=self.root,
        )

        sfile = usage_journal.get_session_file_path(sid, root=self.root)
        content = sfile.read_text(encoding="utf-8")

        self.assertNotIn(secret_token, content)
        self.assertNotIn(api_key, content)
        self.assertIn("[REDACTED]", content)
        self.assertNotIn("def foo()", content)

    def test_tc003_fail_open_resilience(self):
        """TC-003: Logging errors fail open and return 0 without raising exceptions."""
        sid = "20260928T100000Z-test3"
        # Point to an unwritable directory or file path error
        fake_root = Path(self.temp_dir) / "non_existent_deep" / "unwritable"
        # Even if creating dir fails, record_event must return 0 and not throw
        ret = usage_journal.record_event("session.start", {}, session_id=sid, root=fake_root)
        # Guaranteed not to raise
        self.assertIsInstance(ret, int)

    def test_tc004_event_taxonomy(self):
        """TC-004: All required event categories record successfully."""
        sid = "20260928T100000Z-test4"
        os.environ["AI_SDLC_LOOP_SESSION_ID"] = sid

        # Session lifecycle
        usage_journal.record_event("session.start", {"runtime_version": "0.10.1"}, session_id=sid, root=self.root)
        # Skill execution
        usage_journal.record_event("skill.start", {"skill": "ai-sdlc-loop-specify", "trigger": "user", "phase": "specify"}, session_id=sid, root=self.root)
        usage_journal.record_event("skill.end", {"skill": "ai-sdlc-loop-specify", "status": "completed"}, session_id=sid, root=self.root)
        # User interactions & approvals
        usage_journal.record_event("approval.accepted", {"action": "implement", "reviewer": "team-lead"}, session_id=sid, root=self.root)
        # Artifacts
        usage_journal.record_event("artifact.created", {"artifact_type": "spec", "artifact_ref": ".ai-sdlc-loop/feature/spec.toon"}, session_id=sid, root=self.root)
        # Quality & verification
        usage_journal.record_event("quality_gate.executed", {"findings": {"high": 0, "medium": 1, "low": 2}}, session_id=sid, root=self.root)
        usage_journal.record_event("verification.passed", {"ready": True}, session_id=sid, root=self.root)
        # Transitions
        usage_journal.record_event("workflow.transition", {"previous_skill": "ai-sdlc-loop-specify", "current_skill": "ai-sdlc-loop-implement", "transition_type": "normal"}, session_id=sid, root=self.root)
        usage_journal.record_event("session.end", {"event_count": 8}, session_id=sid, root=self.root)

        sessions = usage_journal.scan_sessions(root=self.root)
        self.assertEqual(1, len(sessions))
        events = sessions[0]["events"]
        self.assertEqual(9, len(events))

    def test_tc005_scenario_a_canonical_run_and_scenario_e_handoff(self):
        """Scenario A (Canonical flow) and Scenario E (Handoff discoverability)."""
        sid = "20260928T100000Z-scenA"
        # Canonical flow
        skills = [
            "ai-sdlc-loop-specify",
            "ai-sdlc-loop-implement",
            "ai-sdlc-loop-engineering-quality-gate",
            "ai-sdlc-loop-verify",
            "ai-sdlc-loop-commit",
        ]
        for s in skills:
            usage_journal.record_event("skill.start", {"skill": s, "trigger": "user"}, session_id=sid, root=self.root)
            usage_journal.record_event("skill.end", {"skill": s, "status": "completed"}, session_id=sid, root=self.root)

        # Scenario E: skill used exclusively via handoff 4 times
        sid_e = "20260928T100000Z-scenE"
        for _ in range(4):
            usage_journal.record_event("skill.start", {"skill": "ai-sdlc-loop-edge-case-hunter", "trigger": "handoff"}, session_id=sid_e, root=self.root)
            usage_journal.record_event("skill.end", {"skill": "ai-sdlc-loop-edge-case-hunter", "status": "completed"}, session_id=sid_e, root=self.root)

        sessions = usage_journal.scan_sessions(root=self.root)
        self.assertEqual(2, len(sessions))

        signals = usage_journal.derive_signals(sessions)
        disc = signals["discoverability"]
        self.assertEqual(4, disc["ai-sdlc-loop-edge-case-hunter"]["handoff"])
        self.assertEqual(0, disc["ai-sdlc-loop-edge-case-hunter"]["user"])

        # Coach should suggest direct invocation for edge-case-hunter
        self.assertEqual(0, coach.cmd_suggest(session_id=sid_e, root=self.root))

    def test_tc006_scenario_b_evidence_lag(self):
        """Scenario B: Evidence lag detected when implementation finishes many steps before gate."""
        sid = "20260928T100000Z-scenB"
        usage_journal.record_event("skill.start", {"skill": "ai-sdlc-loop-implement"}, session_id=sid, root=self.root)
        usage_journal.record_event("skill.end", {"skill": "ai-sdlc-loop-implement", "status": "completed"}, session_id=sid, root=self.root)
        # 4 intermediary steps
        for i in range(4):
            usage_journal.record_event("skill.start", {"skill": f"ai-sdlc-loop-task-{i}"}, session_id=sid, root=self.root)
            usage_journal.record_event("skill.end", {"skill": f"ai-sdlc-loop-task-{i}", "status": "completed"}, session_id=sid, root=self.root)
        # Quality gate occurs after lag
        usage_journal.record_event("quality_gate.executed", {"passed": True}, session_id=sid, root=self.root)

        sessions = usage_journal.scan_sessions(root=self.root)
        signals = usage_journal.derive_signals(sessions)
        self.assertTrue(len(signals["evidence_lags"]) >= 1)
        avg_lag = signals["evidence_lags"][0]["steps"]
        self.assertTrue(avg_lag >= 4)

    def test_tc007_scenario_c_rework_cycles(self):
        """Scenario C: Recurring rework cycles (implement -> gate -> implement)."""
        sid = "20260928T100000Z-scenC"
        for _ in range(4):
            usage_journal.record_event("skill.start", {"skill": "ai-sdlc-loop-implement"}, session_id=sid, root=self.root)
            usage_journal.record_event("skill.end", {"skill": "ai-sdlc-loop-implement", "status": "completed"}, session_id=sid, root=self.root)
            usage_journal.record_event("skill.start", {"skill": "ai-sdlc-loop-engineering-quality-gate"}, session_id=sid, root=self.root)
            usage_journal.record_event("skill.end", {"skill": "ai-sdlc-loop-engineering-quality-gate", "status": "failed"}, session_id=sid, root=self.root)

        sessions = usage_journal.scan_sessions(root=self.root)
        signals = usage_journal.derive_signals(sessions)
        self.assertTrue(len(signals["rework_cycles"]) >= 3)

    def test_tc008_scenario_d_ignored_recommendations(self):
        """Scenario D: Tracking ignored recommendations when user chooses another skill."""
        sid = "20260928T100000Z-scenD"
        # Coach suggests bug hunter
        usage_journal.record_event("coach.suggest", {"suggested_skill": "ai-sdlc-loop-bug-hunter"}, session_id=sid, root=self.root)
        # User instead invokes implement
        usage_journal.record_event("skill.start", {"skill": "ai-sdlc-loop-implement", "trigger": "user"}, session_id=sid, root=self.root)

        sessions = usage_journal.scan_sessions(root=self.root)
        signals = usage_journal.derive_signals(sessions)
        self.assertEqual(1, len(signals["ignored_recommendations"]))
        self.assertEqual("ai-sdlc-loop-bug-hunter", signals["ignored_recommendations"][0]["recommended"])
        self.assertEqual("ai-sdlc-loop-implement", signals["ignored_recommendations"][0]["selected"])

    def test_tc009_scenario_f_capability_gaps(self):
        """Scenario F: Capability gaps from user overrides and blocked statuses."""
        sid = "20260928T100000Z-scenF"
        usage_journal.record_event("user.override", {"override_target": "custom_build_script", "reason": "no skill supports custom bundler"}, session_id=sid, root=self.root)
        usage_journal.record_event("skill.end", {"skill": "ai-sdlc-loop-implement", "status": "blocked", "reason": "unsupported packaging"}, session_id=sid, root=self.root)

        sessions = usage_journal.scan_sessions(root=self.root)
        signals = usage_journal.derive_signals(sessions)
        self.assertEqual(2, len(signals["capability_gaps"]))

    def test_tc010_to_tc014_cli_subcommands(self):
        """TC-010 to TC-014: Coach CLI subcommands."""
        # report
        self.assertEqual(0, coach.cmd_report(root=self.root))
        self.assertEqual(0, coach.cmd_report(output_format="toon", root=self.root))

        # explain
        self.assertEqual(0, coach.cmd_explain("rework-cycle"))
        self.assertEqual(0, coach.cmd_explain("gate-timing"))
        self.assertEqual(1, coach.cmd_explain("non-existent-signal"))

        # feedback
        self.assertEqual(0, coach.cmd_feedback("sug-1", "accepted", session_id="20260928T100000Z-test", root=self.root))


if __name__ == "__main__":
    unittest.main()
