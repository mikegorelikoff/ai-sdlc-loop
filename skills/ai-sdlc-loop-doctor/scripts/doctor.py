#!/usr/bin/env python3
"""Diagnose AI SDLC Loop installations and preview local upgrade plans."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path

_SHARED = Path(__file__).resolve().parents[2] / "ai-sdlc-loop-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_toon import ToonDecodeError, decode_toon, encode_toon

REPORT_SCHEMA = "ai-sdlc-loop-doctor-report/v1"
PLAN_SCHEMA = "ai-sdlc-loop-upgrade-plan/v1"
PROFILES = {"codex-project": Path(".agents/skills"), "claude-code-project": Path(".claude/skills")}
SKILLS = (
    "ai-sdlc-loop-flow", "ai-sdlc-loop-doctor", "ai-sdlc-loop-orchestrate",
    "ai-sdlc-loop-specify", "ai-sdlc-loop-implement", "ai-sdlc-loop-verify",
    "ai-sdlc-loop-commit", "ai-sdlc-loop-approvals-sandbox", "ai-sdlc-loop-branching",
    "ai-sdlc-loop-test-cases", "ai-sdlc-loop-qa", "ai-sdlc-loop-requirements-review",
    "ai-sdlc-loop-validation", "ai-sdlc-loop-code-review", "ai-sdlc-loop-security-testing",
    "ai-sdlc-loop-commit-prep", "ai-sdlc-loop-conventional-commit",
    "ai-sdlc-loop-release-readiness", "ai-sdlc-loop-shared-runtime",
)


def digest_tree(root: Path) -> str:
    if root.is_symlink():
        raise ValueError(f"symlink skill root: {root}")
    digest = hashlib.sha256()
    entries = sorted(root.rglob("*"))
    if any(path.is_symlink() for path in entries):
        raise ValueError(f"symlink in skill tree: {root}")
    for path in (item for item in entries if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode() + b"\0")
        digest.update(path.read_bytes())
    return "sha256:" + digest.hexdigest()


def fingerprint(value: dict[str, object]) -> str:
    return "sha256:" + hashlib.sha256(encode_toon(value).encode("utf-8")).hexdigest()


def check(code: str, passed: bool, evidence: str, remediation: str) -> dict[str, str]:
    return {
        "code": code,
        "status": "pass" if passed else "fail",
        "evidence": evidence,
        "remediation": "" if passed else remediation,
    }


def target_root(project: Path, profile: str, skills_root: str | None) -> Path:
    if profile == "agent-project":
        if not skills_root:
            raise ValueError("agent-project requires --skills-root")
        relative = Path(skills_root)
    else:
        if skills_root:
            raise ValueError("named profiles reject --skills-root")
        relative = PROFILES[profile]
    if relative.is_absolute() or ".." in relative.parts or not relative.parts:
        raise ValueError("skills root must be a safe project-relative path")
    target = project
    for part in relative.parts:
        target = target / part
        if target.is_symlink():
            raise ValueError("skills root contains a symlink")
    target.resolve(strict=False).relative_to(project)
    return target


def read_record(project: Path, profile: str) -> tuple[dict[str, object] | None, str]:
    directory = project
    for part in (".ai-sdlc-loop", "install"):
        directory = directory / part
        if directory.is_symlink():
            return None, directory.as_posix()
    path = directory / f"{profile}.toon"
    if path.is_symlink() or not path.is_file():
        return None, path.as_posix()
    try:
        value = decode_toon(path.read_text(encoding="utf-8"))
    except (OSError, ToonDecodeError):
        return None, path.as_posix()
    return value if isinstance(value, dict) else None, path.as_posix()


def diagnose(project: Path, profile: str, skills_root: str | None) -> dict[str, object]:
    root = target_root(project, profile, skills_root)
    record, record_name = read_record(project, profile)
    checks = [
        check("python-version", sys.version_info >= (3, 9), sys.version.split()[0], "Install Python 3.9 or newer."),
        check("git-available", shutil.which("git") is not None, shutil.which("git") or "not found", "Install Git and expose it on PATH."),
        check("install-record", record is not None, record_name, "Reinstall Loop with the intended profile."),
    ]
    record_ok = bool(record and record.get("schema") == "ai-sdlc-loop-install/v1" and record.get("profile") == profile)
    checks.append(check("record-contract", record_ok, f"schema={record.get('schema') if record else 'missing'};profile={record.get('profile') if record else 'missing'}", "Restore a valid profile-bound TOON install record."))
    expected_root = root.relative_to(project).as_posix()
    root_ok = bool(record_ok and record.get("skills_root") == expected_root)
    checks.append(check("record-skills-root", root_ok, f"expected={expected_root};recorded={record.get('skills_root') if record else 'missing'}", "Reinstall with the intended profile and project-relative skills root."))
    recorded = record.get("skills") if record_ok else []
    names = [item.get("name") for item in recorded if isinstance(item, dict)] if isinstance(recorded, list) else []
    checks.append(check("exact-inventory", names == list(SKILLS), f"expected={len(SKILLS)};recorded={len(names)}", "Install the complete current Loop package."))
    present = sorted(path.name for path in root.glob("ai-sdlc-loop-*") if path.is_dir()) if root.is_dir() else []
    unexpected = sorted(set(present) - set(SKILLS))
    missing = sorted(set(SKILLS) - set(present))
    checks.append(check("filesystem-inventory", not unexpected and not missing, f"missing={','.join(missing) or 'none'};unexpected={','.join(unexpected) or 'none'}", "Review unexpected Loop-owned directories and restore the exact package inventory."))
    drift: list[str] = []
    manifest_errors: list[str] = []
    expected_digests = {item.get("name"): item.get("digest") for item in recorded if isinstance(item, dict)} if isinstance(recorded, list) else {}
    for name in SKILLS:
        skill = root / name
        if not skill.is_dir():
            drift.append(f"{name}:missing")
            continue
        try:
            if digest_tree(skill) != expected_digests.get(name):
                drift.append(f"{name}:digest")
        except ValueError:
            drift.append(f"{name}:symlink")
        manifest = skill / "steps/manifest.toon"
        try:
            value = decode_toon(manifest.read_text(encoding="utf-8"))
            if not isinstance(value, dict) or value.get("skill") != name or value.get("schema") not in {"ai-sdlc-loop-skill-steps/v1", "ai-sdlc-skill-steps/v2"} or not isinstance(value.get("steps"), list) or not value["steps"]:
                manifest_errors.append(f"{name}:invalid")
        except (OSError, ToonDecodeError):
            manifest_errors.append(f"{name}:unreadable")
    checks.append(check("skill-digests", not drift, ",".join(drift) or "all-match", "Preserve local edits, then reinstall or restore drifted skills."))
    checks.append(check("step-manifests", not manifest_errors, ",".join(manifest_errors) or "all-valid", "Restore the named canonical step manifests."))
    runtime = root / "ai-sdlc-loop-shared-runtime/scripts/loop.py"
    checks.append(check("shared-runtime", runtime.is_file() and not runtime.is_symlink(), runtime.as_posix(), "Restore ai-sdlc-loop-shared-runtime."))
    report: dict[str, object] = {
        "schema": REPORT_SCHEMA,
        "profile": profile,
        "project_root": project.as_posix(),
        "skills_root": root.relative_to(project).as_posix(),
        "status": "healthy" if all(item["status"] == "pass" for item in checks) else "unhealthy",
        "checks": checks,
    }
    report["fingerprint"] = fingerprint(report)
    return report


def upgrade_plan(project: Path, profile: str, skills_root: str | None, package: Path) -> dict[str, object]:
    installed = target_root(project, profile, skills_root)
    source = package.resolve() / "skills"
    if not source.is_dir():
        raise ValueError("package root must contain skills/")
    candidate = sorted(path.name for path in source.glob("ai-sdlc-loop-*") if path.is_dir())
    if candidate != sorted(SKILLS):
        raise ValueError("candidate package must contain the exact Loop skill inventory")
    changes = []
    for name in SKILLS:
        before = installed / name
        after = source / name
        if not after.is_dir() or after.is_symlink():
            raise ValueError(f"candidate package is missing {name}")
        before_digest = digest_tree(before) if before.is_dir() else ""
        after_digest = digest_tree(after)
        changes.append({
            "skill": name,
            "action": "add" if not before_digest else "unchanged" if before_digest == after_digest else "modify",
            "before_digest": before_digest,
            "after_digest": after_digest,
        })
    extra = sorted(path.name for path in installed.glob("ai-sdlc-loop-*") if path.is_dir() and path.name not in SKILLS)
    changes.extend({"skill": name, "action": "remove", "before_digest": digest_tree(installed / name), "after_digest": ""} for name in extra)
    plan: dict[str, object] = {
        "schema": PLAN_SCHEMA,
        "profile": profile,
        "project_root": project.as_posix(),
        "package_root": package.resolve().as_posix(),
        "changes": changes,
        "apply_authorized": False,
    }
    plan["fingerprint"] = fingerprint(plan)
    return plan


def markdown(value: dict[str, object]) -> str:
    if value["schema"] == REPORT_SCHEMA:
        lines = ["# Loop Installation Doctor", "", f"Status: **{value['status']}**", f"Fingerprint: `{value['fingerprint']}`", "", "| Check | Status | Evidence |", "| --- | --- | --- |"]
        lines.extend(f"| `{item['code']}` | {item['status']} | {item['evidence']} |" for item in value["checks"])
        return "\n".join(lines) + "\n"
    lines = ["# Loop Upgrade Plan", "", f"Fingerprint: `{value['fingerprint']}`", "", "| Skill | Action |", "| --- | --- |"]
    lines.extend(f"| `{item['skill']}` | {item['action']} |" for item in value["changes"])
    return "\n".join(lines) + "\n"


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="command", required=True)
    for name in ("check", "upgrade-plan"):
        command = sub.add_parser(name)
        command.add_argument("--project-root", type=Path, default=Path.cwd())
        command.add_argument("--profile", choices=(*PROFILES, "agent-project"), required=True)
        command.add_argument("--skills-root")
        command.add_argument("--format", choices=("toon", "markdown"), default="toon")
        command.add_argument("--quick-flow", action="store_true")
        command.add_argument("--full-flow", action="store_true")
        if name == "upgrade-plan":
            command.add_argument("--package-root", type=Path, required=True)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        project = args.project_root.resolve(strict=True)
        if not project.is_dir():
            raise ValueError("project root must be a directory")
        value = diagnose(project, args.profile, args.skills_root) if args.command == "check" else upgrade_plan(project, args.profile, args.skills_root, args.package_root)
        print(encode_toon(value) if args.format == "toon" else markdown(value), end="")
        return 2 if value.get("status") == "unhealthy" else 0
    except (OSError, ValueError, TypeError, ToonDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
