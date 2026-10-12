# gvs-skills

A catalog of **draft-only** AI skills: packaged instructions an assistant can follow in Claude, ChatGPT, Cursor, or any chat. Each skill drafts work for a human to review. Nothing here sends, posts, or calls a paid API.

Maintained by Gold Valley Solutions. License: [MIT](LICENSE). This repo stays private until the owner publishes it.

## Skills

| Name | What it does | Tools | Safety |
|---|---|---|---|
| [content-drafting-agent](skills/content-drafting-agent/) | Turns a filled voice guide plus rough notes into 1 blog post, 2 LinkedIn posts, and 1 newsletter blurb | none (chat-only) | draft-only |

## How to use a skill

1. Open the skill folder. Read its `README.md`.
2. Fill in any templates (for example the voice guide). Use your own words. Do not paste private files from someone else.
3. Give the assistant `SKILL.md`, your filled template, your notes, and `checks.md`.
4. Take the drafts. Edit them. Publish only if you choose to, outside the skill.

The same files work in tools that load Agent Skills (for example Claude) and in tools that do not. The skill README has copy-paste steps for Claude, ChatGPT, Cursor, and a plain paste path.

## Format and contributing

- Skill file layout: [docs/skill-format.md](docs/skill-format.md)
- Listing checklist: [CONTRIBUTING.md](CONTRIBUTING.md)
- Agent instructions: [AGENTS.md](AGENTS.md)

New listings need a valid `SKILL.md` front matter, invented examples only, a passing secret scan, and PM review. Safety stays **draft-only** unless a later spec says otherwise.
