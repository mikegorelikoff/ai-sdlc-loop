"""Build the Windows x64 installer from an explicit skill inventory."""
from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import install

VERSION = "0.10.0"
NAME = f"ai-sdlc-loop-{VERSION}-windows-x64-setup"


def stage(destination: Path) -> None:
    for name in install.SKILLS:
        source = ROOT / "skills" / name
        install.digest_tree(source)  # Reject linked package inputs before copying.
        shutil.copytree(source, destination / "skills" / name,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", "tests"))
    shutil.copy2(ROOT / "install.py", destination / "install.py")
    shutil.copy2(ROOT / "LICENSE", destination / "LICENSE")


def main() -> None:
    if sys.platform != "win32":
        raise SystemExit("Build this installer on Windows x64 with Python 3.11.")
    if sys.maxsize <= 2**32:
        raise SystemExit("An x64 Python interpreter is required.")
    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="loop-windows-build-") as folder:
        work = Path(folder)
        payload = work / "payload"
        stage(payload)
        subprocess.run([
            sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--onefile",
            "--noupx", "--name", NAME, "--distpath", str(output),
            "--workpath", str(work / "build"), "--specpath", str(work),
            "--paths", str(ROOT), "--hidden-import", "ast", "--hidden-import", "math",
            "--add-data", f"{payload / 'skills'}:skills",
            "--add-data", f"{payload / 'install.py'}:.",
            "--add-data", f"{payload / 'LICENSE'}:.",
            str(ROOT / "packaging/windows/launcher.py"),
        ], check=True)
    exe = output / (NAME + ".exe")
    checksum = hashlib.sha256(exe.read_bytes()).hexdigest()
    exe.with_suffix(".exe.sha256").write_text(f"{checksum}  {exe.name}\n", encoding="ascii")
    print(exe)


if __name__ == "__main__":
    main()
