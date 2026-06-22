from __future__ import annotations

import argparse
import shutil
import tempfile
import urllib.request
import zipfile
from datetime import datetime
from pathlib import Path


DEFAULT_REPOSITORY = "1447751897/zno-project-command-skills"
DEFAULT_BRANCH = "master"

CODEX_SKILL_NAMES = [
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

CLAUDE_SKILL_NAMES = [
    "ai-init",
    "ai-goal",
    "ai-super",
    "ai-feature",
    "ai-change",
    "ai-fix",
    "ai-tech",
    "ai-deploy",
    "ai-handoff",
    "ai-roadmap",
    "ai-plan",
    "ai-status",
    "ai-continue",
    "ai-upgrade",
    "ai-project-kickoff-docs",
]


def infer_tool_from_script_path() -> str:
    parts = {part.lower() for part in Path(__file__).resolve().parts}
    if "claude-skills" in parts or any(name in parts for name in CLAUDE_SKILL_NAMES):
        return "claude"
    return "codex"


def default_target_root(tool: str) -> Path:
    if tool == "claude":
        return Path.home() / ".claude" / "skills"
    return Path.home() / ".agents" / "skills"


def source_dir_name(tool: str) -> str:
    return "claude-skills" if tool == "claude" else "skills"


def expected_skill_names(tool: str) -> list[str]:
    return CLAUDE_SKILL_NAMES if tool == "claude" else CODEX_SKILL_NAMES


def restart_message(tool: str) -> str:
    return "Restart Claude Code so it can rescan skills." if tool == "claude" else (
        "Restart Codex desktop so the command menu can rescan skills."
    )


def download_zip(repository: str, branch: str, destination: Path) -> None:
    url = f"https://github.com/{repository}/archive/refs/heads/{branch}.zip"
    print(f"Downloading: {url}")
    request = urllib.request.Request(url, headers={"User-Agent": "ai-project-command-skills-updater"})
    with urllib.request.urlopen(request, timeout=60) as response:
        destination.write_bytes(response.read())


def find_package_root(extract_root: Path, required_source_dir: str) -> Path:
    candidates = [path for path in extract_root.iterdir() if path.is_dir()]
    for candidate in candidates:
        if (candidate / required_source_dir).is_dir():
            return candidate
    raise SystemExit(f"Downloaded package does not contain a {required_source_dir} directory.")


def validate_skills(skills_root: Path, skill_names: list[str]) -> list[str]:
    available: list[str] = []
    missing: list[str] = []
    for name in skill_names:
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
    inferred_tool = infer_tool_from_script_path()
    parser = argparse.ArgumentParser(
        description="Download the latest AI Project Command Skills from GitHub and install them locally."
    )
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY, help="GitHub repository in owner/name form")
    parser.add_argument("--branch", default=DEFAULT_BRANCH, help="Git branch to download")
    parser.add_argument(
        "--tool",
        choices=["codex", "claude"],
        default=inferred_tool,
        help="Install target tool. Defaults to the current skill package type.",
    )
    parser.add_argument(
        "--target-root",
        default=None,
        help="Local skills directory. Defaults to ~/.agents/skills for Codex or ~/.claude/skills for Claude Code.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Download and validate without changing local skills")
    args = parser.parse_args()

    target_root = (
        Path(args.target_root).expanduser().resolve()
        if args.target_root
        else default_target_root(args.tool).resolve()
    )
    required_source_dir = source_dir_name(args.tool)
    expected_names = expected_skill_names(args.tool)

    with tempfile.TemporaryDirectory(prefix="ai-project-command-skills-") as temp_dir:
        temp_root = Path(temp_dir)
        zip_path = temp_root / "package.zip"
        extract_root = temp_root / "extract"
        extract_root.mkdir()

        download_zip(args.repository, args.branch, zip_path)
        with zipfile.ZipFile(zip_path) as archive:
            archive.extractall(extract_root)

        package_root = find_package_root(extract_root, required_source_dir)
        skills_root = package_root / required_source_dir
        skill_names = validate_skills(skills_root, expected_names)

        print(f"Tool: {args.tool}")
        print(f"Package root: {package_root}")
        print(f"Source skills: {skills_root}")
        print(f"Target root: {target_root}")
        install_skills(skills_root, target_root, skill_names, args.dry_run)

    if args.dry_run:
        print("Dry run complete. No local skills were changed.")
    else:
        print("Update complete. " + restart_message(args.tool))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
