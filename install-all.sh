#!/usr/bin/env bash
set -euo pipefail

TOOL="auto"
SOURCE="local"
REPOSITORY="1447751897/zno-project-command-skills"
BRANCH="master"
CODEX_TARGET_ROOT="$HOME/.agents/skills"
CLAUDE_TARGET_ROOT="$HOME/.claude/skills"
DRY_RUN=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --tool)
      TOOL="${2:?Missing value for --tool}"
      shift 2
      ;;
    --source)
      SOURCE="${2:?Missing value for --source}"
      shift 2
      ;;
    --repository)
      REPOSITORY="${2:?Missing value for --repository}"
      shift 2
      ;;
    --branch)
      BRANCH="${2:?Missing value for --branch}"
      shift 2
      ;;
    --codex-target-root)
      CODEX_TARGET_ROOT="${2:?Missing value for --codex-target-root}"
      shift 2
      ;;
    --claude-target-root)
      CLAUDE_TARGET_ROOT="${2:?Missing value for --claude-target-root}"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

case "$TOOL" in
  auto|codex|claude|all) ;;
  *)
    echo "--tool must be auto, codex, claude, or all" >&2
    exit 1
    ;;
esac

case "$SOURCE" in
  local|github) ;;
  *)
    echo "--source must be local or github" >&2
    exit 1
    ;;
esac

CODEX_SKILL_NAMES=(
  init
  goal
  super
  feature
  change
  fix
  tech
  deploy
  handoff
  roadmap
  plan
  status
  continue
  upgrade
  project-kickoff-docs
)

CLAUDE_SKILL_NAMES=(
  zno-init
  zno-goal
  zno-super
  zno-feature
  zno-change
  zno-fix
  zno-tech
  zno-deploy
  zno-handoff
  zno-roadmap
  zno-plan
  zno-status
  zno-continue
  zno-upgrade
  zno-project-kickoff-docs
)

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

codex_detected() {
  [ -n "${CODEX_HOME:-}" ] || [ -d "$HOME/.codex" ] || [ -d "$HOME/.agents" ] || command_exists codex
}

claude_detected() {
  [ -n "${CLAUDE_CONFIG_DIR:-}" ] || [ -d "$HOME/.claude" ] || command_exists claude
}

selected_tools() {
  case "$TOOL" in
    codex)
      printf '%s\n' codex
      ;;
    claude)
      printf '%s\n' claude
      ;;
    all)
      printf '%s\n' codex claude
      ;;
    auto)
      if codex_detected; then printf '%s\n' codex; fi
      if claude_detected; then printf '%s\n' claude; fi
      ;;
  esac
}

package_root() {
  if [ "$SOURCE" = "local" ]; then
    cd "$(dirname "${BASH_SOURCE[0]}")" && pwd
    return
  fi

  if ! command_exists python3; then
    echo "python3 is required for --source github" >&2
    exit 1
  fi

  python3 - "$REPOSITORY" "$BRANCH" <<'PY'
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

repository, branch = sys.argv[1], sys.argv[2]
temp_root = Path(tempfile.mkdtemp(prefix="zno-project-command-skills-"))
zip_path = temp_root / "package.zip"
extract_root = temp_root / "extract"
extract_root.mkdir()
url = f"https://github.com/{repository}/archive/refs/heads/{branch}.zip"
print(f"Downloading: {url}", file=sys.stderr)
request = urllib.request.Request(url, headers={"User-Agent": "zno-project-command-skills-installer"})
with urllib.request.urlopen(request, timeout=60) as response:
    zip_path.write_bytes(response.read())
with zipfile.ZipFile(zip_path) as archive:
    archive.extractall(extract_root)
for candidate in extract_root.iterdir():
    if candidate.is_dir() and ((candidate / "skills").is_dir() or (candidate / "claude-skills").is_dir()):
        print(candidate)
        raise SystemExit(0)
raise SystemExit("Downloaded package does not contain skills or claude-skills.")
PY
}

backup_existing() {
  local target_root="$1"
  shift
  local skill_names=("$@")
  local existing=()

  for name in "${skill_names[@]}"; do
    if [ -e "$target_root/$name" ]; then
      existing+=("$target_root/$name")
    fi
  done

  if [ "${#existing[@]}" -eq 0 ]; then
    return 0
  fi

  local backup_root="$target_root/.backup/zno-project-command-skills-$(date +%Y%m%d-%H%M%S)"
  mkdir -p "$backup_root"
  for path in "${existing[@]}"; do
    cp -R "$path" "$backup_root/$(basename "$path")"
  done
  echo "Backup created: $backup_root"
}

install_skill_set() {
  local kind="$1"
  local root="$2"
  local source_root target_root restart_text
  local skill_names=()

  if [ "$kind" = "codex" ]; then
    source_root="$root/skills"
    target_root="$CODEX_TARGET_ROOT"
    restart_text="Restart Codex desktop so the command menu can rescan skills."
    skill_names=("${CODEX_SKILL_NAMES[@]}")
  else
    source_root="$root/claude-skills"
    target_root="$CLAUDE_TARGET_ROOT"
    restart_text="Restart Claude Code so it can rescan skills."
    skill_names=("${CLAUDE_SKILL_NAMES[@]}")
  fi

  if [ ! -d "$source_root" ]; then
    echo "Missing $kind source directory: $source_root" >&2
    exit 1
  fi

  for name in "${skill_names[@]}"; do
    if [ ! -f "$source_root/$name/SKILL.md" ]; then
      echo "Missing $kind skill: $name" >&2
      exit 1
    fi
  done

  echo
  echo "== $kind =="
  echo "Source: $source_root"
  echo "Target: $target_root"

  if [ "$DRY_RUN" -eq 1 ]; then
    for name in "${skill_names[@]}"; do
      if [ -e "$target_root/$name" ]; then
        action="update"
      else
        action="install"
      fi
      echo "Would $action: $name -> $target_root/$name"
    done
    return
  fi

  mkdir -p "$target_root"
  backup_existing "$target_root" "${skill_names[@]}"

  for name in "${skill_names[@]}"; do
    rm -rf "$target_root/$name"
    cp -R "$source_root/$name" "$target_root/$name"
    echo "Installed: $name"
  done

  echo "$restart_text"
}

mapfile -t SELECTED_TOOLS < <(selected_tools)
if [ "${#SELECTED_TOOLS[@]}" -eq 0 ]; then
  echo "No Codex or Claude Code installation was detected. Use --tool codex, --tool claude, or --tool all to install anyway." >&2
  exit 1
fi

PACKAGE_ROOT="$(package_root)"
echo "Package root: $PACKAGE_ROOT"
echo "Selected tools: ${SELECTED_TOOLS[*]}"

for selected_tool in "${SELECTED_TOOLS[@]}"; do
  install_skill_set "$selected_tool" "$PACKAGE_ROOT"
done

if [ "$DRY_RUN" -eq 1 ]; then
  echo
  echo "Dry run complete. No local skills were changed."
fi
