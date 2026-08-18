#!/usr/bin/env python3
"""Shared safe output helpers for compact Loop review artifacts."""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

from toon import encode_toon


FEATURE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")


def row(value: str, fields: tuple[str, ...]) -> dict[str, str]:
    parts = [part.strip() for part in value.split("|", len(fields) - 1)]
    if len(parts) != len(fields) or any(not part for part in parts):
        raise argparse.ArgumentTypeError("value must be " + "|".join(fields))
    return dict(zip(fields, parts))


def safe_output(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or path.suffix != ".toon":
        raise argparse.ArgumentTypeError("output must be a safe project-relative .toon path")
    return path


def validate_feature(value: str) -> str:
    if not FEATURE.fullmatch(value):
        raise argparse.ArgumentTypeError("feature must be a lowercase hyphenated slug")
    return value


def write_or_print(artifact: dict[str, Any], output: Path | None) -> None:
    content = encode_toon(artifact)
    if output is None:
        print(content, end="")
        return
    root = Path.cwd().resolve()
    target = (root / output).resolve(strict=False)
    if target == root or root not in target.parents:
        raise ValueError("output escapes the project root")
    current = root
    for part in output.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("output path contains a symlink")
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def finish(artifact: dict[str, Any], output: Path | None) -> int:
    try:
        write_or_print(artifact, output)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    return 0
