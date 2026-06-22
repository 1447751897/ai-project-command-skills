---
name: ai-upgrade
description: Use when the user writes /ai-upgrade, wants to update local installed skills from GitHub, refresh ~/.claude/skills, update slash commands, or apply newer project workflow templates to an initialized project. For local skill package updates, download the latest GitHub package and update installed skills. For project docs upgrades, copy only missing docs, preserve existing content, record upgrade history, update current status, and propose additive merges for new rules. Also follows the shared project-kickoff document-first workflow and supports related prefixes /ai-init, /ai-goal, /ai-goal --super, /ai-super, /ai-feature, /ai-change, /ai-fix, /ai-tech, /ai-deploy, /ai-handoff, /ai-roadmap, /ai-plan, /ai-status, /ai-continue, and /ai-upgrade. Includes frontend design direction, UI style reference collection, design keywords, and frontend design documentation updates.
---

# Ai-Upgrade
## Claude Code Compatibility

This is the Claude Code alias of the 'upgrade' workflow skill. Use the '/ai-upgrade' slash command in Claude Code. The 'ai-' prefix avoids collisions with Claude Code built-in commands such as '/init', '/plan', and '/upgrade' while preserving the same document-first workflow semantics.


Use this skill to make project development document-first and continuity-friendly. It enforces a repeatable loop: clarify requirements, initialize or update project docs, get confirmation when direction matters, then implement.

## Command Prefixes

Treat these user message prefixes as commands for this skill:

```text
/ai-init <project requirement>
/ai-goal <project or phase objective>
/ai-goal --super <project or phase objective>
/ai-super <project or phase objective>   # compatibility alias for /ai-goal --super
/ai-feature <new feature requirement>
/ai-change <change to existing behavior>
/ai-fix <bug or defect description>
/ai-tech <technical decision or architecture change>
/ai-deploy <deployment, environment, release, or rollback change>
/ai-handoff <handoff note or onboarding change>
/ai-roadmap <phase, priority, or milestone change>
/ai-plan <optional planning question>
/ai-status <optional progress note>
/ai-continue <optional next task>
/ai-upgrade <optional upgrade note>
```

Command behavior:

- `/ai-init`: initialize missing docs if needed, restate the project goal, ask clarification questions, then prepare the initial docs. Do not implement before confirmation.
- `/ai-goal`: use goal-mode execution when available, or emulate goal-mode execution otherwise. Create/enter a long-running objective, initialize or continue the project docs as needed, break the goal into phases/tasks, then autonomously progress through the workflow until completion, a required confirmation gate, or a real blocker.
- `/ai-goal --super`: high-autonomy variant of `/ai-goal`. Do not stop for ordinary product/technical confirmations; choose the recommended path, continue implementation, and record key decisions in `docs/development/14-decision-log.md`. Still stop for paid services, production data deletion, secrets, destructive git operations, or clear security/compliance risks.
- `/ai-super`: compatibility alias for `/ai-goal --super`.
- `/ai-feature`: treat as a mid-project new feature. Clarify if needed, update requirements/roadmap/tech docs as relevant, implement after confirmation when direction matters, then update the changelog.
- `/ai-change`: treat as a behavior or scope change. Identify affected docs and code before implementation.
- `/ai-fix`: reproduce or reason about the defect, keep the docs update lightweight, and update the changelog after the fix if behavior changes.
- `/ai-tech`: update `docs/engineering/04-tech-decisions.md` before or alongside any implementation.
- `/ai-deploy`: update `docs/operations/08-deployment.md`, and update `docs/operations/07-local-development.md` if local commands or env vars change.
- `/ai-handoff`: update `docs/handoff/05-handoff-guide.md`.
- `/ai-roadmap`: update `docs/product/06-roadmap.md`.
- `/ai-plan`: when the user has no clear next step or asks what to add/improve, read existing docs, recommend feature/optimization directions with value, complexity, priority, dependencies, and risks, then wait for the user to choose. Do not implement directly.
- `/ai-status`: inspect the current workspace, recent changes, docs, tests, and known pending work; update `docs/development/10-current-status.md` with a concise handoff-ready snapshot. Do not implement new work unless the user explicitly asks.
- `/ai-continue`: read `AI_DEVELOPMENT_RULES.md`, `docs/00_START_HERE.md`, `docs/development/10-current-status.md`, `docs/development/03-feature-changelog.md`, `docs/product/06-roadmap.md`, and `docs/handoff/05-handoff-guide.md`; summarize current state and continue only after identifying the next safe task.
- `/ai-upgrade`: if the user asks to update local skills, run `scripts/update_installed_skills.py` to download the latest GitHub package and update `~/.claude/skills`; otherwise copy only missing project template docs, preserve existing content, update `docs/maintenance/12-upgrade-history.md`, and then update `docs/development/10-current-status.md`.

