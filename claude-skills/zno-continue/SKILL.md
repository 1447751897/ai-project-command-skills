---
---
name: zno-continue
description: Use when the user writes /zno-continue or wants to resume development in a new chat. Read AI_DEVELOPMENT_RULES.md, docs/00_START_HERE.md, docs/development/10-current-status.md, feature changelog, roadmap, handoff guide, project structure doc, command reference, tech decisions, and decision log; inspect workspace state, summarize where work left off, then continue with the next safe task. Also follows the shared project-kickoff document-first workflow and supports related prefixes /zno-init, /zno-goal, /zno-goal --super, /zno-super, /zno-feature, /zno-change, /zno-fix, /zno-tech, /zno-deploy, /zno-handoff, /zno-roadmap, /zno-plan, /zno-status, /zno-continue, and /zno-upgrade. Includes frontend design direction, UI style reference collection, design keywords, and frontend design documentation updates.
---

# Zno-Init
## Claude Code Compatibility

This is the Claude Code alias of the 'init' workflow skill. Use the '/zno-init' slash command in Claude Code. The 'zno-' prefix avoids collisions with Claude Code built-in commands such as '/init', '/plan', and '/upgrade' while preserving the same document-first workflow semantics.


Use this skill to make project development document-first and continuity-friendly. It enforces a repeatable loop: clarify requirements, initialize or update project docs, get confirmation when direction matters, then implement.

## Command Prefixes

Treat these user message prefixes as commands for this skill:

```text
/zno-init <project requirement>
/zno-goal <project or phase objective>
/zno-goal --super <project or phase objective>
/zno-super <project or phase objective>   # compatibility alias for /zno-goal --super
/zno-feature <new feature requirement>
/zno-change <change to existing behavior>
/zno-fix <bug or defect description>
/zno-tech <technical decision or architecture change>
/zno-deploy <deployment, environment, release, or rollback change>
/zno-handoff <handoff note or onboarding change>
/zno-roadmap <phase, priority, or milestone change>
/zno-plan <optional planning question>
/zno-status <optional progress note>
/zno-continue <optional next task>
/zno-review <optional scope or branch>
/zno-upgrade <optional upgrade note>
```

Command behavior:

- `/zno-init`: initialize missing docs if needed, restate the project goal, ask clarification questions, then prepare the initial docs. Do not implement before confirmation.
- `/zno-goal`: use goal-mode execution when available, or emulate goal-mode execution otherwise. Create/enter a long-running objective, initialize or continue the project docs as needed, break the goal into phases/tasks, then autonomously progress through the workflow until completion, a required confirmation gate, or a real blocker.
- `/zno-goal --super`: high-autonomy variant of `/zno-goal`. Do not stop for ordinary product/technical confirmations; choose the recommended path, continue implementation, and record key decisions in `docs/development/14-decision-log.md`. Still stop for paid services, production data deletion, secrets, destructive git operations, or clear security/compliance risks.
- `/zno-super`: compatibility alias for `/zno-goal --super`.
- `/zno-feature`: treat as a mid-project new feature. Clarify if needed, update requirements/roadmap/tech docs as relevant, implement after confirmation when direction matters, then update the changelog.
- `/zno-change`: treat as a behavior or scope change. Identify affected docs and code before implementation.
- `/zno-fix`: reproduce or reason about the defect, keep the docs update lightweight, and update the changelog after the fix if behavior changes.
- `/zno-tech`: update `docs/engineering/04-tech-decisions.md` before or alongside any implementation.
- `/zno-deploy`: update `docs/operations/08-deployment.md`, and update `docs/operations/07-local-development.md` if local commands or env vars change.
- `/zno-handoff`: update `docs/handoff/05-handoff-guide.md`.
- `/zno-roadmap`: update `docs/product/06-roadmap.md`.
- `/zno-plan`: when the user has no clear next step or asks what to add/improve, read existing docs, recommend feature/optimization directions with value, complexity, priority, dependencies, and risks, then wait for the user to choose. Do not implement directly.
- `/zno-status`: inspect the current workspace, recent changes, docs, tests, and known pending work; update `docs/development/10-current-status.md` with a concise handoff-ready snapshot. Do not implement new work unless the user explicitly asks.
- `/zno-continue`: read `AI_DEVELOPMENT_RULES.md`, `docs/00_START_HERE.md`, `docs/development/10-current-status.md`, `docs/development/03-feature-changelog.md`, `docs/product/06-roadmap.md`, and `docs/handoff/05-handoff-guide.md`; summarize current state and continue only after identifying the next safe task.
- `/zno-upgrade`: if the user asks to update local skill `scripts/update_installed_skills.py` to download the latest GitHub package and update `~/.claude/skills`; otherwise copy only missing project template docs, preserve existing content, update `docs/maintenance/12-upgrade-history.md`, and then update `docs/development/10-current-status.md`.
- `/zno-review`: perform a self-review of recent changes or a specified scope/branch. Audit across 5 dimensions: security, performance, error handling, SOLID/DRY, and project conventions. Output findings as blocking items, suggestions, and reminders. Update `docs/development/03-feature-changelog.md` with review status.

