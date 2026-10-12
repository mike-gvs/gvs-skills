# Content drafting agent

Turn a filled voice guide plus rough notes into one blog post, two LinkedIn posts, and a newsletter blurb. Safety level: **draft-only**. The skill never sends or publishes.

This folder is an [Agent Skill](https://agentskills.io/specification): `SKILL.md` plus optional `references/` and `assets/`. No extra tools or API keys.

## Before you start

1. Copy `assets/voice-guide-template.md` and fill in every bracket with your own words. Do not paste a private voice guide from someone else.
2. Gather rough notes (facts only). Look at `assets/input-notes.md` for the shape. All names and numbers in the example are invented.
3. Keep `references/checks.md` handy. The assistant must run it on every draft.

## Claude

Confirmed from [Claude Code skills](https://code.claude.com/docs/en/skills) and [anthropics/skills](https://github.com/anthropics/skills):

**Marketplace (Claude Code):** this repo ships `.claude-plugin/marketplace.json`. In Claude Code:

```text
/plugin marketplace add mike-gvs/gvs-skills
```

Then browse plugins, select `gvs-skills`, install `content-drafting-agent`, or:

```text
/plugin install content-drafting-agent@gvs-skills
```

**Project skill:** copy this folder to `.claude/skills/content-drafting-agent/` in a repo (Claude Code loads project skills from `.claude/skills/`).

**Claude.ai / Projects:** add the folder as an Agent Skill, or paste `SKILL.md`, `references/checks.md`, and your filled voice guide into a Project. There is no Claude.ai marketplace for this GitHub repo.

After it loads, give it your filled voice guide and notes. Ask it to draft the four pieces, run `references/checks.md`, list ask-the-owner questions, and not publish.

## ChatGPT

Confirmed from [Build skills (ChatGPT / Codex)](https://learn.chatgpt.com/docs/build-skills):

**No Claude-style marketplace here.** ChatGPT and Codex do not read `.claude-plugin/marketplace.json`. Their plugin catalog is a separate system (OpenAI plugins / `.agents/plugins/marketplace.json`). This repo is not published to the ChatGPT Plugins Directory.

**Codex / ChatGPT desktop local skills:** copy this folder to `.agents/skills/content-drafting-agent/` in the repo, or to `$HOME/.agents/skills/content-drafting-agent`. Codex scans `.agents/skills`. The built-in `$skill-installer` can also pull skills from other GitHub repos for local Codex use.

**ChatGPT custom GPT / Project instructions:** paste `SKILL.md` into the instructions. Upload `references/checks.md` and your filled voice guide (or paste them). Do not enable actions that send email, post, or call an API.

## GitHub Copilot

Confirmed from [About agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) and [Adding agent skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills):

**No Copilot marketplace.json in this repo.** Copilot does not use `.claude-plugin/marketplace.json`.

**Project skill:** copy this folder to `.github/skills/content-drafting-agent/`, `.claude/skills/content-drafting-agent/`, or `.agents/skills/content-drafting-agent/` in the repo you want Copilot to use it in.

**Personal skill:** copy it to `~/.copilot/skills/content-drafting-agent` or `~/.agents/skills/content-drafting-agent`.

**GitHub CLI** (`gh` 2.90.0+, `gh skill` is public preview):

```text
gh skill preview mike-gvs/gvs-skills content-drafting-agent
gh skill install mike-gvs/gvs-skills content-drafting-agent
```

Inspect the skill before installing. Copilot loads it when the task matches the description, or you can invoke it with `/content-drafting-agent`.

## Cursor and any chat (paste)

Cursor has no skills marketplace for this catalog. Copy `SKILL.md` into a project rule, or paste `SKILL.md`, the filled voice guide, notes, and `references/checks.md` into the chat. Say: run these checks, ask the owner anything you cannot confirm, never send or publish.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Spec front matter plus instructions |
| `assets/voice-guide-template.md` | Blank voice guide you fill in |
| `assets/input-notes.md` | Invented sample notes |
| `assets/output-draft.md` | Invented sample drafts that pass the checks |
| `references/checks.md` | AI-tells check and ask-the-owner list |
