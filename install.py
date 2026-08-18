#!/usr/bin/env python3
"""Install or verify the AI SDLC Loop skill package."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
import shutil
import sys
import tempfile
from pathlib import Path

PROFILES = {"codex-project": Path(".agents/skills"), "claude-code-project": Path(".claude/skills")}
SKILLS = (
    "ai-sdlc",
    "ai-sdlc-specify",
    "ai-sdlc-implement",
    "ai-sdlc-verify",
    "ai-sdlc-commit",
    "ai-sdlc-approvals-sandbox",
    "ai-sdlc-branching",
    "ai-sdlc-test-cases",
    "ai-sdlc-qa",
    "ai-sdlc-validation",
    "ai-sdlc-code-review",
    "ai-sdlc-security-testing",
    "ai-sdlc-commit-prep",
    "ai-sdlc-conventional-commit",
    "ai-sdlc-shared-runtime",
)


def load_codec():
    candidates = (
        Path(__file__).resolve().parent / "toon.py",
        Path(__file__).resolve().parent / "skills" / "ai-sdlc-shared-runtime" / "scripts" / "toon.py",
    )
    path = next((candidate for candidate in candidates if candidate.is_file()), None)
    if path is None:
        raise RuntimeError("AI SDLC Loop TOON codec is missing")
    spec = importlib.util.spec_from_file_location("ai_sdlc_loop_toon", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load TOON codec: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


TOON = load_codec()


class InstallError(RuntimeError):
    pass


def digest_tree(root: Path) -> str:
    digest = hashlib.sha256()
    entries = sorted(root.rglob("*"))
    linked = [path for path in entries if path.is_symlink()]
    if linked:
        raise InstallError(f"skill tree contains a symlink: {linked[0].relative_to(root)}")
    for path in (item for item in entries if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode() + b"\0")
        digest.update(path.read_bytes())
    return "sha256:" + digest.hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    if path.is_symlink():
        raise InstallError(f"install state file is a symlink: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def target_for(args: argparse.Namespace) -> tuple[Path, Path]:
    project = Path(args.project_root).resolve()
    if not project.is_dir():
        raise InstallError(f"project root is not a directory: {project}")
    if args.profile == "agent-project":
        if not args.skills_root:
            raise InstallError("agent-project requires --skills-root")
        relative = Path(args.skills_root)
    else:
        if args.skills_root:
            raise InstallError("named profiles reject --skills-root")
        relative = PROFILES[args.profile]
    if relative.is_absolute() or ".." in relative.parts or not relative.parts:
        raise InstallError("skills root must be a safe project-relative path")
    normalized = relative.as_posix()
    if normalized in {".git", ".ai-sdlc-loop"} or normalized.startswith((".git/", ".ai-sdlc-loop/")):
        raise InstallError("skills root overlaps protected project metadata")
    target = project / relative
    current = project
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise InstallError("skills root contains a symlink")
    resolved = target.resolve(strict=False)
    if project not in resolved.parents:
        raise InstallError("skills root escapes project")
    return project, target


def record_path(project: Path, profile: str) -> Path:
    directory = project
    for part in (".ai-sdlc-loop", "install"):
        directory = directory / part
        if directory.is_symlink():
            raise InstallError(f"install state path contains a symlink: {directory}")
        resolved = directory.resolve(strict=False)
        if project not in resolved.parents:
            raise InstallError("install state path escapes project")
    record = directory / f"{profile}.toon"
    if record.is_symlink():
        raise InstallError(f"install record is a symlink: {record}")
    return record


def verify(args: argparse.Namespace) -> None:
    project, root = target_for(args)
    record = TOON.decode_toon(record_path(project, args.profile).read_text(encoding="utf-8"))
    if not isinstance(record, dict):
        raise InstallError("invalid install record")
    if record.get("schema") != "ai-sdlc-loop-install/v1" or record.get("profile") != args.profile:
        raise InstallError("invalid install record")
    expected = record.get("skills")
    if not isinstance(expected, list) or [item.get("name") for item in expected if isinstance(item, dict)] != list(SKILLS):
        raise InstallError("install record has the wrong Loop skill inventory")
    for item in expected:
        name = item["name"]
        target = root / name
        if not target.is_dir() or digest_tree(target) != item.get("digest"):
            raise InstallError(f"installed skill is missing or drifted: {name}")
    print(f"verified {args.profile}: {len(SKILLS)} Loop skills in {root}")


def install(args: argparse.Namespace) -> None:
    project, root = target_for(args)
    source_root = Path(__file__).resolve().parent / "skills"
    record_file = record_path(project, args.profile)
    verifier_file = record_file.parent / "install.py"
    codec_file = record_file.parent / "toon.py"
    if verifier_file.is_symlink():
        raise InstallError(f"installed verifier is a symlink: {verifier_file}")
    if codec_file.is_symlink():
        raise InstallError(f"installed TOON codec is a symlink: {codec_file}")
    targets = {name: root / name for name in SKILLS}
    if any(target.exists() for target in targets.values()):
        if record_file.exists():
            verify(args)
            return
        occupied = ", ".join(name for name, target in targets.items() if target.exists())
        raise InstallError(f"unmanaged Loop target already exists: {occupied}")
    root.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".ai-sdlc-stage-", dir=root))
    installed: list[Path] = []
    try:
        for name in SKILLS:
            source = source_root / name
            if not source.is_dir():
                raise InstallError(f"packaged skill is missing: {name}")
            shutil.copytree(source, staging / name)
        for name in SKILLS:
            os.replace(staging / name, targets[name])
            installed.append(targets[name])
    except Exception:
        for target in reversed(installed):
            shutil.rmtree(target, ignore_errors=True)
        raise
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    record = {
        "schema": "ai-sdlc-loop-install/v1",
        "profile": args.profile,
        "skills_root": root.relative_to(project).as_posix(),
        "skills": [{"name": name, "digest": digest_tree(targets[name])} for name in SKILLS],
    }
    try:
        atomic_write(record_file, TOON.encode_toon(record).encode("utf-8"))
        atomic_write(verifier_file, Path(__file__).resolve().read_bytes())
        atomic_write(codec_file, (source_root / "ai-sdlc-shared-runtime" / "scripts" / "toon.py").read_bytes())
    except Exception:
        for target in targets.values():
            shutil.rmtree(target, ignore_errors=True)
        for state_file in (record_file, verifier_file, codec_file):
            if state_file.exists() and not state_file.is_symlink():
                state_file.unlink()
        raise
    print(f"installed {args.profile}: {len(SKILLS)} Loop skills in {root}")


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(
        description=__doc__,
        epilog="profiles: codex-project, claude-code-project, agent-project (requires --skills-root)",
    )
    sub = value.add_subparsers(dest="action", required=True)
    for action in ("install", "verify"):
        command = sub.add_parser(action)
        command.add_argument("profile", choices=(*PROFILES, "agent-project"))
        command.add_argument("--project-root", default=".")
        command.add_argument("--skills-root")
    # Preserve the one-command `install.py PROFILE` interface.
    return value


def normalize_argv(argv: list[str]) -> list[str]:
    if argv and argv[0] in (*PROFILES, "agent-project"):
        return ["install", *argv]
    return argv


def main() -> int:
    args = parser().parse_args(normalize_argv(sys.argv[1:]))
    try:
        (verify if args.action == "verify" else install)(args)
    except (InstallError, OSError, RuntimeError, ValueError, TypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
