# Contributing

This catalog lists draft-only skills. The repo is public. Mike reviews every listing. Open a draft PR; do not merge, do not change visibility, and do not enable Pages. Every push must pass the secret scan and the spec's scrub.

## Listing checklist

A skill may be listed only when every item is true:

- **Draft-only.** The skill never sends, posts, mails, schedules, or calls an API. Instructions say so in `SKILL.md`.
- **No secrets or keys.** No API keys, tokens, passwords, or `.env` files in the skill or its examples.
- **No client or personal data.** No real customers, inboxes, phone numbers, or private notes.
- **Invented examples only.** Input and output samples are clearly fictional. Do not copy a real voice guide.
- **Secret scan passes.** `gitleaks detect --source . --no-banner` exits 0 on the full history.
- **Scrub passes.** The spec's scrub grep finds no private client or machine text.
- **Front matter valid.** `python scripts/validate_skills.py` and `agentskills validate skills/<name>` (skills-ref) exit 0. `SKILL.md` has parseable YAML with required `name` and `description`. Optional spec fields only: `license`, `compatibility`, `metadata`, `allowed-tools`. Catalog extras such as `version` go under `metadata`. `name` matches the folder.
- **PM review.** A human checks this list, the AI-tells check, and the "ask the owner" list before merge.

## Adding a skill

1. Create `skills/<kebab-name>/` with `SKILL.md`, plus `references/` and `assets/` as needed. See [docs/skill-format.md](docs/skill-format.md). If it is listed for Claude Code, add it to `.claude-plugin/marketplace.json`.
2. Put usage steps in the skill `README.md` for Claude, ChatGPT, Cursor, and paste.
3. Add a row to the registry table in the root `README.md` (name linked to the folder, one-line description, `npx skills add mike-gvs/gvs-skills --skill <name>`, safety level **draft-only**). Add the same skill to `.claude-plugin/marketplace.json`. `pytest` fails if those lists drift from `skills/`.
4. Run the validation commands in [AGENTS.md](AGENTS.md).
5. Open a **draft** pull request using `.github/pull_request_template.md`.

## Out of scope here

GitHub Pages (stay off), changing visibility, paid listings, third-party submissions, and extra Python packages other than pytest, PyYAML, and skills-ref. Those need a new spec and Mike's OK.
