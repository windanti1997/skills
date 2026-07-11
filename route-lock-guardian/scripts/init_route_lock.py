#!/usr/bin/env python3
"""Initialize generic route-lock documents in a project.

Usage:
  python scripts/init_route_lock.py <project-root> --minimal
  python scripts/init_route_lock.py <project-root> --full
"""
from __future__ import annotations

import argparse
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = SKILL_ROOT / "templates"

MINIMAL = [
    ("current-route-lock-template.md", "current-route-lock.md"),
    ("user-journey-contract-template.md", "user-journey-contract.md"),
    ("non-goals-and-killed-routes-template.md", "non-goals-and-killed-routes.md"),
]

FULL_EXTRA = [
    ("architecture-boundary-contract-template.md", "architecture-boundary-contract.md"),
    ("authority-matrix-template.md", "authority-matrix.md"),
    ("workflow-event-policy-template.md", "workflow-event-policy.md"),
    ("dogfood-readiness-gate-template.md", "dogfood-readiness-gate.md"),
    ("release-readiness-gate-template.md", "release-readiness-gate.md"),
    ("route-drift-review-checklist-template.md", "route-drift-review-checklist.md"),
]


def copy_templates(project_root: Path, full: bool, force: bool) -> int:
    route_dir = project_root / "docs" / "route"
    route_dir.mkdir(parents=True, exist_ok=True)

    files = MINIMAL + (FULL_EXTRA if full else [])
    created = 0
    skipped = 0

    for template_name, output_name in files:
        source = TEMPLATES / template_name
        target = route_dir / output_name
        if target.exists() and not force:
            print(f"skip existing: {target}")
            skipped += 1
            continue
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"write: {target}")
        created += 1

    print(f"done: created_or_updated={created}, skipped={skipped}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", type=Path)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--minimal", action="store_true", help="create only the required route files")
    group.add_argument("--full", action="store_true", help="create the full route contract set")
    parser.add_argument("--force", action="store_true", help="overwrite existing route files")
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    full = bool(args.full)
    return copy_templates(project_root, full=full, force=args.force)


if __name__ == "__main__":
    raise SystemExit(main())