If the user omits the skill name but starts with one of these prefixes, apply this skill.

## Core Workflow

For a new project:

1. Inspect the current workspace for existing docs and project files.
2. If the project lacks the required docs, run `scripts/init_project_docs.py <project-root>` to copy the template files.
3. Read `AI_DEVELOPMENT_RULES.md` and `docs/00_START_HERE.md` after initialization.
4. Restate the user's project goal in plain language.
5. Ask only the clarification questions that affect product scope, architecture, data, permissions, deployment, frontend design direction, or acceptance.
6. If the project has any user interface, identify whether it is a website, mini program, browser extension, app, desktop app, internal tool, admin system, dashboard, or other surface; collect or recommend 2-5 UI style references; then extract overall mood, colors, layout, card/component style, interaction states, and things to avoid into `docs/product/15-frontend-design.md`.
7. After the user confirms, fill or update the docs under `docs/`.
8. Do not start implementation until the requirements and initial docs are confirmed.

For mid-project new requirements:

1. Do not ask the user to paste the kickoff prompt again.
2. Classify the request as new feature, change, bug fix, UX improvement, technical adjustment, or deployment change.
3. Restate the requirement briefly.
4. Ask clarification questions only if the request affects scope, business rules, data shape, permissions, technical decisions, deployment, or acceptance.
5. Update the relevant docs before or alongside code changes.
6. Always update `docs/development/03-feature-changelog.md` after a feature, change, deletion, or fix.
7. Update `docs/product/15-frontend-design.md` when the request affects product surface, UI style, layout, component strategy, interaction states, or frontend experience boundaries.
8. Final response must include page-level manual test steps when the change affects user-visible UI or browser workflows.

For technical choices:

1. If work involves core frameworks, databases, cache, queues, auth, storage, payment, email/SMS/push, deployment, CI/CD, monitoring, logging, schedulers, heavy frontend libraries, or any dependency/service with meaningful performance/cost/security/maintenance impact, do not implement immediately.
2. Present 2-3 viable options with purpose, pros, cons, performance impact, cost, maintenance complexity, risks, and rollback.
3. Recommend one option and explain why.
4. Wait for user confirmation unless the user explicitly specified the technology and explicitly waived comparison.
5. After confirmation, record the decision in `docs/engineering/04-tech-decisions.md`, then implement.

For open-ended planning:

1. Trigger this flow when the user writes `/ai-plan` or says they have no idea what to add, asks what to do next, asks how to improve the project, or wants feature recommendations.
2. Read `docs/product/01-requirements-clarification.md`, `docs/development/03-feature-changelog.md`, `docs/product/06-roadmap.md`, `docs/development/10-current-status.md`, and `docs/engineering/11-project-structure.md`.
3. Identify the current project phase and whether the core user journey is complete.
4. Recommend 3-7 candidate directions across core workflow gaps, UX polish, admin/permissions/audit, performance, security, deployment/observability, data/reporting, and operations/commercialization when relevant.
5. For each candidate, include user value, priority, implementation complexity, dependencies, performance/security/deployment impact, and whether a technical-selection gate may be needed.
6. Recommend the top 1-2 next steps and ask the user to choose.
7. Do not implement until the user selects a direction.

For goal-mode automatic execution:

