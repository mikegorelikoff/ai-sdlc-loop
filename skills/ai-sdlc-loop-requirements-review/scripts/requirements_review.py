#!/usr/bin/env python3
"""Create a canonical TOON requirements gap review."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SHARED = Path(__file__).resolve().parents[2] / "ai-sdlc-loop-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from review_artifact import finish, row, safe_output, validate_feature  # noqa: E402


FIELDS = ("id", "severity", "category", "evidence", "impact", "resolution")


def finding(value: str) -> dict[str, str]:
    result = row(value, FIELDS)
    if result["severity"] not in {"critical", "high", "medium", "low"}:
        raise argparse.ArgumentTypeError("severity must be critical, high, medium, or low")
    if result["category"] not in {"actor", "workflow", "rule", "acceptance", "scope", "dependency"}:
        raise argparse.ArgumentTypeError("unsupported finding category")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--feature", required=True, type=validate_feature)
    parser.add_argument("--source", action="append", required=True)
    parser.add_argument("--coverage", action="append", default=[])
    parser.add_argument("--missing", action="append", default=[])
    parser.add_argument("--finding", action="append", default=[], type=finding)
    parser.add_argument("--status", choices=("ready", "gaps", "blocked"), required=True)
    parser.add_argument("--output", type=safe_output)
    args = parser.parse_args()
    severe = any(item["severity"] in {"critical", "high"} for item in args.finding)
    if args.status == "ready" and (args.missing or severe):
        parser.error("ready requires no missing coverage or critical/high finding")
    artifact = {
        "schema": "ai-sdlc-loop-requirements-review/v1",
        "feature": args.feature,
        "status": args.status,
        "sources": args.source,
        "coverage": args.coverage,
        "missing": args.missing,
        "findings": args.finding,
    }
    return finish(artifact, args.output)


if __name__ == "__main__":
    raise SystemExit(main())
