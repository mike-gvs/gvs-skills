# Contributing

This catalog lists draft-only skills. Mike reviews every listing. Open a draft PR; do not merge and do not make the repo public.

## Listing checklist

A skill may be listed only when every item is true:

- **Draft-only.** The skill never sends, posts, mails, schedules, or calls an API. Instructions say so in `SKILL.md`.
- **No secrets or keys.** No API keys, tokens, passwords, or `.env` files in the skill or its examples.
- **No client or personal data.** No real customers, inboxes, phone numbers, or private notes.
- **Invented examples only.** Input and output samples are clearly fictional. Do not copy a real voice guide.
- **Secret scan passes.** `gitleaks detect --source . --no-banner` exits 0 on the full history.
- **Front matter valid.** `python scripts/validate_skills.py` exits 0. `SKILL.md` has parseable YAML with `name`, `description`, `version`, `license: MIT`, and `tools`. `name` matches the folder and is kebab-case. `version` is semver.
- **PM review.** A human checks this list, the AI-tells check, and the "ask the owner" list before merge.

## Adding a skill

1. Create `skills/<kebab-name>/` with `SKILL.md`, `README.md`, `checks.md`, plus `templates/` and `examples/` as needed. See [docs/skill-format.md](docs/skill-format.md).
2. Put usage steps in the skill `README.md` for Claude, ChatGPT, Cursor, and paste.
3. Add a row to the index table in the root `README.md` (name, what it does, tools, safety level **draft-only**).
4. Run the validation commands in [AGENTS.md](AGENTS.md).
5. Open a **draft** pull request using `.github/pull_request_template.md`.

## Out of scope here

GitHub Pages, making the repo public, paid listings, third-party submissions, and extra Python packages. Those need a new spec and Mike's OK.
