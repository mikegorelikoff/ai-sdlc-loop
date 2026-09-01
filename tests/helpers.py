from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "skills" / "ai-sdlc-loop-orchestrate" / "scripts" / "loop.py"
QUALITY_GATE_CLI = (
    ROOT
    / "skills"
    / "ai-sdlc-loop-engineering-quality-gate"
    / "scripts"
    / "engineering_quality_gate.py"
)
sys.path.insert(0, str(ROOT / "skills" / "ai-sdlc-loop-shared-runtime" / "scripts"))
from toon import decode_toon, encode_toon


def run_cli(project: Path, *args: str, ok: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(CLI), "--project-root", str(project), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if ok and result.returncode:
        raise AssertionError(f"CLI failed: {result.stdout}\n{result.stderr}")
    return result


def git(project: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=project, text=True, capture_output=True, check=True
    ).stdout.strip()


def init_repo(path: Path) -> Path:
    path.mkdir()
    git(path, "init", "-q")
    git(path, "config", "user.name", "Loop Test")
    git(path, "config", "user.email", "loop@example.invalid")
    git(path, "config", "commit.gpgsign", "false")
    (path / "app.txt").write_text("before\n", encoding="utf-8")
    git(path, "add", "app.txt")
    git(path, "commit", "-qm", "initial")
    return path


def read_toon(path: Path) -> dict:
    value = decode_toon(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"expected TOON mapping: {path}")
    return value


def write_toon(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(encode_toon(value), encoding="utf-8")


def run_quality_gate(project: Path, *args: str, ok: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(QUALITY_GATE_CLI), *args, "--root", str(project)],
        text=True,
        capture_output=True,
        check=False,
    )
    if ok and result.returncode:
        raise AssertionError(f"quality gate CLI failed: {result.stdout}\n{result.stderr}")
    return result


def create_quality_gate(
    project: Path,
    feature: str = "demo",
    *,
    status: str = "PASS",
) -> dict:
    """Create a schema-valid gate from an actually executed deterministic check."""
    spec = read_toon(project / ".ai-sdlc-loop" / feature / "spec.toon")
    context_path = project / ".ai-sdlc-loop" / feature / "quality-context.toon"
    run_quality_gate(
        project,
        "context",
        "--request",
        spec["request"],
        "--feature",
        feature,
        "--quick-flow",
        "--output",
        f".ai-sdlc-loop/{feature}/quality-context.toon",
    )
    context = read_toon(context_path)
    passing = status != "FAIL"
    command = [sys.executable, "-c", "pass" if passing else "raise SystemExit(7)"]
    executed = subprocess.run(command, cwd=project, text=True, capture_output=True, check=False)
    examples = [item["path"] for item in context["candidate_examples"][:2]]
    remaining = []
    if status == "PASS_WITH_FINDINGS":
        remaining = [
            {
                "id": "QG-001",
                "severity": "low",
                "category": "maintainability",
                "file": "app.txt",
                "location": "",
                "issue": "The fixture intentionally records a non-blocking readability note.",
                "evidence": ["app.txt was inspected during the fixture review"],
                "impact": "No delivery impact; the note is retained for traceability.",
                "recommended_fix": "Consider the note during a future scoped change.",
                "blocking": False,
                "resolution": "remaining",
                "fix": "",
                "reason_not_fixed": "A Low finding does not justify broadening this fixture change.",
            }
        ]
    draft = {
        "schema": "ai-sdlc-engineering-quality-gate-draft/v1",
        "status": status,
        "summary": "Deterministic fixture quality review completed.",
        "repository_profile": {
            "architecture": {"pattern": "single-file fixture", "relevant_layers": ["application"]},
            "conventions": [
                {
                    "name": "change scope",
                    "value": "bounded by the Loop specification",
                    "evidence": ["The current Loop specification allows app.txt."],
                }
            ],
            "representative_examples": examples,
            "example_shortfall_reason": (
                "The minimal fixture contains fewer than two unchanged comparable implementations."
                if len(examples) < 2
                else ""
            ),
            "applicable_rules": ["Keep the fixture change inside the approved app.txt path."],
        },
        "findings_fixed": [],
        "remaining_findings": remaining,
        "verification": [
            {
                "id": "VERIFY-001",
                "kind": "tests",
                "phase": "final",
                "required": True,
                "status": "pass" if passing else "fail",
                "command": command,
                "exit_code": executed.returncode,
                "evidence": [
                    "The deterministic fixture command completed successfully."
                    if passing
                    else "The deterministic fixture command exited with code 7."
                ],
                "reason": "The fixture command is the available affected verification check.",
            }
        ],
        "change_scope": {"new_dependencies": [], "unrelated_changes": []},
        "quality_evidence": {
            "repository_consistency": ["The change remains inside the approved Loop path."],
            "correctness": ["The current app.txt bytes are bound into the context fingerprint."],
            "testing": ["The recorded fixture command was actually executed."],
            "simplicity": ["No dependency or abstraction was added to the fixture."],
        },
        "final_decision": {
            "ready_for_next_stage": passing,
            "blocking_reasons": [] if passing else ["Required deterministic verification failed."],
        },
    }
    draft_path = project / ".ai-sdlc-loop" / feature / "quality-gate-draft.toon"
    write_toon(draft_path, draft)
    report_path = project / ".ai-sdlc-loop" / feature / "quality-gate.toon"
    run_quality_gate(
        project,
        "finalize",
        "--context",
        f".ai-sdlc-loop/{feature}/quality-context.toon",
        "--draft",
        f".ai-sdlc-loop/{feature}/quality-gate-draft.toon",
        "--output",
        f".ai-sdlc-loop/{feature}/quality-gate.toon",
    )
    return read_toon(report_path)