If the user omits the skill name but starts with one of these prefixes, apply this skill.

## Core Workflow

For a new project:

1. Inspect the current workspace for existing docs and project files.
2. If the project lacks the required docs, run `scripts/init_project_docs.py <project-root>` to scaffold essential docs only (progressive mode). This creates only the core files needed for kickoff. Remaining docs (changelog, tech decisions, deployment, etc.) will be created on-demand when their corresponding commands are first triggered.
3. Read `AI_DEVELOPMENT_RULES.md` and `docs/00_START_HERE.md` after initialization.
4. Restate the user's project goal in plain language.
5. Ask only the clarification questions that affect product scope, architecture, data, permissions, deployment, frontend design direction, or acceptance.
6. If the project has any user interface, identify whether it is a website, mini program, browser extension, app, desktop app, internal tool, admin system, dashboard, or other surface; collect or recommend 2-5 UI style references; then extract overall mood, colors, layout, card/component style, interaction states, and things to avoid into `docs/product/15-frontend-design.md`. Also generate initial token values in `docs/product/15-frontend-design-tokens.json` based on the confirmed design direction.
7. After the user confirms, fill or update the docs under `docs/`.
8. Do not start implementation until the requirements and initial docs are confirmed.

For mid-project new requirements:

1. Do not ask the user to paste the kickoff prompt again.
2. Classify the request as new feature, change, bug fix, UX improvement, technical adjustment, or deployment change.
3. Restate the requirement briefly.
4. Ask clarification questions only if the request affects scope, business rules, data shape, permissions, technical decisions, deployment, or acceptance.
5. If any required doc file does not yet exist (e.g. `03-feature-changelog.md` on first feature), scaffold it from the template using `scripts/init_project_docs.py <project-root> --scaffold <trigger>` before writing content.
6. If the project has a test framework configured, follow Test-First (TDD): write a failing test for the new behavior, implement minimally to pass, then refactor under green tests. Skip TDD for pure UI tweaks, docs, or config changes.
7. Update the relevant docs before or alongside code changes.
8. Always update `docs/development/03-feature-changelog.md` after a feature, change, deletion, or fix.
9. Update `docs/product/15-frontend-design.md` and `docs/product/15-frontend-design-tokens.json` when the request affects product surface, UI style, layout, component strategy, interaction states, or frontend experience boundaries.
10. Before marking the task complete, satisfy the Verification Gate: provide at least 2 of (test pass output, build success, type check pass, API response sample, manual test steps). If unable, explain why and state remaining risks.
11. Final response must include page-level manual test steps when the change affects user-visible UI or browser workflows.

For technical choices:

1. If work involves core frameworks, databases, cache, queues, auth, storage, payment, email/SMS/push, deployment, CI/CD, monitoring, logging, schedulers, heavy frontend libraries, or any dependency/service with meaningful performance/cost/security/maintenance impact, do not implement immediately.
2. Present 2-3 viable options with purpose, pros, cons, performance impact, cost, maintenance complexity, risks, and rollback.
3. Recommend one option and explain why.
4. Wait for user confirmation unless the user explicitly specified the technology and explicitly waived comparison.
5. After confirmation, record the decision in `docs/engineering/04-tech-decisions.md`, then implement.

For open-ended planning:

1. Trigger this flow when the user writes `/zno-plan` or says they have no idea what to add, asks what to do next, asks how to improve the project, or wants feature recommendations.
2. Read `docs/product/01-requirements-clarification.md`, `docs/development/03-feature-changelog.md`, `docs/product/06-roadmap.md`, `docs/development/10-current-status.md`, and `docs/engineering/11-project-structure.md`.
3. Identify the current project phase and whether the core user journey is complete.
4. Recommend 3-7 candidate directions across core workflow gaps, UX polish, admin/permissions/audit, performance, security, deployment/observability, data/reporting, and operations/commercialization when relevant.
5. For each candidate, include user value, priority, implementation complexity, dependencies, performance/security/deployment impact, and whether a technical-selection gate may be needed.
6. Recommend the top 1-2 next steps and ask the user to choose.
7. Do not implement until the user selects a direction.

