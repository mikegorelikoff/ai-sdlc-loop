"""AI SDLC Loop tests."""

import sys
from pathlib import Path

_LOOP_DIR = Path(__file__).resolve().parent.parent
if str(_LOOP_DIR) not in sys.path:
    sys.path.insert(0, str(_LOOP_DIR))
