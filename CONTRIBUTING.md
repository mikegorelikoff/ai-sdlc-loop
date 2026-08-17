# Contributing

Use a focused branch and keep the repository limited to the one-skill Loop contract. Add or update tests before changing behavior. Run:

```sh
python3 -m unittest discover -s tests -v
python3 -m compileall -q install.py skills tests
sh -n install.sh
git diff --check
```

Do not commit generated local `.ai-sdlc-loop/` state. Security reports belong in the private channel described in [SECURITY.md](SECURITY.md), not a public issue.