For goal-mode automatic execution:

1. Trigger this flow when the user writes `/zno-goal`, asks to fully complete a project/phase, or says they do not want to keep issuing per-feature commands.
2. If the environment exposes a goal tool, create a goal with the user's objective. If not, treat the current conversation as goal-mode and state that the workflow will be followed manually.
3. If the project is not initialized, run the `/zno-init` workflow first: clarify only essential product/technical uncertainties, scaffold docs, and wait for required confirmations.
4. If the project is already initialized, run the `/zno-continue` workflow first: read project rules, current status, roadmap, changelog, handoff, project structure, command reference, and technical decisions.
5. Break the goal into phases and immediate tasks, then keep progressing without requiring the user to type `/zno-feature`, `/zno-status`, or `/zno-continue`.
6. Apply the same gates internally: use `/zno-plan` behavior when the next step is unclear, `/zno-tech` behavior for major technical selections, `/zno-feature` or `/zno-change` behavior for implementation tasks, `/zno-fix` behavior for defects, and `/zno-deploy` behavior for deployment work.
7. Update relevant docs after each meaningful unit of work, especially `docs/development/03-feature-changelog.md`, `docs/product/06-roadmap.md`, `docs/development/10-current-status.md`, and `docs/engineering/11-project-structure.md`.
8. Stop and ask the user only for required decisions: product boundary ambiguity, major technology selection, paid/external services, production deployment, security/permission/data deletion/compliance risk, or an actual blocker.
9. Low-risk implementation details may be decided autonomously and recorded in the relevant docs.
10. When the goal is genuinely achieved, mark the Goal complete if the environment provides a goal status tool; otherwise summarize completion and remaining risks.

For super high-autonomy execution:

1. Trigger this flow when the user writes `/zno-goal --super`, uses `/zno-super`, or explicitly says to proceed without asking ordinary confirmation questions.
2. Enter `/zno-goal` behavior, but treat ordinary technical/product choices as AI-owned decisions.
3. For major choices, still compare options internally, select the best fit, implement it, and record the decision in `docs/development/14-decision-log.md`.
4. Continue without waiting for user confirmation unless the decision involves paid services, production data deletion, secrets, destructive git operations, or clear security/compliance risk.
5. Final responses must summarize the important decisions made, why they were made, risks, rollback options, validation, and page manual test steps when UI is affected.

For code review:

1. Trigger this flow when the user writes `/zno-review`, asks to review code, or a feature branch is ready to merge.
2. Identify the scope: recent uncommitted changes, a specific branch diff, or files the user specifies.
3. Audit across 5 dimensions:
   - Security: SQL injection, XSS, auth bypass, credential leaks, insecure deserialization.
   - Performance: N+1 queries, missing pagination, redundant requests, oversized bundles, missing indexes.
   - Error handling: swallowed errors, empty catch blocks, unhandled promise rejections, missing user feedback.
   - SOLID/DRY: duplicated logic, oversized functions, deep coupling, violation of single responsibility.
   - Project conventions: naming, directory placement, existing patterns, consistency with design tokens.
4. Output findings in 3 tiers:
   - Blocking items (must fix before merge): prefix with a red indicator.
   - Suggestions (recommended, not blocking): prefix with a yellow indicator.
   - Reminders (optional improvements): prefix with a blue indicator.
5. If blocking items exist, propose fixes or explain the fix direction.
6. Update `docs/development/03-feature-changelog.md` with review status if the review leads to changes.
7. Do not merge or push; only report findings and optionally apply fixes if user confirms.

## Progressive Documentation Scaffold

This skill uses progressive (lazy) documentation generation:

- On `/zno-init`: only essential docs are created (requirements, roadmap, design, dev principles, README, rules).
- On first use of a related command: the corresponding doc is scaffolded from template automatically.
- Mapping: `/zno-feature` triggers `feature`, `/zno-tech` triggers `tech`, `/zno-deploy` triggers `deploy`, `/zno-status` triggers `status`, `/zno-handoff` triggers `handoff`.
- To scaffold manually: `scripts/init_project_docs.py <project-root> --scaffold <trigger>`.
- To generate all docs at once (legacy): `scripts/init_project_docs.py <project-root> --full`.

