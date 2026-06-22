# AI Project Command Skills

[简体中文](README.zh-CN.md) | English

Document-first workflow skills for AI coding assistants. The package supports both Codex and Claude Code, with commands for project kickoff, feature work, goal-mode execution, handoff, and cross-chat continuation.

The skills help an AI coding assistant clarify requirements, maintain project docs, make technical decisions deliberately, and keep enough project state on disk for future chats or developers to continue.

## Command Names

Codex uses the original command names. Claude Code uses `ai-` prefixed aliases to avoid collisions with built-in Claude Code commands such as `/init`, `/plan`, and `/upgrade`.

| Purpose | Codex | Claude Code |
| --- | --- | --- |
| Start a new project | `/init` | `/ai-init` |
| Run a long project or phase objective | `/goal` | `/ai-goal` |
| High-autonomy goal mode | `/goal --super` | `/ai-goal --super` |
| High-autonomy alias | `/super` | `/ai-super` |
| Add a new feature | `/feature` | `/ai-feature` |
| Change existing behavior or rules | `/change` | `/ai-change` |
| Diagnose and fix a bug | `/fix` | `/ai-fix` |
| Compare technical options | `/tech` | `/ai-tech` |
| Update deployment or release guidance | `/deploy` | `/ai-deploy` |
| Update onboarding and handoff guidance | `/handoff` | `/ai-handoff` |
| Update phases, milestones, and priorities | `/roadmap` | `/ai-roadmap` |
| Recommend next features or improvements | `/plan` | `/ai-plan` |
| Write a current progress snapshot | `/status` | `/ai-status` |
| Resume work in a new chat | `/continue` | `/ai-continue` |
| Update installed skills or project docs | `/upgrade` | `/ai-upgrade` |

## One-Step Install Or Update

Use the auto installer when you want one script to configure everything it can find on the machine. It detects Codex and Claude Code, then installs or updates the matching skill packages.

### Windows

```powershell
powershell -ExecutionPolicy Bypass -File .\install-all.ps1
```

### macOS/Linux

```bash
chmod +x ./install-all.sh
./install-all.sh
```

Install from the latest GitHub package without cloning the full repo:

```powershell
powershell -ExecutionPolicy Bypass -File .\install-all.ps1 -Source github
```

```bash
./install-all.sh --source github
```

Force installation for both tools even if auto-detection does not find them:

```powershell
powershell -ExecutionPolicy Bypass -File .\install-all.ps1 -Tool all
```

```bash
./install-all.sh --tool all
```

Preview changes without writing local skills:

```powershell
powershell -ExecutionPolicy Bypass -File .\install-all.ps1 -Source github -DryRun
```

```bash
./install-all.sh --source github --dry-run
```

## Install For Codex Only

Clone this repository or download the source zip, then run the installer from the repository root.

### Windows

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

### macOS/Linux

```bash
chmod +x ./install.sh
./install.sh
```

The Codex installer copies skills into:

```text
~/.agents/skills
```

Restart Codex desktop after installation so the command menu can rescan the skills.

## Install For Claude Code Only

### Windows

```powershell
powershell -ExecutionPolicy Bypass -File .\install-claude.ps1
```

### macOS/Linux

```bash
chmod +x ./install-claude.sh
./install-claude.sh
```

The Claude Code installer copies alias skills into:

```text
~/.claude/skills
```

Restart Claude Code after installation so it can rescan the skills. Use `/ai-init`, `/ai-goal`, `/ai-feature`, and the other `ai-` commands in Claude Code.

## Typical Usage

Start a new project:

```text
/init Build a team task management app with login, projects, kanban tasks, member invites, basic permissions, local setup, and deployment docs.
```

Claude Code equivalent:

```text
/ai-init Build a team task management app with login, projects, kanban tasks, member invites, basic permissions, local setup, and deployment docs.
```

Run a whole goal in high-autonomy mode:

```text
/goal --super Complete the team task management MVP. Make ordinary product and technical decisions yourself, record key decisions, and only stop for paid services, destructive actions, secrets, production data, or security/compliance risks.
```

Claude Code equivalent:

