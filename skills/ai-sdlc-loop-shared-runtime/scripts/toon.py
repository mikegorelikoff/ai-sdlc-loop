#!/usr/bin/env python3
"""Wrapper around ai_sdlc_toon providing standard TOON codec aliases."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_candidates = [
    _SCRIPTS_DIR,
    _SCRIPTS_DIR.parents[1] / ".agents" / "skills" / "ai-sdlc-loop-shared-runtime" / "scripts" if len(_SCRIPTS_DIR.parents) > 1 else _SCRIPTS_DIR,
    _SCRIPTS_DIR.parents[1] / ".claude" / "skills" / "ai-sdlc-loop-shared-runtime" / "scripts" if len(_SCRIPTS_DIR.parents) > 1 else _SCRIPTS_DIR,
    _SCRIPTS_DIR.parents[1] / "skills" / "ai-sdlc-loop-shared-runtime" / "scripts" if len(_SCRIPTS_DIR.parents) > 1 else _SCRIPTS_DIR,
    _SCRIPTS_DIR.parent / "skills" / "ai-sdlc-loop-shared-runtime" / "scripts",
]
for _cand in _candidates:
    if (_cand / "ai_sdlc_toon.py").is_file():
        if str(_cand) not in sys.path:
            sys.path.insert(0, str(_cand))
        break
else:
    if len(_SCRIPTS_DIR.parents) > 1:
        _project_root = _SCRIPTS_DIR.parents[1]
        for _found in _project_root.glob("**/ai_sdlc_toon.py"):
            if str(_found.parent) not in sys.path:
                sys.path.insert(0, str(_found.parent))
            break

from ai_sdlc_toon import (
    ToonDecodeError,
    decode_toon,
    dump,
    dumps,
    encode_toon,
    load,
    loads,
)

__all__ = [
    "ToonDecodeError",
    "decode_toon",
    "dump",
    "dumps",
    "encode_toon",
    "load",
    "loads",
]
