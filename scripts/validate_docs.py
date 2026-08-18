#!/usr/bin/env python3
"""Validate Loop documentation structure and source contracts."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
INSTALL = "curl -fsSL https://raw.githubusercontent.com/mikegorelikoff/ai-sdlc-loop/v0.2.0/install.sh | sh -s -- codex-project"


def fail(message: str) -> None:
    raise ValueError(message)


def main() -> int:
    try:
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        if not (ROOT / "requirements-docs.lock").is_file():
            fail("hashed documentation dependency lock is missing")
        nav = ("Home:", "Start here:", "How it works:", "Guides:", "Reference:", "Project:")
        positions = [config.index(item) for item in nav]
        if positions != sorted(positions):
            fail("public navigation order changed")
        for relative in ("README.md", "docs/index.md", "docs/start-here.md"):
            if (ROOT / relative).read_text(encoding="utf-8").count(INSTALL) != 1:
                fail(f"primary install command mismatch: {relative}")
        required = ("## Goal", "## When to use it", "## Prerequisites", "## Procedure", "## Verify", "## Troubleshooting", "## Next step")
        for guide in sorted((DOCS / "guides").glob("*.md")):
            text = guide.read_text(encoding="utf-8")
            if any(section not in text for section in required):
                fail(f"guide template incomplete: {guide.relative_to(ROOT)}")
        link_pattern = re.compile(r"\[[^]]*\]\(([^)]+)\)")
        for page in sorted(DOCS.rglob("*.md")):
            for target in link_pattern.findall(page.read_text(encoding="utf-8")):
                clean = target.split("#", 1)[0]
                if not clean or "://" in clean or clean.startswith("mailto:"):
                    continue
                resolved = (page.parent / clean).resolve()
                if not resolved.exists():
                    fail(f"broken local link: {page.relative_to(ROOT)} -> {target}")
        check = subprocess.run(
            [sys.executable, str(DOCS / "scripts/build_catalog.py"), "--check"],
            cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        if check.returncode:
            fail(check.stderr.strip())
    except (OSError, ValueError) as exc:
        print(f"documentation validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"documentation validation passed: {len(list(DOCS.rglob('*.md')))} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
