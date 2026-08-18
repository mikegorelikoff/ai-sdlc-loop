#!/bin/sh
set -eu

repo="mikegorelikoff/ai-sdlc-loop"
ref="${AI_SDLC_LOOP_REF:-v0.1.1}"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
curl -fsSL "https://github.com/${repo}/archive/refs/tags/${ref}.tar.gz" -o "$tmp/source.tar.gz"
tar -xzf "$tmp/source.tar.gz" -C "$tmp"
python3 "$tmp/ai-sdlc-loop-${ref#v}/install.py" "$@"
