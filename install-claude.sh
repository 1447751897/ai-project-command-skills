#!/usr/bin/env bash
set -euo pipefail

PACKAGE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SOURCE="$PACKAGE_ROOT/skills"
TARGET_ROOT="${1:-$HOME/.claude/skills}"

if [ ! -d "$SKILLS_SOURCE" ]; then
  echo "Missing Claude skills directory: $SKILLS_SOURCE" >&2
  exit 1
fi

mkdir -p "$TARGET_ROOT"

SKILL_NAMES=(
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

for name in "${SKILL_NAMES[@]}"; do
  source="$SKILLS_SOURCE/$name"
  target="$TARGET_ROOT/$name"

  if [ ! -d "$source" ]; then
    echo "Skip missing skill: $name" >&2
    continue
  fi

  rm -rf "$target"
  cp -R "$source" "$target"
  echo "Installed: $name"
done

echo
echo "Done. Restart Claude Code, then try /zno-init, /zno-goal, /zno-goal --super, /zno-feature, /zno-fix, /zno-tech, /zno-deploy, /zno-handoff, /zno-roadmap, /zno-plan, /zno-status, /zno-continue, or /zno-upgrade. /zno-super is also available as a compatibility alias."
