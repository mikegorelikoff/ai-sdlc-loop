#!/usr/bin/env python3
"""Run the owning hunter through the canonical shared engine."""
import sys
from pathlib import Path
sys.dont_write_bytecode = True
SKILL = Path(__file__).resolve().parents[1]
_SHARED = Path(__file__).resolve().parents[2] / "ai-sdlc-loop-shared-runtime" / "scripts"
if _SHARED.is_dir() and str(_SHARED) not in sys.path:
    sys.path.insert(0, str(_SHARED))
try:
    import usage_journal
except ImportError:
    usage_journal = None

from ai_sdlc_hunters import main

if __name__ == "__main__":
    if usage_journal:
        with usage_journal.track_skill("ai-sdlc-loop-blind-case-hunter", trigger="user"):
            raise SystemExit(main("blind-case-hunter", SKILL))
    else:
        raise SystemExit(main("blind-case-hunter", SKILL))
