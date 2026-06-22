# Contributing

[简体中文](CONTRIBUTING.zh-CN.md) | English

Thanks for improving AI Project Command Skills.

## Development Notes

- Keep command behavior documented in the skill instructions and in `docs/13-command-reference.md` inside the bundled project template.
- If you add a new project document template, update:
  - `docs/00_START_HERE.md`
  - `docs/README.md`
  - `docs/09-ai-project-start-prompt.md`
  - `docs/13-command-reference.md`
  - top-level `README.md` and `README.zh-CN.md`
  - `docs/12-upgrade-history.md` expectations if needed
- If you change technical decision behavior, update `docs/04-tech-decisions.md` and `docs/14-decision-log.md` if relevant.
- If you change installable Codex command names, update both `install.ps1` and `install.sh`.
- If you add or rename workflow skills, keep `skills/` and `claude-skills/` in sync. Claude Code aliases should keep the `ai-` prefix.
- If you change Claude Code command names, update both `install-claude.ps1` and `install-claude.sh`.
- If you change install targets or skill lists, update `install-all.ps1` and `install-all.sh` too.
- Keep `/super` as a compatibility alias for `/goal --super`.

## Validation

Before publishing a change:

1. Install locally with the platform installer.
2. Restart Codex desktop.
3. Confirm the command menu can find the changed command.
4. Test at least:

Auto installer:

```bash
./install-all.sh --tool all --dry-run
```

```powershell
powershell -ExecutionPolicy Bypass -File .\install-all.ps1 -Tool all -DryRun
```

Core commands:

```text
/init Test project
/goal Test objective
/goal --super Test objective
/upgrade
/status
/continue
```

For Claude Code compatibility, also validate the alias package with:

```text
/ai-init Test project
/ai-goal Test objective
/ai-goal --super Test objective
/ai-upgrade
/ai-status
/ai-continue
```

## Pull Requests

Please include:

- What command or document behavior changed.
- Which bundled templates were updated.
- Whether Codex skills and Claude Code alias skills were both updated when applicable.
- How you validated the change.
