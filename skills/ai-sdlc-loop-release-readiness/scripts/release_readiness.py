#!/usr/bin/env python3
"""Create a canonical TOON release-readiness decision."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_SHARED = Path(__file__).resolve().parents[2] / "ai-sdlc-loop-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from review_artifact import finish, row, safe_output, validate_feature  # noqa: E402


def commit(value: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{7,64}", value):
        raise argparse.ArgumentTypeError("commit must be a lowercase hexadecimal Git identity")
    return value


def gate(value: str) -> dict[str, str]:
    result = row(value, ("name", "status", "evidence"))
    if result["status"] not in {"passed", "failed", "planned", "skipped"}:
        raise argparse.ArgumentTypeError("gate status must be passed, failed, planned, or skipped")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--feature", required=True, type=validate_feature)
    parser.add_argument("--release", required=True)
    parser.add_argument("--commit", required=True, type=commit)
    parser.add_argument("--gate", action="append", required=True, type=gate)
    parser.add_argument("--blocker", action="append", default=[])
    parser.add_argument("--residual-risk", action="append", default=[])
    parser.add_argument("--status", choices=("ready", "blocked"), required=True)
    parser.add_argument("--output", type=safe_output)
    args = parser.parse_args()
    if args.status == "ready" and (args.blocker or any(item["status"] != "passed" for item in args.gate)):
        parser.error("ready requires every gate passed and no blocker")
    artifact = {
        "schema": "ai-sdlc-loop-release-readiness/v1",
        "feature": args.feature,
        "release": args.release,
        "commit": args.commit,
        "status": args.status,
        "gates": args.gate,
        "blockers": args.blocker,
        "residual_risks": args.residual_risk,
    }
    return finish(artifact, args.output)


if __name__ == "__main__":
    raise SystemExit(main())
