# AI Project Command Skills

Document-first Codex skills for project kickoff, feature work, goal-mode execution, handoff, and cross-chat continuation.

This package installs a set of slash-style workflow skills such as `/init`, `/goal`, `/feature`, `/status`, and `/continue`. The skills help an AI coding assistant clarify requirements, maintain project docs, make technical decisions deliberately, and keep enough project state on disk for future chats or developers to continue.

## Commands

| Command | Purpose |
| --- | --- |
| `/init` | Start a new project: clarify requirements, scaffold project docs, and wait for confirmation before development. |
| `/goal` | Run a long project or phase objective with automatic task breakdown and progress. |
| `/goal --super` | High-autonomy goal mode: AI makes ordinary product/technical decisions and records them. |
| `/super` | Compatibility alias for `/goal --super`. |
| `/feature` | Add a new feature with docs, changelog, and page test steps. |
| `/change` | Change existing behavior or business rules with impact tracking. |
| `/fix` | Diagnose, fix, verify, and record a bug fix. |
| `/tech` | Compare technical options before adopting a major dependency or architecture choice. |
| `/deploy` | Update deployment, environment, CI/CD, release, or rollback guidance. |
| `/handoff` | Update onboarding, project structure, and handoff guidance. |
| `/roadmap` | Update phases, MVP scope, milestones, and priorities. |
| `/plan` | Recommend next features or improvements when you do not know what to build next. |
| `/status` | Write a current progress snapshot for later continuation. |
| `/continue` | Resume work in a new chat from project docs and current status. |
| `/upgrade` | Add missing docs/rules from a newer version without overwriting project content. |

## Install

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

The installer copies skills into:

```text
~/.agents/skills
```

Restart Codex desktop after installation so the command menu can rescan the skills.

## Typical Usage

Start a new project:

```text
/init Build a team task management app with login, projects, kanban tasks, member invites, basic permissions, local setup, and deployment docs.
```

Run a whole goal with normal confirmation gates:

```text
/goal Complete the team task management MVP.
```

Run a whole goal in high-autonomy mode:

```text
/goal --super Complete the team task management MVP. Make ordinary product and technical decisions yourself, record key decisions, and only stop for paid services, destructive actions, secrets, production data, or security/compliance risks.
```

Resume in a new chat:

```text
/continue
```

Before leaving a chat:

```text
/status
```

Upgrade an existing project that was initialized with an older version:

```text
/upgrade
```

## Project Docs Created By The Skills

When initialized, projects receive a document set like:

```text
AI_DEVELOPMENT_RULES.md
docs/
  00_START_HERE.md
  01-requirements-clarification.md
  02-development-principles.md
  03-feature-changelog.md
  04-tech-decisions.md
  05-handoff-guide.md
  06-roadmap.md
  07-local-development.md
  08-deployment.md
  09-ai-project-start-prompt.md
  10-current-status.md
  11-project-structure.md
  12-upgrade-history.md
  13-command-reference.md
  14-decision-log.md
```

These files are the continuity layer. They let another chat, another AI assistant, or another developer understand what has been decided and what remains.

## Design Principles

- New projects start with clarification and docs before implementation.
- Existing projects use `/upgrade`, not a destructive re-init.
- Technical choices normally require options and confirmation.
- `/goal --super` skips ordinary confirmation but records important decisions.
- Page-facing work must end with manual browser test steps.
- Cross-chat continuity goes through `docs/10-current-status.md`.
- Project structure knowledge goes into `docs/11-project-structure.md`.
- Command semantics are documented in `docs/13-command-reference.md`.
- High-autonomy decisions are recorded in `docs/14-decision-log.md`.

## Repository Layout

```text
skills/                 Skill folders installed into ~/.agents/skills
install.ps1             Windows installer
install.sh              macOS/Linux installer
README.md               Project documentation
LICENSE                 MIT license
CHANGELOG.md            Release notes
CONTRIBUTING.md         Contribution guide
SECURITY.md             Security policy
```

Each command is packaged as a standalone skill folder so Codex can expose it in the command menu. This intentionally duplicates the bundled project template across command aliases for easy installation and offline use.

## Updating Installed Skills

Pull the latest repository changes and rerun the installer:

```bash
git pull
./install.sh
```

On Windows:

```powershell
git pull
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

Then restart Codex desktop.

Inside a project that was already initialized, run:

```text
/upgrade
```

This adds missing new docs and rules without overwriting project-specific content.

