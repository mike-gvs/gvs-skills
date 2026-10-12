# gvs-skills

A catalog of **draft-only** [Agent Skills](https://agentskills.io/specification): packaged `SKILL.md` folders an assistant can follow. Each skill drafts work for a human to review. Nothing here sends, posts, or calls a paid API.

Maintained by Gold Valley Solutions. License: [MIT](LICENSE). This repo is public. Every push must pass the secret scan and the spec's scrub.

## Skills

| Name | What it does | Tools | Safety |
|---|---|---|---|
| [content-drafting-agent](skills/content-drafting-agent/) | Turns a filled voice guide plus rough notes into 1 blog post, 2 LinkedIn posts, and 1 newsletter blurb | none (chat-only; no `allowed-tools`) | draft-only |

## Install

### Claude Code marketplace (confirmed)

This repo includes `.claude-plugin/marketplace.json` so Claude Code can add it as a marketplace, list the plugin, and install the skill ([anthropics/skills](https://github.com/anthropics/skills), [Claude Code plugins](https://code.claude.com/docs/en/plugins/marketplace-reference)):

```text
/plugin marketplace add mike-gvs/gvs-skills
/plugin install content-drafting-agent@gvs-skills
```

### ChatGPT

No marketplace in this repo for ChatGPT. ChatGPT/Codex do not read `.claude-plugin/marketplace.json`. Copy the skill folder to `.agents/skills/` for Codex, use `$skill-installer` for local Codex installs from GitHub, or paste `SKILL.md` into a custom GPT. This catalog is not listed in the ChatGPT Plugins Directory. See the skill README.

### GitHub Copilot

No Copilot marketplace manifest in this repo. Copy the skill into `.github/skills/`, `.claude/skills/`, or `.agents/skills/`, or (`gh` 2.90+):

```text
gh skill preview mike-gvs/gvs-skills content-drafting-agent
gh skill install mike-gvs/gvs-skills content-drafting-agent
```

See [Adding agent skills for GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills).

## How to use a skill

1. Open the skill folder. Read its `README.md`.
2. Fill in any templates under `assets/` (for example the voice guide). Use your own words.
3. Give the assistant `SKILL.md`, your filled template, your notes, and `references/checks.md`.
4. Take the drafts. Edit them. Publish only if you choose to, outside the skill.

## Format and contributing

- Open spec: [agentskills.io/specification](https://agentskills.io/specification)
- This catalog's notes: [docs/skill-format.md](docs/skill-format.md)
- Listing checklist: [CONTRIBUTING.md](CONTRIBUTING.md)
- Agent instructions: [AGENTS.md](AGENTS.md)

Validate:

```bash
python scripts/validate_skills.py
agentskills validate skills/content-drafting-agent
pytest -q
gitleaks detect --source . --no-banner
```
