#!/usr/bin/env python3
"""Collect concise review context after delegated agent work.

This helper is for Codex review. It avoids dumping huge diffs by default while
surfacing the information Codex needs before accepting delegated changes.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def run_git(workspace: Path, args: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(workspace),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def section(title: str, body: str) -> str:
    return f"\n## {title}\n\n{body.strip() if body.strip() else '(none)'}\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect concise git review context.")
    parser.add_argument("--workspace", default=".", help="Workspace directory.")
    parser.add_argument("--max-diff-lines", type=int, default=300, help="Max full diff lines to include.")
    parser.add_argument("--include-full-diff", action="store_true", help="Include capped unified diff.")
    parser.add_argument("--output", help="Optional markdown output file.")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    if not workspace.exists() or not workspace.is_dir():
        raise SystemExit(f"Workspace does not exist or is not a directory: {workspace}")

    rc, top, err = run_git(workspace, ["rev-parse", "--show-toplevel"])
    if rc != 0:
        raise SystemExit(f"Not a git repository: {workspace}\n{err}")
    repo = Path(top)

    parts: list[str] = [f"# Delegated Work Review Context\n\nWorkspace: `{repo}`\n"]

    for title, git_args in [
        ("Git Status", ["status", "--short"]),
        ("Changed Files", ["diff", "--name-status", "HEAD"]),
        ("Diff Stat", ["diff", "--stat", "HEAD"]),
        ("Recent Commits", ["log", "--oneline", "-5"]),
    ]:
        rc, out, err = run_git(repo, git_args)
        parts.append(section(title, out if rc == 0 else err))

    if args.include_full_diff:
        rc, out, err = run_git(repo, ["diff", "HEAD"])
        diff = out if rc == 0 else err
        lines = diff.splitlines()
        if len(lines) > args.max_diff_lines:
            diff = "\n".join(lines[: args.max_diff_lines]) + f"\n\n... truncated after {args.max_diff_lines} lines ..."
        parts.append(section("Capped Diff", f"```diff\n{diff}\n```" if diff else "(none)"))

    report = "".join(parts)
    if args.output:
        Path(args.output).expanduser().resolve().write_text(report, encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
