#!/usr/bin/env python3
"""Deterministic local gates for the AI SDLC Loop skill."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shlex
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SHARED_SCRIPTS = Path(__file__).resolve().parents[2] / "ai-sdlc-loop-shared-runtime" / "scripts"
if not SHARED_SCRIPTS.is_dir():
    raise ImportError(f"AI SDLC Loop shared runtime is missing: {SHARED_SCRIPTS}")
sys.path.insert(0, str(SHARED_SCRIPTS))
from toon import ToonDecodeError, decode_toon, encode_toon

SCHEMA = "ai-sdlc-loop/v1"
PROMOTION_SCHEMA = "ai-sdlc-harness-promotion/v1"
FEATURE_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")
SECRET_RE = re.compile(
    r"(?i)(authorization\s*[:=]\s*bearer\s+|token\s*[:=]\s*|password\s*[:=]\s*|secret\s*[:=]\s*)([^\s\"']+)"
)
PRIVATE_KEY_RE = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S)


class LoopError(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return encode_toon(value).encode("utf-8")


def fingerprint(value: dict[str, Any], omit: str = "fingerprint") -> str:
    payload = {key: item for key, item in value.items() if key != omit}
    return "sha256:" + hashlib.sha256(canonical(payload)).hexdigest()


def atomic_toon(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(canonical(value))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def load_toon(path: Path) -> dict[str, Any]:
    try:
        value = decode_toon(path.read_text(encoding="utf-8"))
    except (OSError, ToonDecodeError, ValueError, TypeError) as exc:
        raise LoopError(f"cannot read valid TOON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise LoopError(f"expected a TOON mapping in {path}")
    return value


def normalize_request(value: str) -> str:
    normalized = " ".join(value.split())
    if not normalized:
        raise LoopError("request must not be empty")
    return normalized


def validate_feature(value: str) -> str:
    if not FEATURE_RE.fullmatch(value):
        raise LoopError("feature must match [a-z0-9][a-z0-9-]{0,62}")
    return value


def project_root(value: str) -> Path:
    root = Path(value).resolve()
    if not root.is_dir():
        raise LoopError(f"project root is not a directory: {root}")
    return root


def state_dir(root: Path, feature: str) -> Path:
    directory = root
    for part in (".ai-sdlc-loop", validate_feature(feature)):
        directory = directory / part
        if directory.is_symlink():
            raise LoopError(f"Loop state path contains a symlink: {directory}")
        resolved = directory.resolve(strict=False)
        if root not in resolved.parents:
            raise LoopError(f"Loop state path escapes project root: {directory}")
    return directory


def state_path(root: Path, feature: str, *parts: str) -> Path:
    path = state_dir(root, feature)
    for part in parts:
        if not part or part in {".", ".."} or "/" in part or "\\" in part:
            raise LoopError(f"invalid Loop state component: {part}")
        path = path / part
        if path.is_symlink():
            raise LoopError(f"Loop state path contains a symlink: {path}")
        resolved = path.resolve(strict=False)
        if root not in resolved.parents:
            raise LoopError(f"Loop state path escapes project root: {path}")
    return path


def safe_relative(root: Path, value: str, *, allow_state: bool = False) -> str:
    candidate = Path(value)
    if candidate.is_absolute() or not candidate.parts or ".." in candidate.parts or "\x00" in value:
        raise LoopError(f"unsafe relative path: {value}")
    normalized = candidate.as_posix()
    if not normalized or normalized == ".git" or normalized.startswith(".git/"):
        raise LoopError(f"path overlaps Git metadata: {value}")
    if not allow_state and (normalized == ".ai-sdlc-loop" or normalized.startswith(".ai-sdlc-loop/")):
        raise LoopError(f"path overlaps Loop state: {value}")
    current = root
    for part in Path(normalized).parts:
        current = current / part
        if current.is_symlink():
            raise LoopError(f"path contains a symlink: {value}")
    resolved = (root / normalized).resolve(strict=False)
    if resolved != root and root not in resolved.parents:
        raise LoopError(f"path escapes project root: {value}")
    return normalized


def run_git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=False)
    if check and result.returncode:
        raise LoopError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result


def changed_paths(root: Path) -> list[str]:
    if run_git(root, "rev-parse", "--is-inside-work-tree", check=False).returncode:
        raise LoopError("project root must be a Git worktree")
    paths: set[str] = set()
    for args in (("diff", "--name-only", "-z"), ("diff", "--cached", "--name-only", "-z"), ("ls-files", "--others", "--exclude-standard", "-z")):
        result = run_git(root, *args)
        for path in result.stdout.split("\0"):
            if path and not path.startswith(".ai-sdlc-loop/"):
                paths.add(safe_relative(root, path))
    return sorted(paths)


def path_allowed(path: str, allowed: list[str]) -> bool:
    return any(path == item or path.startswith(item.rstrip("/") + "/") for item in allowed)


def file_digest(root: Path, path: str) -> dict[str, Any]:
    target = root / path
    if not target.exists():
        return {"path": path, "kind": "deleted"}
    if not target.is_file():
        raise LoopError(f"changed path is not a regular file: {path}")
    return {"path": path, "kind": "file", "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}


def change_snapshot(root: Path, spec: dict[str, Any]) -> dict[str, Any]:
    paths = changed_paths(root)
    outside = [path for path in paths if not path_allowed(path, spec["allowed_paths"])]
    if outside:
        raise LoopError("changes outside approved paths: " + ", ".join(outside))
    value = {"spec_fingerprint": spec["fingerprint"], "files": [file_digest(root, path) for path in paths]}
    value["fingerprint"] = fingerprint(value)
    return value


def current_spec(root: Path, feature: str) -> dict[str, Any]:
    spec = load_toon(state_path(root, feature, "spec.toon"))
    if spec.get("schema") != SCHEMA or spec.get("feature") != feature:
        raise LoopError("unsupported or mismatched spec")
    if spec.get("fingerprint") != fingerprint(spec):
        raise LoopError("spec fingerprint does not match its content")
    return spec


def require_approval(root: Path, feature: str, action: str, subject: str) -> dict[str, Any]:
    receipt = load_toon(state_path(root, feature, "approvals", f"{action}.toon"))
    if receipt.get("schema") != SCHEMA or receipt.get("action") != action:
        raise LoopError(f"invalid {action} approval receipt")
    if receipt.get("decision") != "approve":
        raise LoopError(f"{action} was not approved")
    if receipt.get("subject_fingerprint") != subject:
        raise LoopError(f"stale or mismatched {action} approval")
    return receipt


def redact(value: str) -> str:
    value = PRIVATE_KEY_RE.sub("[REDACTED PRIVATE KEY]", value)
    return SECRET_RE.sub(lambda match: match.group(1) + "[REDACTED]", value)


def split_command(value: str) -> list[str]:
    argv = shlex.split(value, posix=os.name != "nt")
    if os.name == "nt":
        argv = [item[1:-1] if len(item) >= 2 and item[0] == item[-1] and item[0] in {'"', "'"} else item for item in argv]
    return argv


def cmd_specify(args: argparse.Namespace) -> None:
    root = project_root(args.project_root)
    feature = validate_feature(args.feature)
    allowed = sorted(set(safe_relative(root, value) for value in args.allow))
    if not allowed:
        raise LoopError("at least one --allow path is required")
    spec: dict[str, Any] = {
        "schema": SCHEMA,
        "feature": feature,
        "request": normalize_request(args.request),
        "allowed_paths": allowed,
        "trace_ids": sorted(set(args.trace)),
    }
    spec["fingerprint"] = fingerprint(spec)
    atomic_toon(state_path(root, feature, "spec.toon"), spec)
    atomic_toon(state_path(root, feature, "state.toon"), {"schema": SCHEMA, "feature": feature, "stage": "specified", "spec_fingerprint": spec["fingerprint"]})
    print(spec["fingerprint"])


def cmd_approve(args: argparse.Namespace) -> None:
    root = project_root(args.project_root)
    feature = validate_feature(args.feature)
    if args.action == "implement":
        expected = current_spec(root, feature)["fingerprint"]
    else:
        evidence = load_toon(state_path(root, feature, "evidence.toon"))
        if not evidence.get("ready"):
            raise LoopError("verification evidence is not ready")
        expected = evidence.get("verified_fingerprint")
    if args.fingerprint != expected:
        raise LoopError(f"fingerprint does not match current {args.action} subject")
    receipt = {
        "schema": SCHEMA,
        "feature": feature,
        "action": args.action,
        "decision": args.decision,
        "reviewer": args.reviewer.strip(),
        "subject_fingerprint": args.fingerprint,
        "recorded_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }
    if not receipt["reviewer"]:
        raise LoopError("reviewer must not be empty")
    atomic_toon(state_path(root, feature, "approvals", f"{args.action}.toon"), receipt)
    print(f"{args.action}: {args.decision}")


def cmd_implement_check(args: argparse.Namespace) -> None:
    root = project_root(args.project_root)
    spec = current_spec(root, validate_feature(args.feature))
    require_approval(root, args.feature, "implement", spec["fingerprint"])
    print("implement eligible: " + spec["fingerprint"])


def cmd_verify(args: argparse.Namespace) -> None:
    root = project_root(args.project_root)
    feature = validate_feature(args.feature)
    if args.timeout <= 0:
        raise LoopError("verification timeout must be positive")
    spec = current_spec(root, feature)
    require_approval(root, feature, "implement", spec["fingerprint"])
    snapshot = change_snapshot(root, spec)
    records: list[dict[str, Any]] = []
    ready = True
    for command in args.command:
        argv = split_command(command)
        if not argv:
            raise LoopError("verification command must not be empty")
        try:
            result = subprocess.run(argv, cwd=root, text=True, errors="replace", capture_output=True, timeout=args.timeout, check=False)
            record = {"argv": [redact(item) for item in argv], "exit_code": result.returncode, "timed_out": False, "stdout": redact(result.stdout[-8000:]), "stderr": redact(result.stderr[-8000:])}
            ready = ready and result.returncode == 0
        except (OSError, subprocess.TimeoutExpired) as exc:
            record = {"argv": [redact(item) for item in argv], "exit_code": None, "timed_out": isinstance(exc, subprocess.TimeoutExpired), "stdout": "", "stderr": redact(str(exc))}
            ready = False
        records.append(record)
    evidence: dict[str, Any] = {
        "schema": SCHEMA,
        "feature": feature,
        "spec_fingerprint": spec["fingerprint"],
        "change_fingerprint": snapshot["fingerprint"],
        "changed_files": snapshot["files"],
        "commands": records,
        "ready": ready,
    }
    evidence["verified_fingerprint"] = fingerprint(evidence, "verified_fingerprint")
    atomic_toon(state_path(root, feature, "evidence.toon"), evidence)
    atomic_toon(state_path(root, feature, "state.toon"), {"schema": SCHEMA, "feature": feature, "stage": "verified" if ready else "verification-failed", "spec_fingerprint": spec["fingerprint"], "verified_fingerprint": evidence["verified_fingerprint"], "ready": ready})
    print(evidence["verified_fingerprint"])
    if not ready:
        raise LoopError("one or more verification commands failed")


def cmd_commit(args: argparse.Namespace) -> None:
    root = project_root(args.project_root)
    feature = validate_feature(args.feature)
    spec = current_spec(root, feature)
    evidence = load_toon(state_path(root, feature, "evidence.toon"))
    if not evidence.get("ready") or evidence.get("spec_fingerprint") != spec["fingerprint"]:
        raise LoopError("current passing verification evidence is required")
    if evidence.get("verified_fingerprint") != fingerprint(evidence, "verified_fingerprint"):
        raise LoopError("verification evidence fingerprint is invalid")
    snapshot = change_snapshot(root, spec)
    if snapshot["fingerprint"] != evidence.get("change_fingerprint"):
        raise LoopError("changes drifted after verification")
    require_approval(root, feature, "commit", evidence["verified_fingerprint"])
    paths = [item["path"] for item in evidence["changed_files"]]
    if not paths:
        raise LoopError("there are no approved changes to commit")
    prior_index = run_git(root, "write-tree").stdout.strip()
    run_git(root, "add", "--", *paths)
    message = f"{args.message}\n\nAI-SDLC-Loop-Feature: {feature}\nAI-SDLC-Loop-Verified: {evidence['verified_fingerprint']}"
    result = run_git(root, "commit", "-m", message, check=False)
    if result.returncode:
        run_git(root, "read-tree", prior_index, check=False)
        raise LoopError(result.stderr.strip() or "git commit failed")
    print(run_git(root, "rev-parse", "HEAD").stdout.strip())


def cmd_promote(args: argparse.Namespace) -> None:
    root = project_root(args.project_root)
    feature = validate_feature(args.feature)
    spec = current_spec(root, feature)
    payload: dict[str, Any] = {
        "schema": PROMOTION_SCHEMA,
        "source_schema": SCHEMA,
        "feature": feature,
        "request": spec["request"],
        "allowed_paths": spec["allowed_paths"],
        "trace_ids": spec["trace_ids"],
        "spec_fingerprint": spec["fingerprint"],
    }
    for name in ("state", "evidence"):
        path = state_path(root, feature, f"{name}.toon")
        if path.exists():
            payload[name] = load_toon(path)
    approvals = {}
    for action in ("implement", "commit"):
        path = state_path(root, feature, "approvals", f"{action}.toon")
        if path.exists():
            approvals[action] = load_toon(path)
    payload["approvals"] = approvals
    output = Path(args.output)
    if output.suffix != ".toon":
        raise LoopError("promotion output must use a .toon extension")
    if not output.is_absolute():
        output = root / safe_relative(root, args.output, allow_state=True)
    atomic_toon(output, payload)
    print(output)


def cmd_status(args: argparse.Namespace) -> None:
    root = project_root(args.project_root)
    feature = validate_feature(args.feature)
    result = {"spec": load_toon(state_path(root, feature, "spec.toon")), "state": load_toon(state_path(root, feature, "state.toon"))}
    print(encode_toon(result), end="")


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--project-root", default=".")
    commands = value.add_subparsers(dest="command_name", required=True)
    specify = commands.add_parser("specify", help="persist a bounded deterministic specification")
    specify.add_argument("--feature", required=True)
    specify.add_argument("--request", required=True)
    specify.add_argument("--allow", action="append", required=True)
    specify.add_argument("--trace", action="append", default=[])
    specify.set_defaults(handler=cmd_specify)
    approve = commands.add_parser("approve", help="record an explicit reviewer decision")
    approve.add_argument("--feature", required=True)
    approve.add_argument("--action", choices=("implement", "commit"), required=True)
    approve.add_argument("--decision", choices=("approve", "reject"), required=True)
    approve.add_argument("--fingerprint", required=True)
    approve.add_argument("--reviewer", required=True)
    approve.set_defaults(handler=cmd_approve)
    implement = commands.add_parser("implement-check", help="verify Implement authority")
    implement.add_argument("--feature", required=True)
    implement.set_defaults(handler=cmd_implement_check)
    verify = commands.add_parser("verify", help="run explicit checks and persist evidence")
    verify.add_argument("--feature", required=True)
    verify.add_argument("--command", action="append", required=True)
    verify.add_argument("--timeout", type=int, default=300)
    verify.set_defaults(handler=cmd_verify)
    commit = commands.add_parser("commit", help="create one separately approved commit")
    commit.add_argument("--feature", required=True)
    commit.add_argument("--message", required=True)
    commit.set_defaults(handler=cmd_commit)
    promote = commands.add_parser("promote", help="emit a Harness-compatible artifact")
    promote.add_argument("--feature", required=True)
    promote.add_argument("--output", required=True)
    promote.set_defaults(handler=cmd_promote)
    status = commands.add_parser("status", help="show current local Loop state")
    status.add_argument("--feature", required=True)
    status.set_defaults(handler=cmd_status)
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        args.handler(args)
    except LoopError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
