from __future__ import annotations

import argparse
import shutil
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = SKILL_ROOT / "assets" / "project-template"

# ---------------------------------------------------------------------------
# Progressive scaffold: essential files are created on /zno-init;
# on-demand files are created lazily when their corresponding command fires.
# ---------------------------------------------------------------------------

ESSENTIAL_FILES = [
    "AI_DEVELOPMENT_RULES.md",
    "docs/README.md",
    "docs/00_START_HERE.md",
    "docs/product/01-requirements-clarification.md",
    "docs/product/06-roadmap.md",
    "docs/product/15-frontend-design.md",
    "docs/product/15-frontend-design-tokens.json",
    "docs/engineering/02-development-principles.md",
]

# Maps: trigger context -> list of on-demand files to scaffold
ON_DEMAND_MAP = {
    "feature": [
        "docs/development/03-feature-changelog.md",
    ],
    "tech": [
        "docs/engineering/04-tech-decisions.md",
    ],
    "handoff": [
        "docs/handoff/05-handoff-guide.md",
    ],
    "local-dev": [
        "docs/operations/07-local-development.md",
    ],
    "deploy": [
        "docs/operations/08-deployment.md",
    ],
    "status": [
        "docs/development/10-current-status.md",
    ],
    "structure": [
        "docs/engineering/11-project-structure.md",
    ],
    "upgrade": [
        "docs/maintenance/12-upgrade-history.md",
    ],
    "command-ref": [
        "docs/maintenance/13-command-reference.md",
    ],
    "decision-log": [
        "docs/development/14-decision-log.md",
    ],
    "zno-prompt": [
        "docs/maintenance/09-zno-project-start-prompt.md",
    ],
}


def copy_files(src_root: Path, dst_root: Path, relatives: list[str], overwrite: bool) -> list[str]:
    """Copy specific files from template to project."""
    written: list[str] = []
    for rel in relatives:
        src = src_root / rel
        if not src.exists():
            continue
        target = dst_root / rel
        if target.exists() and not overwrite:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
        written.append(str(target))
    return written


def copy_tree(src: Path, dst: Path, overwrite: bool) -> list[str]:
    """Copy entire template tree (used with --full)."""
    written: list[str] = []
    for item in src.rglob("*"):
        relative = item.relative_to(src)
        target = dst / relative
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        if target.exists() and not overwrite:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)
        written.append(str(target))
    return written


def list_template_files(src: Path) -> list[Path]:
    return [item.relative_to(src) for item in src.rglob("*") if item.is_file()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize or upgrade AI project docs.")
    parser.add_argument("project_root", help="Target project root directory")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing docs. Use only when explicitly requested.",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Generate all template files at once (legacy behavior). Default is minimal/progressive.",
    )
    parser.add_argument(
        "--scaffold",
        type=str,
        default=None,
        help="Scaffold on-demand files for a specific trigger (e.g. feature, tech, deploy, status).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only list missing template files without writing them.",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    if not project_root.exists():
        raise SystemExit(f"Project root does not exist: {project_root}")
    if not project_root.is_dir():
        raise SystemExit(f"Project root is not a directory: {project_root}")
    if not TEMPLATE_ROOT.exists():
        raise SystemExit(f"Template root does not exist: {TEMPLATE_ROOT}")

    if args.check:
        missing = [
            relative
            for relative in list_template_files(TEMPLATE_ROOT)
            if not (project_root / relative).exists()
        ]
        if missing:
            print("Missing project docs:")
            for path in missing:
                print(f"  - {project_root / path}")
        else:
            print("No missing project docs.")
        return 0

    # On-demand scaffold for a specific trigger
    if args.scaffold:
        trigger = args.scaffold.lower()
        if trigger not in ON_DEMAND_MAP:
            valid = ", ".join(sorted(ON_DEMAND_MAP.keys()))
            raise SystemExit(f"Unknown scaffold trigger: {trigger}. Valid: {valid}")
        files = ON_DEMAND_MAP[trigger]
        written = copy_files(TEMPLATE_ROOT, project_root, files, args.overwrite)
        if written:
            print(f"Scaffolded on-demand docs for '{trigger}':")
            for path in written:
                print(f"  - {path}")
        else:
            print(f"On-demand docs for '{trigger}' already exist. Nothing written.")
        return 0

    # Full mode: legacy behavior, copy everything
    if args.full:
        written = copy_tree(TEMPLATE_ROOT, project_root, args.overwrite)
        if written:
            print("Initialized ALL project docs (full mode):")
            for path in written:
                print(f"  - {path}")
        else:
            print("No files written. Existing docs were preserved.")
        return 0

    # Default: minimal/progressive mode - only essential files
    written = copy_files(TEMPLATE_ROOT, project_root, ESSENTIAL_FILES, args.overwrite)
    if written:
        print("Initialized essential project docs (progressive mode):")
        for path in written:
            print(f"  - {path}")
        print()
        print("Remaining docs will be created on-demand when their corresponding")
        print("commands are first used (/zno-feature, /zno-deploy, /zno-status).")
        print("Use --full to generate all docs at once.")
    else:
        print("No files written. Essential docs already exist.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
