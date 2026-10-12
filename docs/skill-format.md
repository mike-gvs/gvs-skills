# Skill format

One folder per skill, plain files, no code required. Folders already work as-is in tools that support Agent Skills (for example Claude). For other tools the skill `README.md` gives a copy-paste path, so a skill is not tied to one vendor.

## Layout

| File | Purpose |
|---|---|
| `SKILL.md` | Front matter (name, one-line description, version, license, tools needed) plus step-by-step instructions the assistant follows |
| `templates/` | Fill-in-the-blank files the user completes (for example a generic `voice-guide-template.md`). Never a private voice guide. |
| `examples/` | One input and output pair with invented, clearly fake content |
| `checks.md` | The "AI tells" check (no em dashes, no stock phrases, no invented clients or numbers) and the "ask the owner" list |
| `README.md` | How to use it in Claude (skills/projects), ChatGPT (custom GPT or project instructions), Cursor (rules), or any chat by pasting it |

## `SKILL.md` front matter

YAML between `---` lines at the top of the file. Required keys:

| Key | Rule |
|---|---|
| `name` | kebab-case; must match the folder name |
| `description` | one line, at most 200 characters |
| `version` | semver `MAJOR.MINOR.PATCH` (for example `1.0.0`) |
| `license` | `MIT` |
| `tools` | YAML list. Use `[none]` when the skill is chat-only. |

Example:

```yaml
---
name: example-skill
description: One line on what the skill drafts.
version: 1.0.0
license: MIT
tools: [none]
---
```

The body after the front matter is the step-by-step instructions.

## Safety rules for every listing

- Draft-only by default (nothing sends or publishes).
- No secrets or keys.
- No client or personal data.
- A secret scan before every push.
- PM review against the checklist in [CONTRIBUTING.md](../CONTRIBUTING.md).

`scripts/validate_skills.py` checks front matter and required files. CI runs that script, `pytest -q`, and gitleaks.