1. Trigger this flow when the user writes `/ai-goal`, asks to fully complete a project/phase, or says they do not want to keep issuing per-feature commands.
2. If the environment exposes a goal tool, create a goal with the user's objective. If not, treat the current conversation as goal-mode and state that the workflow will be followed manually.
3. If the project is not initialized, run the `/ai-init` workflow first: clarify only essential product/technical uncertainties, scaffold docs, and wait for required confirmations.
4. If the project is already initialized, run the `/ai-continue` workflow first: read project rules, current status, roadmap, changelog, handoff, project structure, command reference, and technical decisions.
5. Break the goal into phases and immediate tasks, then keep progressing without requiring the user to type `/ai-feature`, `/ai-status`, or `/ai-continue`.
6. Apply the same gates internally: use `/ai-plan` behavior when the next step is unclear, `/ai-tech` behavior for major technical selections, `/ai-feature` or `/ai-change` behavior for implementation tasks, `/ai-fix` behavior for defects, and `/ai-deploy` behavior for deployment work.
7. Update relevant docs after each meaningful unit of work, especially `docs/development/03-feature-changelog.md`, `docs/product/06-roadmap.md`, `docs/development/10-current-status.md`, and `docs/engineering/11-project-structure.md`.
8. Stop and ask the user only for required decisions: product boundary ambiguity, major technology selection, paid/external services, production deployment, security/permission/data deletion/compliance risk, or an actual blocker.
9. Low-risk implementation details may be decided autonomously and recorded in the relevant docs.
10. When the goal is genuinely achieved, mark the Goal complete if the environment provides a goal status tool; otherwise summarize completion and remaining risks.

For super high-autonomy execution:

1. Trigger this flow when the user writes `/ai-goal --super`, uses `/ai-super`, or explicitly says to proceed without asking ordinary confirmation questions.
2. Enter `/ai-goal` behavior, but treat ordinary technical/product choices as AI-owned decisions.
3. For major choices, still compare options internally, select the best fit, implement it, and record the decision in `docs/development/14-decision-log.md`.
4. Continue without waiting for user confirmation unless the decision involves paid services, production data deletion, secrets, destructive git operations, or clear security/compliance risk.
5. Final responses must summarize the important decisions made, why they were made, risks, rollback options, validation, and page manual test steps when UI is affected.

## Required Docs

The project documentation set is:

- `AI_DEVELOPMENT_RULES.md`: durable AI development rules.
- `docs/00_START_HERE.md`: kickoff and mid-project requirement workflow.
- `docs/README.md`: document index and parent-folder classification.
- `docs/product/01-requirements-clarification.md`: project goals, users, flows, data, acceptance, open questions.
- `docs/engineering/02-development-principles.md`: project-specific product, tech, UI, API, data, security, and quality rules.
- `docs/development/03-feature-changelog.md`: feature/change/fix history.
- `docs/engineering/04-tech-decisions.md`: technical decisions with purpose, reasons, alternatives, tradeoffs, and impact.
- `docs/handoff/05-handoff-guide.md`: how future developers or AI agents should enter the project.
- `docs/product/06-roadmap.md`: phase roadmap, MVP scope, enhancement phase, launch readiness.
- `docs/operations/07-local-development.md`: local setup, environment variables, commands, debugging, common issues.
- `docs/operations/08-deployment.md`: build, deploy, environment, verification, migration, rollback, operations.
- `docs/maintenance/09-ai-project-start-prompt.md`: optional first-message prompt for tools that do not automatically use skills.
- `docs/development/10-current-status.md`: current progress snapshot for cross-chat continuation and handoff.
- `docs/engineering/11-project-structure.md`: project directory map, module responsibilities, key files, data/request flow, and file placement rules.
- `docs/maintenance/12-upgrade-history.md`: Skill/template upgrade history and migration notes for previously initialized projects.
- `docs/maintenance/13-command-reference.md`: command list, use cases, effects, and docs each command updates.
- `docs/development/14-decision-log.md`: key decision log, especially for `/ai-super` mode where AI proceeds without ordinary confirmations.
- `docs/product/15-frontend-design.md`: product surface, UI references, design keywords, color, layout, card/component style, interaction states, and frontend pitfalls to avoid.

