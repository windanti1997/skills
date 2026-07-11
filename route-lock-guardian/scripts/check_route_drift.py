#!/usr/bin/env python3
"""Check for missing route-lock files and common generic drift smells.

This helper is intentionally conservative and project-agnostic. It does not replace review.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED = [
    "current-route-lock.md",
    "user-journey-contract.md",
    "non-goals-and-killed-routes.md",
]

RECOMMENDED_FOR_AUTOMATION = [
    "architecture-boundary-contract.md",
    "authority-matrix.md",
    "workflow-event-policy.md",
    "dogfood-readiness-gate.md",
    "route-drift-review-checklist.md",
]

GENERIC_DRIFT_PATTERNS = [
    "TODO: route",
    "fix later",
    "temporary route",
    "auto approve",
    "auto-approve",
    "auto accept",
    "auto-accept",
    "always allow",
    "skip approval",
    "bypass approval",
    "hidden background",
    "run in background by default",
]

SCAN_EXTENSIONS = {".md", ".txt", ".yaml", ".yml", ".json", ".ts", ".js", ".py", ".toml"}
IGNORE_PARTS = {".git", "node_modules", "dist", "build", ".venv", "venv"}


def should_scan(path: Path) -> bool:
    if path.suffix not in SCAN_EXTENSIONS:
        return False
    return not any(part in IGNORE_PARTS for part in path.parts)


def check(project_root: Path) -> dict:
    route_dir = project_root / "docs" / "route"
    missing_required = [name for name in REQUIRED if not (route_dir / name).exists()]
    missing_recommended = [name for name in RECOMMENDED_FOR_AUTOMATION if not (route_dir / name).exists()]

    matches = []
    for path in project_root.rglob("*"):
        if not path.is_file() or not should_scan(path):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        lower = text.lower()
        for pattern in GENERIC_DRIFT_PATTERNS:
            if pattern.lower() in lower:
                matches.append({"file": str(path.relative_to(project_root)), "pattern": pattern})

    return {
        "ok": not missing_required,
        "missing_required": missing_required,
        "missing_recommended_for_automation": missing_recommended,
        "generic_drift_pattern_matches": matches[:100],
        "match_count": len(matches),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = check(args.project_root.resolve())
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Route drift check")
        print(f"ok: {result['ok']}")
        if result["missing_required"]:
            print("missing required:")
            for item in result["missing_required"]:
                print(f"  - {item}")
        if result["missing_recommended_for_automation"]:
            print("missing recommended for automation-heavy projects:")
            for item in result["missing_recommended_for_automation"]:
                print(f"  - {item}")
        if result["generic_drift_pattern_matches"]:
            print("generic drift pattern matches:")
            for match in result["generic_drift_pattern_matches"][:20]:
                print(f"  - {match['file']}: {match['pattern']}")
            if result["match_count"] > 20:
                print(f"  ... {result['match_count'] - 20} more")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
