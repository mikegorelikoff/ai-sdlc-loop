#!/usr/bin/env python3
"""Validate rendered MkDocs internal targets."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path)
    args = parser.parse_args()
    site = args.site.resolve()
    if not site.is_dir():
        parser.error("site must be a rendered directory")
    checked = 0
    errors = []
    for page in sorted(site.rglob("*.html")):
        text = page.read_text(encoding="utf-8")
        for href in re.findall(r'href=["\']([^"\']+)', text):
            parts = urlsplit(href)
            if parts.scheme or parts.netloc or href.startswith(("#", "mailto:")):
                continue
            relative = unquote(parts.path)
            if not relative:
                continue
            if relative.startswith("/ai-sdlc-loop/"):
                relative = relative.removeprefix("/ai-sdlc-loop/")
                target = site / relative
            else:
                target = (site / relative.lstrip("/")) if relative.startswith("/") else (page.parent / relative)
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                errors.append(f"{page.relative_to(site)} -> {href}")
            checked += 1
    if errors:
        print("rendered validation failed:\n" + "\n".join(errors[:30]), file=sys.stderr)
        return 1
    print(f"rendered validation passed: {checked} internal targets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