## Initialization Script

Use the script when a workspace needs the docs scaffold:

```powershell
python <installed-skills-dir>/ai-init/scripts/init_project_docs.py <project-root>
```

Behavior:

- Creates `AI_DEVELOPMENT_RULES.md` and `docs/` templates.
- Skips files that already exist.
- Use `--overwrite` only if the user explicitly asks to replace existing docs.

Use the local skills updater when the user asks to update this skill package, update local commands, pull the latest GitHub package, or refresh `~/.claude/skills`:

```powershell
python <installed-skills-dir>/ai-upgrade/scripts/update_installed_skills.py
```

Behavior:

- Downloads `https://github.com/1447751897/ai-project-command-skills` as a zip archive.
- Validates that all expected skill folders are present.
- Backs up existing installed skills under `~/.claude/skills/.backup/`.
- Replaces the installed skill folders and tells the user to restart Claude Code.

Use the project docs upgrade script when a project was initialized by an older skill version and the user asks to add missing project docs or template rules:

```powershell
python <installed-skills-dir>/ai-upgrade/scripts/upgrade_project_docs.py <project-root>
```

Behavior:

- Copies only missing files from the current template.
- Never overwrites existing project docs.
- Appends an entry to `docs/maintenance/12-upgrade-history.md`.

## Documentation Update Rules

When a user gives a new requirement, update docs according to impact:

- Product scope, users, roles, workflows, acceptance: update `product/01-requirements-clarification.md`.
- Project-specific coding, UI, API, data, security, or quality rules: update `engineering/02-development-principles.md`.
- Any completed feature/change/fix: update `development/03-feature-changelog.md`.
- New framework, library, service, architecture, database, auth, deployment strategy, or major tradeoff: update `engineering/04-tech-decisions.md`.
- New handoff notes, important directories, common tasks, or pitfalls: update `handoff/05-handoff-guide.md`.
- Phase scope, priority, MVP boundary, launch readiness: update `product/06-roadmap.md`.
- Local commands, env vars, database setup, debug steps: update `operations/07-local-development.md`.
- Build, deploy, env, migration, verification, rollback, ops: update `operations/08-deployment.md`.
- Conversation switch, pause, handoff, current task, recent file changes, verification state, pending work: update `development/10-current-status.md`.
- Directory layout, module boundaries, key file responsibilities, request/data flow, placement rules: update `engineering/11-project-structure.md`.
- Template or rule upgrades, newly added docs, manual merge notes: update `maintenance/12-upgrade-history.md`.
- Command additions, removals, or behavior changes: update `maintenance/13-command-reference.md`.
- High-autonomy decisions, skipped confirmation gates, major technical/product choices: update `development/14-decision-log.md`.
- Product surface, UI style references, design keywords, color/layout/component strategy, interaction states, frontend pitfalls: update `product/15-frontend-design.md`.

## Performance-Aware Design

During clarification, technical decisions, and implementation planning, consider performance before writing code:

1. For frontend work, consider route-level lazy loading, component-level dynamic imports, tree-shakable libraries, avoiding full-package imports, asset compression, and avoiding unnecessary re-renders.
2. For heavy UI features such as charts, rich text, maps, tables, editors, and file previews, prefer loading them only when needed.
3. For lists, logs, tables, messages, and large datasets, consider pagination, virtualization, filtering, and incremental loading.
4. For backend work, consider query shape, indexes, pagination, caching, batching, connection reuse, timeouts, and avoiding N+1 queries.
5. For APIs, avoid oversized responses and request waterfalls; document defaults and limits.
6. Record meaningful performance tradeoffs in `docs/engineering/04-tech-decisions.md`.

## Technical Selection Gate

Never silently pick major technology. Use this gate for:

- frontend/backend framework or build/runtime choices;
- database, cache, message queue, search, object storage;
- authentication, permissions, payment, email, SMS, push, third-party login;
- deployment platform, CI/CD, containerization, monitoring, logging, scheduled jobs;
- heavy frontend dependencies such as charts, rich text, maps, tables, editors, file previews;
- any new dependency or service that affects bundle size, runtime performance, cost, security, or long-term maintenance.