```text
/ai-goal --super Complete the team task management MVP. Make ordinary product and technical decisions yourself, record key decisions, and only stop for paid services, destructive actions, secrets, production data, or security/compliance risks.
```

Resume in a new chat:

```text
/continue
```

Before leaving a chat:

```text
/status
```

Update the locally installed skills from the latest GitHub package:

```text
/upgrade Update my local skills from GitHub.
```

Claude Code equivalent:

```text
/ai-upgrade Update my local skills from GitHub.
```

## Project Docs Created By The Skills

When initialized, projects receive a document set like:

```text
AI_DEVELOPMENT_RULES.md
docs/
  00_START_HERE.md
  README.md
  product/
    01-requirements-clarification.md
    06-roadmap.md
    15-frontend-design.md
  engineering/
    02-development-principles.md
    04-tech-decisions.md
    11-project-structure.md
  development/
    03-feature-changelog.md
    10-current-status.md
    14-decision-log.md
  operations/
    07-local-development.md
    08-deployment.md
  handoff/
    05-handoff-guide.md
  maintenance/
    09-ai-project-start-prompt.md
    12-upgrade-history.md
    13-command-reference.md
```

These files are the continuity layer. They let another chat, another AI assistant, or another developer understand what has been decided and what remains. `docs/README.md` keeps the root entry points small and groups the rest of the docs into parent folders. `docs/product/15-frontend-design.md` captures product surface, UI references, design keywords, colors, layout, component style, interaction states, and frontend pitfalls.

## Design Principles

- New projects start with clarification and docs before implementation.
- Existing projects use `/upgrade` or `/ai-upgrade`, not a destructive re-init.
- Technical choices normally require options and confirmation.
- `--super` skips ordinary confirmation but records important decisions.
- Page-facing work must end with manual browser test steps.
- UI projects start by collecting or recommending UI style references and recording the design direction in `docs/product/15-frontend-design.md`.
- Cross-chat continuity goes through `docs/development/10-current-status.md`.
- Project structure knowledge goes into `docs/engineering/11-project-structure.md`.
- Command semantics are documented in `docs/maintenance/13-command-reference.md`.
- High-autonomy decisions are recorded in `docs/development/14-decision-log.md`.

## Repository Layout

```text
skills/                 Codex skill folders installed into ~/.agents/skills
claude-skills/          Claude Code alias skill folders installed into ~/.claude/skills
install-all.ps1         Auto-detecting Windows installer/updater for Codex and Claude Code
install-all.sh          Auto-detecting macOS/Linux installer/updater for Codex and Claude Code
install.ps1             Codex Windows installer
install.sh              Codex macOS/Linux installer
install-claude.ps1      Claude Code Windows installer
install-claude.sh       Claude Code macOS/Linux installer
README.md               Project documentation
README.zh-CN.md         Simplified Chinese documentation
LICENSE                 MIT license
CHANGELOG.md            Release notes
CHANGELOG.zh-CN.md      Simplified Chinese release notes
CONTRIBUTING.md         Contribution guide
CONTRIBUTING.zh-CN.md   Simplified Chinese contribution guide
SECURITY.md             Security policy
SECURITY.zh-CN.md       Simplified Chinese security policy
```

Each command is packaged as a standalone skill folder. The repository intentionally duplicates the bundled project template across command aliases for easy installation and offline use.

## Updating Installed Skills

For Codex:

```text
/upgrade Update my local skills from GitHub.
```

For Claude Code:

```text
/ai-upgrade Update my local skills from GitHub.
```

The updater downloads the latest package from `1447751897/ai-project-command-skills`, validates the skill folders, backs up existing installed skills under the target tool's `.backup/` directory, then replaces the installed skill folders. Restart the relevant tool after the update.

Manual update still works too. Pull the latest repository changes and rerun the auto installer:

```bash
git pull
./install-all.sh
```

On Windows:

```powershell
git pull
powershell -ExecutionPolicy Bypass -File .\install-all.ps1
```

Inside a project that was already initialized, run `/upgrade` in Codex or `/ai-upgrade` in Claude Code. This adds missing new docs and rules without overwriting project-specific content.
