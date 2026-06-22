# Changelog

[简体中文](CHANGELOG.zh-CN.md) | English

## 0.2.1 - 2026-06-22

Frontend design initialization and parent-folder doc classification.

- Added `docs/product/15-frontend-design.md` to the initialized project template.
- `/init` now collects or recommends UI style references for UI-facing projects and records design keywords, colors, layout, component style, interaction states, and pitfalls to avoid.
- Moved generated project docs into parent folders and documented the category layout in `docs/README.md`.
- Updated Codex and Claude Code skill templates so frontend design changes are tracked during later feature/change work.

## 0.2.0 - 2026-06-18

Claude Code compatibility.

- Added auto-detecting installers: `install-all.ps1` and `install-all.sh`.
- Auto installers can install/update detected Codex and Claude Code packages from either the local repo or the latest GitHub package.
- Added Claude Code alias skills under `claude-skills/`.
- Added Claude Code installers: `install-claude.ps1` and `install-claude.sh`.
- Added `/ai-*` command aliases for Claude Code to avoid conflicts with built-in commands such as `/init`, `/plan`, and `/upgrade`.
- Extended the GitHub self-updater with `--tool codex|claude`, so Codex updates `~/.agents/skills` and Claude Code updates `~/.claude/skills`.
- Updated English and Simplified Chinese documentation with dual-tool installation and command tables.

## 0.1.1 - 2026-06-17

Documentation update.

- Added Simplified Chinese documentation for Chinese-speaking users.
- Added language links between English and Chinese documentation files.
- Added a local skills updater for `/upgrade` so installed skills can be refreshed from the latest GitHub package.

## 0.1.0 - 2026-06-17

Initial open-source release.

Included commands:

- `/init`
- `/goal`
- `/goal --super`
- `/super` compatibility alias
- `/feature`
- `/change`
- `/fix`
- `/tech`
- `/deploy`
- `/handoff`
- `/roadmap`
- `/plan`
- `/status`
- `/continue`
- `/upgrade`

Included project docs:

- `AI_DEVELOPMENT_RULES.md`
- `docs/00_START_HERE.md`
- `docs/product/01-requirements-clarification.md`
- `docs/engineering/02-development-principles.md`
- `docs/development/03-feature-changelog.md`
- `docs/engineering/04-tech-decisions.md`
- `docs/handoff/05-handoff-guide.md`
- `docs/product/06-roadmap.md`
- `docs/operations/07-local-development.md`
- `docs/operations/08-deployment.md`
- `docs/maintenance/09-ai-project-start-prompt.md`
- `docs/development/10-current-status.md`
- `docs/engineering/11-project-structure.md`
- `docs/maintenance/12-upgrade-history.md`
- `docs/maintenance/13-command-reference.md`
- `docs/development/14-decision-log.md`
