#!/usr/bin/env python3
"""Run the owning hunter through the canonical shared engine."""
import sys
from pathlib import Path
sys.dont_write_bytecode = True
SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL.parent / "ai-sdlc-loop-shared-runtime" / "scripts"))
from ai_sdlc_hunters import main
if __name__ == "__main__":
    raise SystemExit(main("blind-case-hunter", SKILL))
