#!/usr/bin/env python3
"""Invoke an execution agent CLI from a delegation brief.

This helper is for Codex while using agent-cli-delegation-partner. It is
CLI-agnostic: Mimo and MimoCode are only presets. Prefer prompt files over
inline prompts to avoid quoting and command-length issues.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from string import Formatter


PRESETS = {
    "mimo": ["mimo", "run", "--dir", "{workspace}", "--title", "{title}", "{prompt}"],
    "mimocode": ["mimocode", "run", "--dir", "{workspace}", "--title", "{title}", "{prompt}"],
}

AUTO_ORDER = ("mimo", "mimocode")
ALLOWED_FIELDS = {"workspace", "title", "prompt_file", "prompt"}


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
        return shlex.split(template, posix=(os.name != "nt"))
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


def safe_log_name(title: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", title.strip()).strip("-")
    return cleaned[:60] or "delegation"


def main() -> int:
    parser = argparse.ArgumentParser(description="Delegate a bounded task to an agent CLI.")
    parser.add_argument("--workspace", required=True, help="Workspace directory for the delegated agent.")
    parser.add_argument("--title", required=True, help="Short task title.")
    parser.add_argument("--prompt-file", required=True, help="Path to the delegation brief.")
    parser.add_argument(
        "--agent",
        choices=["auto", *sorted(PRESETS)],
        default="auto",
        help="Preset agent CLI to use. Default: auto-detect a known preset.",
    )
    parser.add_argument("--command-template", help="Command template. Overrides --agent preset.")
    parser.add_argument(
        "--log-dir",
        default=".agent-delegation/logs",
        help="Directory for stdout/stderr logs, relative to workspace unless absolute.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print command and exit without running it.")
    parser.add_argument("--no-log", action="store_true", help="Do not write stdout/stderr log files.")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    prompt_file = Path(args.prompt_file).expanduser().resolve()

    if not workspace.exists() or not workspace.is_dir():
        raise SystemExit(f"Workspace does not exist or is not a directory: {workspace}")
    if not prompt_file.exists() or not prompt_file.is_file():
        raise SystemExit(f"Prompt file does not exist: {prompt_file}")

    prompt_text = prompt_file.read_text(encoding="utf-8")
    selected_agent, parts = select_parts(args.agent, args.command_template)
    argv = render_parts(parts, workspace, args.title, prompt_file, prompt_text)

    print(f"Selected agent: {selected_agent}")
    print("Delegation argv:")
    print(shlex.join(argv) if hasattr(shlex, "join") else " ".join(argv))

    if args.dry_run:
        return 0

    started = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_dir = Path(args.log_dir)
    if not log_dir.is_absolute():
        log_dir = workspace / log_dir

    process = subprocess.run(
        argv,
        cwd=str(workspace),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if not args.no_log:
        log_dir.mkdir(parents=True, exist_ok=True)
        base = f"{started}-{safe_log_name(args.title)}"
        (log_dir / f"{base}.stdout.log").write_text(process.stdout, encoding="utf-8")
        (log_dir / f"{base}.stderr.log").write_text(process.stderr, encoding="utf-8")
        print(f"Logs written to: {log_dir}")

    if process.stdout:
        print("\n--- stdout ---")
        print(process.stdout)
    if process.stderr:
        print("\n--- stderr ---", file=sys.stderr)
        print(process.stderr, file=sys.stderr)

    return process.returncode


if __name__ == "__main__":
    raise SystemExit(main())
