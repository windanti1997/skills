#!/usr/bin/env python3
"""Invoke an execution agent CLI from a delegation brief.

Runtime helper for agent-cli-delegation-partner.

Design goals:
- work on Windows/macOS/Linux without assuming a shell;
- resolve .cmd/.bat launchers on Windows;
- stream output in real time while also writing logs;
- support long-running agents through --background and --status;
- keep Mimo/MimoCode as presets, not hard dependencies.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from string import Formatter
from typing import TextIO


PRESETS = {
    "mimo": ["mimo", "run", "--dir", "{workspace}", "--title", "{title}", "{prompt}"],
    "mimocode": ["mimocode", "run", "--dir", "{workspace}", "--title", "{title}", "{prompt}"],
}

AUTO_ORDER = ("mimo", "mimocode")
ALLOWED_FIELDS = {"workspace", "title", "prompt_file", "prompt"}
WINDOWS_BATCH_SUFFIXES = {".bat", ".cmd"}


def is_windows() -> bool:
    return os.name == "nt"


def safe_log_name(title: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", title.strip()).strip("-")
    return cleaned[:60] or "delegation"


def validate_fields(parts: list[str]) -> None:
    fields: set[str] = set()
    for part in parts:
        fields.update(field_name for _, field_name, _, _ in Formatter().parse(part) if field_name)
    unknown = fields - ALLOWED_FIELDS
    if unknown:
        raise SystemExit(f"Unknown placeholder(s): {', '.join(sorted(unknown))}")
    if not ({"prompt_file", "prompt"} & fields):
        raise SystemExit("Command arguments must include {prompt_file} or {prompt}.")


def parse_command_template(template: str) -> list[str]:
    try:
        return shlex.split(template, posix=not is_windows())
    except ValueError as exc:
        raise SystemExit(f"Invalid command template: {exc}") from exc


def render_parts(parts: list[str], workspace: Path, title: str, prompt_file: Path, prompt_text: str) -> list[str]:
    validate_fields(parts)
    values = {
        "workspace": str(workspace),
        "title": title,
        "prompt_file": str(prompt_file),
        "prompt": prompt_text,
    }
    return [part.format(**values) for part in parts]


def preset_available(preset: str) -> bool:
    return shutil.which(PRESETS[preset][0]) is not None


def select_parts(agent: str, command_template: str | None) -> tuple[str, list[str]]:
    if command_template:
        return "custom", parse_command_template(command_template)
    if agent == "auto":
        for candidate in AUTO_ORDER:
            if preset_available(candidate):
                return candidate, PRESETS[candidate]
        raise SystemExit(
            "No known agent CLI preset is available on PATH. "
            "Install/configure a compatible CLI or pass --command-template."
        )
    if not preset_available(agent):
        raise SystemExit(
            f"Preset agent CLI '{agent}' is not available on PATH. "
            "Use --command-template to adapt another CLI."
        )
    return agent, PRESETS[agent]


def resolve_argv(argv: list[str]) -> tuple[list[str], bool]:
    """Resolve argv[0] and decide whether Windows shell is required."""
    if not argv:
        raise SystemExit("Empty command argv.")
    executable = shutil.which(argv[0]) or argv[0]
    resolved = [executable, *argv[1:]]
    needs_shell = is_windows() and Path(executable).suffix.lower() in WINDOWS_BATCH_SUFFIXES
    return resolved, needs_shell


def command_display(argv: list[str], shell_required: bool) -> str:
    if is_windows():
        return subprocess.list2cmdline(argv)
    return shlex.join(argv)


def build_log_paths(workspace: Path, log_dir_arg: str, title: str) -> tuple[Path, Path, Path]:
    started = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_dir = Path(log_dir_arg)
    if not log_dir.is_absolute():
        log_dir = workspace / log_dir
    log_dir.mkdir(parents=True, exist_ok=True)
    base = f"{started}-{safe_log_name(title)}"
    return log_dir / f"{base}.combined.log", log_dir / f"{base}.status.json", log_dir


def write_status(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def pid_is_running(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def status_command(status_file: str) -> int:
    path = Path(status_file).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"Status file does not exist: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    pid = int(data.get("pid") or 0)
    running = pid_is_running(pid)
    data["running_now"] = running
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0 if running else int(data.get("returncode") or 0)


def stream_process(process: subprocess.Popen[str], log_file: TextIO) -> int:
    assert process.stdout is not None
    for line in iter(process.stdout.readline, ""):
        sys.stdout.write(line)
        sys.stdout.flush()
        log_file.write(line)
        log_file.flush()
    return process.wait()


def launch(argv: list[str], workspace: Path, shell_required: bool, background: bool, log_path: Path | None) -> subprocess.Popen[str]:
    command: str | list[str] = command_display(argv, True) if shell_required else argv
    if background:
        assert log_path is not None
        stdout_target = open(log_path, "a", encoding="utf-8", buffering=1)
        stderr_target = subprocess.STDOUT
    else:
        stdout_target = subprocess.PIPE
        stderr_target = subprocess.STDOUT
    try:
        return subprocess.Popen(
            command,
            cwd=str(workspace),
            text=True,
            stdout=stdout_target,
            stderr=stderr_target,
            shell=shell_required,
        )
    except FileNotFoundError as exc:
        raise SystemExit(f"Agent CLI executable not found: {argv[0]}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Delegate a bounded task to an agent CLI.")
    parser.add_argument("--workspace", help="Workspace directory for the delegated agent.")
    parser.add_argument("--title", help="Short task title.")
    parser.add_argument("--prompt-file", help="Path to the delegation brief.")
    parser.add_argument("--agent", choices=["auto", *sorted(PRESETS)], default="auto")
    parser.add_argument("--command-template", help="Command template. Overrides --agent preset.")
    parser.add_argument("--log-dir", default=".agent-delegation/logs")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-log", action="store_true")
    parser.add_argument("--background", action="store_true")
    parser.add_argument("--status", help="Read a background status JSON file.")
    args = parser.parse_args()

    if args.status:
        return status_command(args.status)

    missing = [name for name in ("workspace", "title", "prompt_file") if getattr(args, name) is None]
    if missing:
        raise SystemExit(f"Missing required argument(s): {', '.join('--' + x.replace('_', '-') for x in missing)}")

    workspace = Path(args.workspace).expanduser().resolve()
    prompt_file = Path(args.prompt_file).expanduser().resolve()
    if not workspace.exists() or not workspace.is_dir():
        raise SystemExit(f"Workspace does not exist or is not a directory: {workspace}")
    if not prompt_file.exists() or not prompt_file.is_file():
        raise SystemExit(f"Prompt file does not exist: {prompt_file}")

    prompt_text = prompt_file.read_text(encoding="utf-8")
    selected_agent, parts = select_parts(args.agent, args.command_template)
    raw_argv = render_parts(parts, workspace, args.title, prompt_file, prompt_text)
    argv, shell_required = resolve_argv(raw_argv)

    print(f"Selected agent: {selected_agent}")
    print(f"Detected OS: {os.name}; shell_required: {shell_required}")
    print("Delegation command:")
    print(command_display(argv, shell_required))
    if args.dry_run:
        return 0

    log_path = status_path = None
    if not args.no_log or args.background:
        log_path, status_path, _ = build_log_paths(workspace, args.log_dir, args.title)
        print(f"Log file: {log_path}")

    process = launch(argv, workspace, shell_required, args.background, log_path)
    if args.background:
        assert status_path is not None
        write_status(status_path, {
            "pid": process.pid,
            "agent": selected_agent,
            "workspace": str(workspace),
            "title": args.title,
            "prompt_file": str(prompt_file),
            "command": command_display(argv, shell_required),
            "log_file": str(log_path),
            "started_at": _dt.datetime.now().isoformat(timespec="seconds"),
            "returncode": None,
        })
        print(f"Started background delegation. PID: {process.pid}")
        print(f"Status file: {status_path}")
        return 0

    if log_path and not args.no_log:
        with log_path.open("a", encoding="utf-8", buffering=1) as log_file:
            returncode = stream_process(process, log_file)
    else:
        returncode = stream_process(process, sys.stdout)

    if status_path and not args.no_log:
        write_status(status_path, {
            "pid": process.pid,
            "agent": selected_agent,
            "workspace": str(workspace),
            "title": args.title,
            "prompt_file": str(prompt_file),
            "command": command_display(argv, shell_required),
            "log_file": str(log_path),
            "finished_at": _dt.datetime.now().isoformat(timespec="seconds"),
            "returncode": returncode,
        })
    return returncode


if __name__ == "__main__":
    raise SystemExit(main())
