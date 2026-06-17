from __future__ import annotations

import argparse
import shutil
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = SKILL_ROOT / "assets" / "project-template"


def copy_tree(src: Path, dst: Path, overwrite: bool) -> list[str]:
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
                print(f"- {project_root / path}")
        else:
            print("No missing project docs.")
        return 0

    written = copy_tree(TEMPLATE_ROOT, project_root, args.overwrite)
    if written:
        print("Initialized project docs:")
        for path in written:
            print(f"- {path}")
    else:
        print("No files written. Existing docs were preserved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
