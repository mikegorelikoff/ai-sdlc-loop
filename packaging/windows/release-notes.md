## Windows installer

Download **ai-sdlc-loop-0.10.0-windows-x64-setup.exe**, open it, and choose your project folder and Codex or Claude Code. The executable includes Python for installation and all 26 Loop skills; installation works offline without administrator privileges.

Existing Python and shell installation commands remain supported. Generic agent profiles are available through the EXE command line. Existing managed installations are verified; local drift and unmanaged files are preserved and reported rather than overwritten.

### Verification

The release asset is built on Windows x64 with hash-locked dependencies and tested without Python on PATH: all profiles, repeated installation, drift rejection, unsafe paths and checksum validation. CI also covers the existing cross-platform Loop contracts. A `.sha256` file accompanies the executable.

### Requirements and limitations

Windows 10/11 x64. The executable is currently unsigned; Windows may display a publisher/SmartScreen warning. Python is bundled for the installer only; running Python-based Loop skills still requires the documented Python runtime. Optional graph-parser dependencies retain their existing installation contract. Existing projects are not automatically upgraded or uninstalled.

### Rollback

The previous source release is v0.9.0. Preserve local changes and use a clean project/skill destination when installing another version.
