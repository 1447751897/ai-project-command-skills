from __future__ import annotations

import argparse
import shutil
import tempfile
import urllib.request
import zipfile
from datetime import datetime
from pathlib import Path


DEFAULT_REPOSITORY = "1447751897/ai-project-command-skills"
DEFAULT_BRANCH = "master"
SKILL_NAMES = [
    "init",
    "goal",
    "super",
    "feature",
    "change",
    "fix",
    "tech",
    "deploy",
    "handoff",
    "roadmap",
    "plan",
    "status",
    "continue",
    "upgrade",
    "project-kickoff-docs",
]


def default_target_root() -> Path:
    return Path.home() / ".agents" / "skills"


def download_zip(repository: str, branch: str, destination: Path) -> None:
    url = f"https://github.com/{repository}/archive/refs/heads/{branch}.zip"
    print(f"Downloading: {url}")
    request = urllib.request.Request(url, headers={"User-Agent": "ai-project-command-skills-updater"})
    with urllib.request.urlopen(request, timeout=60) as response:
        destination.write_bytes(response.read())


def find_package_root(extract_root: Path) -> Path:
    candidates = [path for path in extract_root.iterdir() if path.is_dir()]
    for candidate in candidates:
        if (candidate / "skills").is_dir():
            return candidate
    raise SystemExit("Downloaded package does not contain a skills directory.")


def validate_skills(skills_root: Path) -> list[str]:
    available: list[str] = []
    missing: list[str] = []
    for name in SKILL_NAMES:
        skill_md = skills_root / name / "SKILL.md"
        if skill_md.is_file():
            available.append(name)
        else:
            missing.append(name)

    if missing:
        raise SystemExit("Downloaded package is missing skills: " + ", ".join(missing))
    return available


def backup_existing(target_root: Path, skill_names: list[str]) -> Path | None:
    existing = [target_root / name for name in skill_names if (target_root / name).exists()]
    if not existing:
        return None

    backup_root = target_root / ".backup" / (
        "ai-project-command-skills-" + datetime.now().strftime("%Y%m%d-%H%M%S")
    )
    backup_root.mkdir(parents=True, exist_ok=True)
    for source in existing:
        shutil.copytree(source, backup_root / source.name)
    return backup_root


def install_skills(source_root: Path, target_root: Path, skill_names: list[str], dry_run: bool) -> None:
    target_root.mkdir(parents=True, exist_ok=True)
    backup_root = None if dry_run else backup_existing(target_root, skill_names)
    if backup_root:
        print(f"Backup created: {backup_root}")

    for name in skill_names:
        source = source_root / name
        target = target_root / name
        if dry_run:
            action = "update" if target.exists() else "install"
            print(f"Would {action}: {name} -> {target}")
            continue

        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)
        print(f"Installed: {name}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download the latest AI Project Command Skills from GitHub and install them locally."
    )
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY, help="GitHub repository in owner/name form")
    parser.add_argument("--branch", default=DEFAULT_BRANCH, help="Git branch to download")
    parser.add_argument(
        "--target-root",
        default=str(default_target_root()),
        help="Local skills directory, default: ~/.agents/skills",
    )
    parser.add_argument("--dry-run", action="store_true", help="Download and validate without changing local skills")
    args = parser.parse_args()

    target_root = Path(args.target_root).expanduser().resolve()
    with tempfile.TemporaryDirectory(prefix="ai-project-command-skills-") as temp_dir:
        temp_root = Path(temp_dir)
        zip_path = temp_root / "package.zip"
        extract_root = temp_root / "extract"
        extract_root.mkdir()

        download_zip(args.repository, args.branch, zip_path)
        with zipfile.ZipFile(zip_path) as archive:
            archive.extractall(extract_root)

        package_root = find_package_root(extract_root)
        skills_root = package_root / "skills"
        skill_names = validate_skills(skills_root)

        print(f"Package root: {package_root}")
        print(f"Target root: {target_root}")
        install_skills(skills_root, target_root, skill_names, args.dry_run)

    if args.dry_run:
        print("Dry run complete. No local skills were changed.")
    else:
        print("Update complete. Restart Codex desktop so the command menu can rescan skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
