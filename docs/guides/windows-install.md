# Install on Windows

## Goal

Install and verify AI SDLC Loop in a Windows project using a standalone executable.

## When to use it

Use the EXE when you want a folder and agent picker or an installer that does not require Python to be installed first.

## Prerequisites

- Windows 10/11 x64 and an existing writable project folder.
- Download [ai-sdlc-loop-0.10.0-windows-x64-setup.exe](https://github.com/mikegorelikoff/ai-sdlc-loop/releases/download/v0.10.0/ai-sdlc-loop-0.10.0-windows-x64-setup.exe) and its [SHA-256 file](https://github.com/mikegorelikoff/ai-sdlc-loop/releases/download/v0.10.0/ai-sdlc-loop-0.10.0-windows-x64-setup.exe.sha256) from the same release.
- Setup includes its own Python and all 26 skills. Python is still required to run Python-based skills afterwards; see [supported environments](../reference/environments.md). Setup does not change PATH or install a system-wide interpreter.

## Procedure

1. Open the EXE.
2. Browse to your project folder.
3. Select **Codex** or **Claude Code**.
4. Click **Install**. Setup reports success only after verification.

Installation works offline and does not require administrator rights. Codex uses `.agents/skills`; Claude Code uses `.claude/skills`.

For automation, PowerShell accepts the existing installer arguments:

```powershell
.\ai-sdlc-loop-0.10.0-windows-x64-setup.exe install codex-project --project-root "C:\Projects\My App"
```

A generic agent uses `agent-project --skills-root .agent/skills`. Run `--help` for the complete CLI or `--version` to inspect the packaged release.

## Verify

Compare the downloaded file's hash with the `.sha256` file:

```powershell
Get-FileHash .\ai-sdlc-loop-0.10.0-windows-x64-setup.exe -Algorithm SHA256
```

Verify the installed project independently:

```powershell
.\ai-sdlc-loop-0.10.0-windows-x64-setup.exe verify codex-project --project-root "C:\Projects\My App"
```

The release pipeline runs the actual executable without Python on PATH, tests all three profiles, and checks repeat installation, local drift, unsafe roots and asset checksums.

## Troubleshooting

- **Unknown publisher / SmartScreen:** this release is unsigned. Verify its source and checksum and follow your organization's software policy. A checksum detects altered downloads; it is not a publisher signature.
- **Occupied or drifted destination:** preserve local changes. Setup verifies an existing managed installation and stops on drift; it does not overwrite or automatically upgrade existing skills. Use a clean project destination for a different version.
- **No project selected:** select an existing directory; setup does not create the project itself.
- **Skill execution cannot find Python:** install the supported Python runtime separately. The interpreter inside setup is private to the installer.

## Next step

[Run the first loop](../start-here.md#run-the-first-loop).
