"""Include owning Doctor mutation suite in the product regression entrypoint."""
import importlib.util
import sys
from pathlib import Path

def load_tests(loader, tests, pattern):
    root=Path(__file__).resolve().parents[1]
    path=root/'skills/ai-sdlc-loop-doctor/tests/test_framework.py'
    spec=importlib.util.spec_from_file_location('owning_framework_doctor_tests',path)
    module=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=module
    spec.loader.exec_module(module)
    return loader.loadTestsFromModule(module)