Required recommendation format:

```text
Technical need:
Constraints:
Option A:
Option B:
Option C:
Recommended option:
Why:
Performance impact:
Maintenance cost:
Risks and rollback:
Question for confirmation:
```

Do not proceed to implementation until the user confirms the selected option.

## Cross-Chat Continuation

When handling `/ai-status`:

1. Inspect relevant docs and, if available, git status/recent changed files.
2. Record the current phase, current task, completed work, in-progress work, pending next steps, blockers, recent file changes, verification run, verification not run, and continuation advice in `docs/development/10-current-status.md`.
3. Keep the snapshot factual. Do not claim tests ran unless they actually ran.
4. Final response should tell the user that the status snapshot was updated and what the next recommended step is.

When handling `/ai-continue`:

1. Read the current status doc first.
2. Read the minimum supporting docs needed to avoid guessing: usually `00_START_HERE`, `03-feature-changelog`, `06-roadmap`, `05-handoff-guide`, and `13-command-reference`.
3. Read `AI_DEVELOPMENT_RULES.md` and `docs/engineering/04-tech-decisions.md` before making implementation or technology choices.
4. Inspect the workspace for current files and uncommitted changes before editing.
5. Briefly summarize where the project left off.
6. Continue with the next task only if it is clear; otherwise ask the smallest necessary clarification question.
7. If the next task requires a new technical choice, use the Technical Selection Gate before implementation.

When handling `/ai-upgrade`:

1. Classify the request first.
2. If the user asks to update local skills, commands, this skill package, or the latest GitHub version, run `scripts/update_installed_skills.py`. Use `--dry-run` first when the user asks to preview only.
3. If the user asks to upgrade an initialized project, run `scripts/upgrade_project_docs.py <project-root>` or manually apply the same behavior.
4. For project docs upgrades, never overwrite existing project docs; read the list of new files, summarize what was added, propose/apply additive merges for new rules, and update `docs/development/10-current-status.md`.
5. For local skill package updates, summarize the downloaded repository/branch, target install path, backup path if created, installed commands, and tell the user to restart Claude Code.

When handling `/ai-goal`:

1. Create or enter a long-running objective if Goal tooling is available.
2. Do not wait for the user to issue the next command after every task.
3. Keep applying this skill's docs, gates, and update rules automatically.
4. Keep the user informed at meaningful checkpoints, especially before any required confirmation gate.
5. Use `/ai-status` behavior automatically at phase boundaries, before stopping, and after meaningful progress.

When handling `/ai-goal --super` or `/ai-super`:

1. Create or enter a long-running objective if Goal tooling is available.
2. Apply `/ai-goal` behavior without stopping for ordinary confirmations.
3. Record key decisions in `docs/development/14-decision-log.md`.
4. Stop only for paid/external service activation, production data deletion, secrets, destructive git operations, or clear security/compliance risk.

## Interaction Rules

- Treat this skill as a long-lived project agreement once invoked for a project.
- For the first project request, insist on clarification and docs before implementation.
- For later requests, continue the same workflow automatically without requiring the long prompt again.
- If the user explicitly says to skip docs for a tiny fix, keep the change small and still update the changelog if behavior changed.
- Never invent unknown business rules. Mark unresolved items in the relevant doc and ask the smallest useful question.
- After completing a requirement, feature, change, or bug fix, include manual browser/page testing steps in the final response. If no page is involved, say so and give the relevant API, command, or configuration verification.

## Final Response Test Steps

When work affects a page, interaction, visible data, form, navigation, or browser workflow, include:

```text
页面测试步骤：
1. 打开：
2. 前置条件：
3. 操作：
4. 输入：
5. 预期结果：
6. 异常/边界验证：
```

Keep the steps practical and executable by the user in the browser. Include at least one happy path and, when relevant, one or two boundary/error checks. Do not replace page steps with only command-line test output.
