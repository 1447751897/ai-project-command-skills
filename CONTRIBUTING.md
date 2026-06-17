# Contributing

Thanks for improving AI Project Command Skills.

## Development Notes

- Keep command behavior documented in the skill instructions and in `docs/13-command-reference.md` inside the bundled project template.
- If you add a new project document template, update:
  - `docs/00_START_HERE.md`
  - `docs/README.md`
  - `docs/09-ai-project-start-prompt.md`
  - `docs/12-upgrade-history.md` expectations if needed
- If you change technical decision behavior, update `docs/04-tech-decisions.md` and `docs/14-decision-log.md` if relevant.
- If you change installable command names, update both `install.ps1` and `install.sh`.
- Keep `/super` as a compatibility alias for `/goal --super`.

## Validation

Before publishing a change:

1. Install locally with the platform installer.
2. Restart Codex desktop.
3. Confirm the command menu can find the changed command.
4. Test at least:

```text
/init Test project
/goal Test objective
/goal --super Test objective
/upgrade
/status
/continue
```

## Pull Requests

Please include:

- What command or document behavior changed.
- Which bundled templates were updated.
- How you validated the change.

