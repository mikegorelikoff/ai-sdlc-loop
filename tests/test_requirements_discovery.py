"""Include the installed discovery package's behavior suite in Loop CI."""

import importlib.util
from pathlib import Path

_path = (Path(__file__).resolve().parents[1] / "skills" /
         "ai-sdlc-loop-requirements-discovery/tests/test_scripts.py")
_spec = importlib.util.spec_from_file_location("loop_discovery_tests", _path)
_tests = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_tests)
DiscoveryTests = _tests.DiscoveryTests
