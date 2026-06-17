# Security Policy

[简体中文](SECURITY.zh-CN.md) | English

## Reporting

If you find a security issue in the skill templates or installer scripts, open a GitHub issue with a clear description and reproduction steps.

Do not include real secrets, access tokens, production credentials, private keys, or sensitive project data in issue text.

## Scope

This repository contains local Codex skill folders and install scripts. The skills are instructions and templates; they do not provide a hosted service.

Important safety boundaries in the bundled workflow:

- Do not hardcode secrets.
- Do not commit real tokens.
- Do not perform destructive Git operations unless explicitly requested.
- `/goal --super` still stops for paid services, production data deletion, secrets, destructive Git operations, and clear security/compliance risks.
