# gvs-skills

A catalog of **draft-only** [Agent Skills](https://agentskills.io/specification): packaged `SKILL.md` folders an assistant can follow. Each skill drafts work for a human to review. Nothing here sends, posts, or calls a paid API.

Maintained by Gold Valley Solutions. License: [MIT](LICENSE). This repo is public. Every push must pass the secret scan and the spec's scrub.

## Skills

| Name | What it does | Tools | Safety |
|---|---|---|---|
| [content-drafting-agent](skills/content-drafting-agent/) | Turns a filled voice guide plus rough notes into 1 blog post, 2 LinkedIn posts, and 1 newsletter blurb | none (chat-only; no `allowed-tools`) | draft-only |

## Install

### CLI (`npx skills`)

The [skills CLI](https://github.com/vercel-labs/skills) (`npx skills`, [skills.sh](https://skills.sh)) discovers `skills/<name>/SKILL.md` in this catalog and copies the skill into `.agents/skills/`, which Cursor and other surfaces the CLI supports then load:

```bash
npx skills add mike-gvs/gvs-skills --skill content-drafting-agent
```

List skills in the catalog without installing:

```bash
npx skills add mike-gvs/gvs-skills --list
```

List skills already installed in the current project:

```bash
npx skills list
```

From a non-default git ref or a local clone:

```bash
npx skills add mike-gvs/gvs-skills#<branch> --skill content-drafting-agent
npx skills add ./ --skill content-drafting-agent
```

Until this catalog is on the repo default branch, use the `#<branch>` or local-path form. `npx skills add mike-gvs/gvs-skills` clones the default branch.

### Claude Code marketplace (confirmed)

This repo includes `.claude-plugin/marketplace.json` so Claude Code can add it as a marketplace, list the plugin, and install the skill ([anthropics/skills](https://github.com/anthropics/skills), [Claude Code plugins](https://code.claude.com/docs/en/plugins/marketplace-reference)):

```text
/plugin marketplace add mike-gvs/gvs-skills
/plugin install content-drafting-agent@gvs-skills
```

### ChatGPT

No marketplace in this repo for ChatGPT. ChatGPT/Codex do not read `.claude-plugin/marketplace.json`. `npx skills add` (above) copies the skill into `.agents/skills/`, which Codex scans. Or copy the folder there yourself, use `$skill-installer` for local Codex installs from GitHub, or paste `SKILL.md` into a custom GPT. This catalog is not listed in the ChatGPT Plugins Directory. See the skill README.

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
