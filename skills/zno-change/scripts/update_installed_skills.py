from __future__ import annotations

import argparse
import re
import shutil
import tempfile
import urllib.request
import zipfile
from datetime import datetime
from pathlib import Path


DEFAULT_REPOSITORY = "1447751897/ai-project-command-skills"
DEFAULT_BRANCH = "master"

CODEX_SKILL_NAMES = [
    "zno-init",
    "zno-goal",
    "zno-super",
    "zno-feature",
    "zno-change",
    "zno-fix",
    "zno-tech",
    "zno-deploy",
    "zno-handoff",
    "zno-roadmap",
    "zno-plan",
    "zno-status",
    "zno-continue",
    "zno-upgrade",
    "zno-project-kickoff-docs",
    "zno-evaluate",
    "zno-retro",
    "zno-review",
]

CLAUDE_SKILL_NAMES = [
    "zno-init",
    "zno-goal",
    "zno-super",
    "zno-feature",
    "zno-change",
    "zno-fix",
    "zno-tech",
    "zno-deploy",
    "zno-handoff",
    "zno-roadmap",
    "zno-plan",
    "zno-status",
    "zno-continue",
    "zno-upgrade",
    "zno-project-kickoff-docs",
    "zno-evaluate",
    "zno-retro",
    "zno-review",
]


def infer_tool_from_script_path() -> str:
    parts = {part.lower() for part in Path(__file__).resolve().parts}
    if ".claude" in parts:
        return "claude"
    if ".agents" in parts or ".codex" in parts:
        return "codex"
    return "codex"


def default_target_root(tool: str) -> Path:
    if tool == "claude":
        return Path.home() / ".claude" / "skills"
    return Path.home() / ".agents" / "skills"


def source_dir_name(tool: str) -> str:
    return "skills"


def expected_skill_names(tool: str) -> list[str]:
    return CLAUDE_SKILL_NAMES if tool == "claude" else CODEX_SKILL_NAMES


def restart_message(tool: str) -> str:
    return "Restart Claude Code so it can rescan skills." if tool == "claude" else (
        "Restart Codex desktop so the command menu can rescan skills."
    )


def download_zip(repository: str, branch: str, destination: Path) -> None:
    url = f"https://github.com/{repository}/archive/refs/heads/{branch}.zip"
    print(f"Downloading: {url}")
    request = urllib.request.Request(url, headers={"User-Agent": "zno-project-command-skills-updater"})
    with urllib.request.urlopen(request, timeout=60) as response:
        destination.write_bytes(response.read())


def find_package_root(extract_root: Path, required_source_dir: str) -> Path:
    candidates = [path for path in extract_root.iterdir() if path.is_dir()]
    for candidate in candidates:
        if (candidate / required_source_dir).is_dir():
            return candidate
    raise SystemExit(f"Downloaded package does not contain a {required_source_dir} directory.")


def discover_skills(skills_root: Path) -> list[str]:
    """Discover all skill directories (containing SKILL.md) in the downloaded package."""
    found = []
    for child in sorted(skills_root.iterdir()):
        if child.is_dir() and (child / "SKILL.md").is_file():
            found.append(child.name)
    return found


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


def rename_upstream_to_local(skills_root: Path) -> int:
    """Rename ai-* directories from upstream to zno-* for local installation."""
    count = 0
    for child in list(skills_root.iterdir()):
        if child.is_dir() and child.name.startswith("ai-"):
            new_name = "zno-" + child.name[3:]
            target = child.parent / new_name
            if not target.exists():
                child.rename(target)
                print(f"  Mapped upstream {child.name} -> {new_name}")
                count += 1
    return count


def replace_prefix_in_files(skills_root: Path) -> None:
    """Replace ai- prefix references with zno- in all text files after download."""
    replacements = [
        ("name: ai-", "name: zno-"),
        ("# Ai-", "# Zno-"),
        ("'ai-", "'zno-"),
        ('"ai-', '"zno-'),
        ("The 'ai-' prefix", "The 'zno-' prefix"),
    ]
    text_extensions = {".md", ".py", ".yaml", ".yml", ".json", ".txt"}

    count = 0
    for filepath in skills_root.rglob("*"):
        if not filepath.is_file():
            continue
        if filepath.suffix.lower() not in text_extensions:
            continue
        try:
            content = filepath.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        original = content
        for old, new in replacements:
            content = content.replace(old, new)
        content = re.sub(r"(?<![A-Za-z0-9_.-])/ai-", "/zno-", content)

        if content != original:
            filepath.write_text(content, encoding="utf-8")
            count += 1

    if count:
        print(f"  Replaced ai- -> zno- prefix in {count} files")


def normalize_openai_metadata(skills_root: Path, skill_names: list[str]) -> None:
    """Keep Codex skill menu names searchable by their zno-* skill IDs."""
    count = 0
    for name in skill_names:
        metadata_path = skills_root / name / "agents" / "openai.yaml"
        if not metadata_path.is_file() or not name.startswith("zno-"):
            continue

        try:
            content = metadata_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        updated_lines: list[str] = []
        changed = False
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("display_name:"):
                prefix = line[: len(line) - len(line.lstrip())]
                new_line = f'{prefix}display_name: "{name}"'
            elif stripped.startswith("default_prompt:"):
                new_line = re.sub(
                    r"(Use\s+\$)[A-Za-z0-9_-]+",
                    lambda match: f"{match.group(1)}{name}",
                    line,
                    count=1,
                )
            else:
                new_line = line

            if new_line != line:
                changed = True
            updated_lines.append(new_line)

        if changed:
            metadata_path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")
            count += 1

    if count:
        print(f"  Normalized agents/openai.yaml metadata in {count} skills")


def backup_existing(target_root: Path, skill_names: list[str]) -> Path | None:
    existing = [target_root / name for name in skill_names if (target_root / name).exists()]
    if not existing:
        return None

    backup_root = target_root / ".backup" / (
        "zno-skills-backup-" + datetime.now().strftime("%Y%m%d-%H%M%S")
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

    with tempfile.TemporaryDirectory(prefix="zno-skills-backup-") as temp_dir:
        temp_root = Path(temp_dir)
        zip_path = temp_root / "package.zip"
        extract_root = temp_root / "extract"
        extract_root.mkdir()

        download_zip(args.repository, args.branch, zip_path)
        with zipfile.ZipFile(zip_path) as archive:
            archive.extractall(extract_root)

        package_root = find_package_root(extract_root, required_source_dir)
        skills_root = package_root / required_source_dir

        # Older upstream packages may still use ai-* names. Normalize them before validation.
        renamed_count = rename_upstream_to_local(skills_root)
        if renamed_count:
            replace_prefix_in_files(skills_root)

        # Discover all available skills from the downloaded package (auto-detect new ones)
        discovered_names = discover_skills(skills_root)
        if not discovered_names:
            raise SystemExit("Downloaded package contains no valid skill directories.")
        validate_skills(skills_root, expected_names)
        normalize_openai_metadata(skills_root, discovered_names)

        print(f"Tool: {args.tool}")
        print(f"Package root: {package_root}")
        print(f"Source skills: {skills_root}")
        print(f"Target root: {target_root}")
        install_skills(skills_root, target_root, discovered_names, args.dry_run)

    if args.dry_run:
        print("Dry run complete. No local skills were changed.")
    else:
        print("Update complete. " + restart_message(args.tool))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
