"""Exercise the real EXE without Python on PATH, including rejection paths."""
from __future__ import annotations

import hashlib
import ctypes
import time
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import install
import importlib.util


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


builder = _load("loop_windows_builder", ROOT / "packaging" / "windows" / "build.py")
launcher = _load("loop_windows_launcher", ROOT / "packaging" / "windows" / "launcher.py")


def main() -> None:
    if len(sys.argv) > 1:
        exe = Path(sys.argv[1]).resolve()
    else:
        exe = (ROOT / "dist" / f"{builder.NAME}.exe").resolve()
    expected = exe.with_suffix(".exe.sha256").read_text(encoding="ascii").split()[0]
    assert hashlib.sha256(exe.read_bytes()).hexdigest() == expected
    env = dict(os.environ)
    env["PATH"] = str(Path(os.environ["SystemRoot"]) / "System32")
    env.pop("PYTHONHOME", None)
    env.pop("PYTHONPATH", None)
    with tempfile.TemporaryDirectory(prefix="Loop installer ü space ") as folder:
        root = Path(folder)
        def run(*args, success=True):
            result = subprocess.run([str(exe), *args], cwd=root, env=env, capture_output=True, text=True, timeout=90)
            assert (result.returncode == 0) == success, (result.returncode, result.stdout, result.stderr)
            return result
        assert launcher.VERSION in run("--version").stdout
        # Prove the bundled Tcl/Tk GUI opens and exits without system Python.
        user32 = ctypes.windll.user32
        user32.FindWindowW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p]
        user32.FindWindowW.restype = ctypes.c_void_p
        user32.PostMessageW.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_size_t, ctypes.c_ssize_t]
        process = subprocess.Popen([str(exe)], cwd=root, env=env)
        try:
            deadline = time.monotonic() + 45
            handle = None
            expected_title = f"AI SDLC Loop {launcher.VERSION} Setup"
            while time.monotonic() < deadline and process.poll() is None:
                handle = user32.FindWindowW(None, expected_title)
                if handle:
                    break
                time.sleep(0.2)
            assert handle, f"packaged setup window '{expected_title}' did not open"
            user32.PostMessageW(handle, 0x0010, 0, 0)  # WM_CLOSE
            assert process.wait(timeout=20) == 0
        finally:
            if process.poll() is None:
                subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], env=env, check=False)

        for profile in ("codex-project", "claude-code-project", "agent-project"):
            project = root / profile
            project.mkdir()
            extra = ["--skills-root", "custom/skills"] if profile == "agent-project" else []
            args = [profile, "--project-root", str(project), *extra]
            run("install", *args)
            run("verify", *args)
            run("install", *args)  # Same-version installation is idempotent.
            skills = project / ({"codex-project": ".agents/skills", "claude-code-project": ".claude/skills"}.get(profile, "custom/skills"))
            assert len(list(skills.glob("ai-sdlc-loop-*"))) == len(install.SKILLS)
            target = skills / "ai-sdlc-loop-flow/SKILL.md"
            with target.open("a", encoding="utf-8") as stream:
                stream.write("\nlocal change\n")
            run("verify", *args, success=False)
            run("install", *args, success=False)
            assert "local change" in target.read_text(encoding="utf-8")
        run("install", "agent-project", "--project-root", str(root), "--skills-root", "../escape", success=False)
    print("Windows EXE: all profiles, no Python on PATH, checksums, drift and unsafe-root checks passed")


if __name__ == "__main__":
    main()