When a command needs to update a doc that does not exist yet, scaffold it first, then write content.

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
- `docs/maintenance/09-zno-project-start-prompt.md`: optional first-message prompt for tools that do not automatically use skills.
- `docs/development/10-current-status.md`: current progress snapshot for cross-chat continuation and handoff.
- `docs/engineering/11-project-structure.md`: project directory map, module responsibilities, key files, data/request flow, and file placement rules.
- `docs/maintenance/12-upgrade-history.md`: Skill/template upgrade history and migration notes for previously initialized projects.
- `docs/maintenance/13-command-reference.md`: command list, use cases, effects, and docs each command updates.
- `docs/development/14-decision-log.md`: key decision log, especially for `/zno-super` mode where AI proceeds without ordinary confirmations.
- `docs/product/15-frontend-design.md`: product surface, UI references, design keywords, color, layout, card/component style, interaction states, and frontend pitfalls to avoid.

## Initialization Script

Use the script when a workspace needs the docs scaffold:

```powershell
python <installed-skills-dir>/zno-init/scripts/init_project_docs.py <project-root>
```

Behavior:

- Creates `AI_DEVELOPMENT_RULES.md` and `docs/` templates.
- Skips files that already exist.
- Use `--overwrite` only if the user explicitly asks to replace existing docs.

Use the local skills updater when the user asks to update this skill package, update local commands, pull the latest GitHub package, or refresh `~/.claude/skills`:

```powershell
python <installed-skills-dir>/zno-upgrade/scripts/update_installed_skills.py
```

Behavior:

- Downloads `https://github.com/1447751897/ai-project-command-skills` as a zip archive.
- Validates that all expected skill folders are present.
- Backs up existing installed skills under `~/.claude/skills/.backup/`.
- Replaces the installed skill folders and tells the user to restart Claude Code.

Use the project docs upgrade script when a project was initialized by an older skill version and the user asks to add missing project docs or template rules:

```powershell
python <installed-skills-dir>/zno-upgrade/scripts/upgrade_project_docs.py <project-root>
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

When handling `/zno-status`:

1. Inspect relevant docs and, if available, git status/recent changed files.
2. Record the current phase, current task, completed work, in-progress work, pending next steps, blockers, recent file changes, verification run, verification not run, and continuation advice in `docs/development/10-current-status.md`.
3. Keep the snapshot factual. Do not claim tests ran unless they actually ran.
4. Final response should tell the user that the status snapshot was updated and what the next recommended step is.

When handling `/zno-continue`:

1. Read the current status doc first.
2. Read the minimum supporting docs needed to avoid guessing: usually `00_START_HERE`, `03-feature-changelog`, `06-roadmap`, `05-handoff-guide`, and `13-command-reference`.
3. Read `AI_DEVELOPMENT_RULES.md` and `docs/engineering/04-tech-decisions.md` before making implementation or technology choices.
4. Inspect the workspace for current files and uncommitted changes before editing.
5. Briefly summarize where the project left off.
6. Continue with the next task only if it is clear; otherwise ask the smallest necessary clarification question.
7. If the next task requires a new technical choice, use the Technical Selection Gate before implementation.

When handling `/zno-upgrade`:

1. Classify the request first.
2. If the user asks to update local skills, commands, this skill package, or the latest GitHub version, run `scripts/update_installed_skills.py`. Use `--dry-run` first when the user asks to preview only.
3. If the user asks to upgrade an initialized project, run `scripts/upgrade_project_docs.py <project-root>` or manually apply the same behavior.
4. For project docs upgrades, never overwrite existing project docs; read the list of new files, summarize what was added, propose/apply additive merges for new rules, and update `docs/development/10-current-status.md`.
5. For local skill package updates, summarize the downloaded repository/branch, target install path, backup path if created, installed commands, and tell the user to restart Claude Code.

When handling `/zno-goal`:

1. Create or enter a long-running objective if Goal tooling is available.
2. Do not wait for the user to issue the next command after every task.
3. Keep applying this skill's docs, gates, and update rules automatically.
4. Keep the user informed at meaningful checkpoints, especially before any required confirmation gate.
5. Use `/zno-status` behavior automatically at phase boundaries, before stopping, and after meaningful progress.

When handling `/zno-goal --super` or `/zno-super`:

1. Create or enter a long-running objective if Goal tooling is available.
2. Apply `/zno-goal` behavior without stopping for ordinary confirmations.
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
