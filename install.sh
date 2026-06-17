#!/usr/bin/env bash
set -euo pipefail

PACKAGE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SOURCE="$PACKAGE_ROOT/skills"
TARGET_ROOT="$HOME/.agents/skills"

if [ ! -d "$SKILLS_SOURCE" ]; then
  echo "Missing skills directory: $SKILLS_SOURCE" >&2
  exit 1
fi

mkdir -p "$TARGET_ROOT"

SKILL_NAMES=(
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
echo "Done. Restart Codex desktop, then try /init, /goal, /goal --super, /feature, /fix, /tech, /deploy, /handoff, /roadmap, /plan, /status, /continue, or /upgrade. /super is also available as a compatibility alias."
