# Skill format

Skills in this repo follow the [Agent Skills specification](https://agentskills.io/specification). One folder per skill under `skills/<name>/` at the repo root. That catalog layout is what the [skills CLI](https://github.com/vercel-labs/skills) discovers (`npx skills add mike-gvs/gvs-skills --skill <name>`). The spec does not define a repo-level registry file; this catalog still lists every skill in the root `README.md` table and in Claude Code's `.claude-plugin/marketplace.json`. Required file: `SKILL.md`. Optional conventional directories: `scripts/`, `references/`, `assets/`. Extra files (for example a human `README.md`) are allowed.

## Layout

```
skills/
└── skill-name/
    ├── SKILL.md          # Required: metadata + instructions
    ├── scripts/          # Optional: executable code
    ├── references/       # Optional: documentation (this catalog: checks.md)
    ├── assets/           # Optional: templates and example resources
    └── README.md         # Optional: how a human installs and uses the skill
```

| Path | Purpose |
|---|---|
| `SKILL.md` | YAML front matter plus step-by-step instructions |
| `assets/` | Templates and static examples (voice guide, invented input/output) |
| `references/` | On-demand docs (AI-tells check, ask-the-owner list) |
| `scripts/` | Executable code (none in skill #1) |

File references from `SKILL.md` are one level deep (`assets/…`, `references/…`).

## `SKILL.md` front matter

Required by the spec:

| Key | Rule |
|---|---|
| `name` | 1–64 characters; lowercase `a-z`, `0-9`, hyphens; no leading/trailing hyphen; no `--`; must match the folder name |
| `description` | 1–1024 characters; what the skill does and when to use it |

Allowed optional fields:

| Key | Rule |
|---|---|
| `license` | License name or bundled license file. This catalog uses `MIT`. |
| `compatibility` | 1–500 characters; omit unless the skill has environment requirements |
| `metadata` | Map of string keys to string values (this catalog puts `version` and `safety` here) |
| `allowed-tools` | Space-separated string of pre-approved tools (experimental). Omit for chat-only draft skills. |

Do not put `version` or `tools` at the top level. Those are not spec fields. Put extra keys under `metadata`.

Example:

```yaml
---
name: example-skill
description: What it drafts and when to use it.
license: MIT
metadata:
  version: "1.0.0"
  safety: draft-only
---
```

## Safety rules for every listing

- Draft-only by default (nothing sends or publishes).
- No secrets or keys.
- No client or personal data.
- A secret scan and the spec's scrub before every push.
- `python scripts/validate_skills.py` and `agentskills validate <skill-dir>` (skills-ref) both exit 0.
- PM review against the checklist in [CONTRIBUTING.md](../CONTRIBUTING.md).
