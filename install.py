#!/usr/bin/env python3
"""Install or verify the single AI SDLC Loop skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

PROFILES = {"codex-project": Path(".agents/skills"), "claude-code-project": Path(".claude/skills")}


class InstallError(RuntimeError):
    pass


def digest_tree(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
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
    record = directory / f"{profile}.json"
    if record.is_symlink():
        raise InstallError(f"install record is a symlink: {record}")
    return record


def verify(args: argparse.Namespace) -> None:
    project, root = target_for(args)
    target = root / "ai-sdlc"
    record = json.loads(record_path(project, args.profile).read_text(encoding="utf-8"))
    if record.get("schema") != "ai-sdlc-loop-install/v1" or record.get("profile") != args.profile:
        raise InstallError("invalid install record")
    if not target.is_dir() or digest_tree(target) != record.get("digest"):
        raise InstallError("installed skill is missing or drifted")
    print(f"verified {args.profile}: {target}")


def install(args: argparse.Namespace) -> None:
    project, root = target_for(args)
    source = Path(__file__).resolve().parent / "skills" / "ai-sdlc"
    target = root / "ai-sdlc"
    record_file = record_path(project, args.profile)
    verifier_file = record_file.parent / "install.py"
    if verifier_file.is_symlink():
        raise InstallError(f"installed verifier is a symlink: {verifier_file}")
    if target.exists():
        if record_file.exists():
            verify(args)
            return
        raise InstallError(f"unmanaged target already exists: {target}")
    root.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".ai-sdlc-stage-", dir=root))
    try:
        shutil.copytree(source, staging / "ai-sdlc")
        os.replace(staging / "ai-sdlc", target)
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    record = {"schema": "ai-sdlc-loop-install/v1", "profile": args.profile, "skills_root": root.relative_to(project).as_posix(), "skill": "ai-sdlc", "digest": digest_tree(target)}
    try:
        atomic_write(record_file, (json.dumps(record, indent=2, sort_keys=True) + "\n").encode())
        atomic_write(verifier_file, Path(__file__).resolve().read_bytes())
    except Exception:
        shutil.rmtree(target, ignore_errors=True)
        for state_file in (record_file, verifier_file):
            if state_file.exists() and not state_file.is_symlink():
                state_file.unlink()
        raise
    print(f"installed {args.profile}: {target}")


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
    except (InstallError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
