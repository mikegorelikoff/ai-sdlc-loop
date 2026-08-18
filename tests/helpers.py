from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "skills" / "ai-sdlc-loop-orchestrate" / "scripts" / "loop.py"
sys.path.insert(0, str(ROOT / "skills" / "ai-sdlc-loop-shared-runtime" / "scripts"))
from toon import decode_toon


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
