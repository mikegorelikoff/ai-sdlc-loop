"""Self-contained Windows installer: graphical entry plus the existing CLI."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import install

VERSION = "0.10.0"


def install_project(project: str, profile: str, skills_root: str | None = None) -> None:
    args = argparse.Namespace(project_root=project, profile=profile, skills_root=skills_root)
    install.install(args)
    install.verify(args)


def gui() -> int:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    window = tk.Tk()
    window.title(f"AI SDLC Loop {VERSION} Setup")
    window.resizable(False, False)
    frame = ttk.Frame(window, padding=24)
    frame.grid()
    ttk.Label(frame, text="Install AI SDLC Loop", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky="w")
    ttk.Label(frame, text="Choose the project folder that should receive the skills.").grid(row=1, column=0, columnspan=2, pady=(8, 16), sticky="w")
    project = tk.StringVar()
    ttk.Entry(frame, textvariable=project, width=58).grid(row=2, column=0, sticky="ew")

    def browse():
        selected = filedialog.askdirectory(parent=window, title="Select project folder", mustexist=True)
        if selected:
            project.set(selected)

    ttk.Button(frame, text="Browse…", command=browse).grid(row=2, column=1, padx=(8, 0))
    ttk.Label(frame, text="Agent").grid(row=3, column=0, pady=(16, 4), sticky="w")
    profiles = {"Codex": "codex-project", "Claude Code": "claude-code-project"}
    choice = ttk.Combobox(frame, values=list(profiles), state="readonly", width=24)
    choice.set("Codex")
    choice.grid(row=4, column=0, sticky="w")
    ttk.Label(frame, text="Installs 26 skills in this project. No administrator rights required.").grid(row=5, column=0, columnspan=2, pady=16, sticky="w")

    def submit():
        if not project.get().strip():
            messagebox.showerror("Choose a project", "Select an existing project folder first.", parent=window)
            return
        button.configure(state="disabled")
        window.update_idletasks()
        try:
            install_project(project.get(), profiles[choice.get()])
        except (install.InstallError, OSError, RuntimeError, ValueError, TypeError) as exc:
            messagebox.showerror("Installation stopped", str(exc), parent=window)
        else:
            messagebox.showinfo("Installation verified", "AI SDLC Loop is installed. Open your agent in this project and use ai-sdlc-loop-flow.", parent=window)
        finally:
            button.configure(state="normal")

    button = ttk.Button(frame, text="Install", command=submit)
    button.grid(row=6, column=0, sticky="e")
    ttk.Button(frame, text="Close", command=window.destroy).grid(row=6, column=1, padx=(8, 0))
    window.mainloop()
    return 0


def main() -> int:
    if sys.argv[1:] == ["--version"]:
        print(f"AI SDLC Loop {VERSION}")
        return 0
    if len(sys.argv) > 1:
        return install.main()
    return gui()


if __name__ == "__main__":
    raise SystemExit(main())
