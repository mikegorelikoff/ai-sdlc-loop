# Windows release packaging

Build on Windows x64 with Python 3.11:

```powershell
python -m pip install --require-hashes -r packaging/windows/requirements.lock
python packaging/windows/build.py
python packaging/windows/smoke.py dist/ai-sdlc-loop-0.10.0-windows-x64-setup.exe
```

The launcher delegates CLI and installation policy to `install.py`. The payload
uses its explicit skill inventory and excludes tests and interpreter caches.
The Python interpreter is private to setup; no registry, PATH or machine-wide
Python changes occur. Native Tcl/Tk provides the folder/profile picker.

The workflow validates the real EXE with Python removed from PATH, exercises the
native GUI, all profiles, repeated installation, drift and unsafe destinations,
and publishes the EXE plus SHA-256 only after the build job succeeds. Tag and
package versions must agree. Releases are unsigned until signing credentials
and a publisher identity are configured; checksums are integrity evidence.

Bundling follows the official PyInstaller [runtime file layout](https://www.pyinstaller.org/en/stable/runtime-information.html)
and [one-file build contract](https://www.pyinstaller.org/en/stable/usage.html).
