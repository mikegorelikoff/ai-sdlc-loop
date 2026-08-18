#!/usr/bin/env python3
"""Explore and revalidate one guided AI SDLC Loop route."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

_SHARED = Path(__file__).resolve().parents[2] / "ai-sdlc-loop-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_toon import ToonDecodeError, decode_toon, encode_toon

SCHEMA = "ai-sdlc-loop-flow/v1"
APPLY_SCHEMA = "ai-sdlc-loop-flow-apply/v1"

ROUTES = (
    (("doctor", "diagnos", "health", "install drift"), "diagnose", "ai-sdlc-loop-doctor"),
    (("release", "ship", "publish"), "release", "ai-sdlc-loop-release-readiness"),
    (("commit",), "commit", "ai-sdlc-loop-commit-prep"),
    (("security", "owasp", "authz", "secret"), "security", "ai-sdlc-loop-security-testing"),
    (("review", "diff", "pull request", " pr "), "review", "ai-sdlc-loop-code-review"),
    (("test case", "test plan", "coverage"), "test-design", "ai-sdlc-loop-test-cases"),
    (("verify", "validate", "regression", "smoke"), "verify", "ai-sdlc-loop-verify"),
    (("implement", "build", "fix", "change", "refactor"), "implement", "ai-sdlc-loop-implement"),
    (("spec", "requirement", "scope", "design"), "specify", "ai-sdlc-loop-specify"),
)


def digest(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def repository_identity(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], cwd=root, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False,
    )
    return Path(result.stdout.strip()).resolve().as_posix() if result.returncode == 0 else root.as_posix()


def select_route(intent: str) -> tuple[str, str]:
    normalized = " " + " ".join(intent.lower().split()) + " "
    for tokens, stage, skill in ROUTES:
        if any(token in normalized for token in tokens):
            return stage, skill
    return "orchestrate", "ai-sdlc-loop-orchestrate"


def lifecycle_state(root: Path, feature: str) -> tuple[str, list[str]]:
    directory = root
    for part in (".ai-sdlc-loop", feature):
        directory = directory / part
        if directory.is_symlink():
            raise ValueError("feature state path must not contain symlinks")
    path = directory / "state.toon"
    if path.is_symlink():
        raise ValueError("feature state must not be a symlink")
    if not path.is_file():
        return "not-started", []
    value = decode_toon(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("schema") != "ai-sdlc-loop/v1" or value.get("feature") != feature:
        raise ValueError("feature state has an unsupported or mismatched contract")
    stage = value.get("stage")
    if stage not in {"specified", "verified", "verification-failed"}:
        raise ValueError(f"unsupported lifecycle stage: {stage}")
    relative = path.relative_to(root).as_posix()
    return str(stage), [f"{relative}:{digest(path.read_text(encoding='utf-8'))}"]


def resume_route(stage: str, selected_stage: str, selected_skill: str) -> tuple[str, str]:
    if selected_stage != "implement":
        return selected_stage, selected_skill
    if stage == "not-started":
        return "specify", "ai-sdlc-loop-specify"
    if stage == "verification-failed":
        return "verify", "ai-sdlc-loop-verify"
    if stage == "verified":
        return "commit", "ai-sdlc-loop-commit-prep"
    return selected_stage, selected_skill


def skill_root(root: Path, skill: str) -> Path | None:
    packaged = Path(__file__).resolve().parents[2]
    for index, candidate in enumerate((
        root / ".agents" / "skills" / skill,
        root / ".claude" / "skills" / skill,
        root / "skills" / skill,
        packaged / skill,
    )):
        if index < 3:
            current = root
            unsafe = False
            for part in candidate.relative_to(root).parts:
                current = current / part
                if current.is_symlink():
                    unsafe = True
                    break
            if unsafe:
                continue
        if candidate.is_symlink():
            continue
        router = candidate / "SKILL.md"
        manifest = candidate / "steps/manifest.toon"
        if not router.is_symlink() and not manifest.is_symlink() and router.is_file() and manifest.is_file():
            return candidate.resolve()
    return None


def source_evidence(path: Path | None) -> list[str]:
    if path is None:
        return []
    result = []
    for relative in ("SKILL.md", "steps/manifest.toon"):
        item = path / relative
        result.append(f"{path.name}/{relative}:{digest(item.read_text(encoding='utf-8'))}")
    return result


def build_card(root: Path, intent: str, feature: str, rigor: str) -> dict[str, object]:
    if not feature or any(char not in "abcdefghijklmnopqrstuvwxyz0123456789-" for char in feature) or feature.startswith("-") or feature.endswith("-"):
        raise ValueError("feature must be a lowercase kebab-case slug")
    normalized = " ".join(intent.split())
    if not normalized:
        raise ValueError("intent must not be empty")
    current_stage, state_sources = lifecycle_state(root, feature)
    stage, skill = resume_route(current_stage, *select_route(normalized))
    owner = skill_root(root, skill)
    blockers = [] if owner else [f"missing-owning-skill:{skill}"]
    if stage == "verify" and current_stage not in {"specified", "verification-failed"}:
        blockers.append("verification-requires-current-specification")
    if stage == "commit" and current_stage != "verified":
        blockers.append("commit-requires-current-passing-evidence")
    writes = [] if blockers or stage in {"diagnose", "review", "security"} else [f".ai-sdlc-loop/{feature}/"]
    semantic: dict[str, object] = {
        "schema": SCHEMA,
        "feature": feature,
        "intent": normalized,
        "rigor": rigor,
        "repository": repository_identity(root),
        "lifecycle_stage": current_stage,
        "stage": stage,
        "owning_skill": skill,
        "sources": state_sources + source_evidence(owner),
        "planned_writes": writes,
        "blockers": blockers,
    }
    semantic["fingerprint"] = digest(encode_toon(semantic))
    return semantic


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="command", required=True)
    explore = sub.add_parser("explore", help="emit a read-only decision card")
    explore.add_argument("--root", type=Path, default=Path.cwd())
    explore.add_argument("--intent", required=True)
    explore.add_argument("--feature", required=True)
    modes = explore.add_mutually_exclusive_group()
    modes.add_argument("--quick-flow", action="store_true")
    modes.add_argument("--full-flow", action="store_true")
    explore.add_argument("--format", choices=("toon", "markdown"), default="toon")
    apply = sub.add_parser("apply", help="revalidate one Explore card and select its owner")
    apply.add_argument("--root", type=Path, default=Path.cwd())
    apply.add_argument("--card", required=True, help="TOON card path or - for stdin")
    apply.add_argument("--execute", action="store_true", help="confirm the handoff selection; performs no owner action")
    apply.add_argument("--approve", action="store_true", help="explicitly approve the selected handoff")
    return result


def markdown(card: dict[str, object]) -> str:
    return (
        "# Loop Flow Decision\n\n"
        f"- Stage: `{card['stage']}`\n- Owner: `{card['owning_skill']}`\n"
        f"- Rigor: `{card['rigor']}`\n- Fingerprint: `{card['fingerprint']}`\n"
        f"- Blockers: `{', '.join(card['blockers']) if card['blockers'] else 'none'}`\n"
    )


def main() -> int:
    args = parser().parse_args()
    root = args.root.resolve()
    try:
        if not root.is_dir():
            raise ValueError("root must be an existing directory")
        if args.command == "explore":
            rigor = "full" if args.full_flow else "quick" if args.quick_flow else "default"
            card = build_card(root, args.intent, args.feature, rigor)
            print(encode_toon(card) if args.format == "toon" else markdown(card), end="")
            return 2 if card["blockers"] else 0
        payload = sys.stdin.read() if args.card == "-" else Path(args.card).read_text(encoding="utf-8")
        accepted = decode_toon(payload)
        if not isinstance(accepted, dict) or accepted.get("schema") != SCHEMA:
            raise ValueError(f"card must use {SCHEMA}")
        current = build_card(root, str(accepted.get("intent", "")), str(accepted.get("feature", "")), str(accepted.get("rigor", "default")))
        if accepted.get("fingerprint") != current["fingerprint"]:
            raise ValueError("FLOW_ROUTE_DRIFT: Explore inputs changed; run Explore again")
        if current["blockers"]:
            raise ValueError("; ".join(current["blockers"]))
        if args.execute and not args.approve:
            raise ValueError("FLOW_APPROVAL_REQUIRED: --execute requires --approve")
        result = {
            "schema": APPLY_SCHEMA,
            "status": "selected" if args.execute else "verified",
            "decision_fingerprint": current["fingerprint"],
            "owning_skill": current["owning_skill"],
            "owner_action_executed": False,
        }
        print(encode_toon(result), end="")
        return 0
    except (OSError, ValueError, TypeError, ToonDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
