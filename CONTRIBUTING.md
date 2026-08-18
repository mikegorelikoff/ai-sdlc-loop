# Contributing

Use a focused branch and keep the repository limited to the fixed Loop skill graph and shared runtime. Add or update tests before changing behavior. Keep all Loop-owned durable machine artifacts in canonical TOON. Run:

```sh
python3 -m unittest discover -s tests -v
PYTHONPYCACHEPREFIX=/tmp/ai-sdlc-loop-pycache python3 -m compileall -q install.py skills tests docs/scripts
sh -n install.sh
python3 docs/scripts/build_catalog.py --check
python3 docs/scripts/validate_docs.py
mkdocs build --strict
python3 docs/scripts/validate_rendered.py site
git diff --check
```

Do not commit generated local `.ai-sdlc-loop/` state. Security reports belong in the private channel described in [SECURITY.md](SECURITY.md), not a public issue.
