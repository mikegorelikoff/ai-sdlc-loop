#!/usr/bin/env python3
"""Compatibility entrypoint for the shared AI SDLC Loop runtime."""

from __future__ import annotations

import runpy
from pathlib import Path


RUNTIME = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts" / "loop.py"
if not RUNTIME.is_file():
    raise SystemExit(f"error: AI SDLC Loop shared runtime is missing: {RUNTIME}")
runpy.run_path(str(RUNTIME), run_name="__main__")
