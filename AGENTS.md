# AGENTS.md: gvs-skills

Instructions for coding agents and humans working in this repo. Read this file first, then the build spec you were given.

## What this is

A catalog of draft-only AI skills: packaged instructions, templates, invented examples, and checks. Gold Valley Solutions publishes the catalog. Skills are plain Markdown. They do not send, post, or call paid APIs. The first skill is `content-drafting-agent`.

This repo is public. Do not change visibility. Do not enable GitHub Pages. Every push must pass the secret scan and the spec's scrub (no private client or machine text).

## Setup (fresh checkout)

```bash
python3.11 -m venv .venv && . .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

Python 3.11, pytest, PyYAML, and the official `skills-ref` validator. Do not add other packages without a spec.

## Validation commands (these match `.github/workflows/ci.yml`; run them before every commit you hand over)

```bash
python scripts/validate_skills.py
agentskills validate skills/content-drafting-agent   # PyPI CLI for skills-ref; some docs say `skills-ref validate`
pytest -q
gitleaks detect --source . --no-banner
```

Then run the spec's scrub grep (AC-20). It must print no matches (`rc=1`). Remove local `__pycache__` first so bytecode paths are not false hits.

- Tests must not call the network or any paid service.
- `scripts/validate_skills.py` must exit 0. On failure it prints a clear message and exits non-zero.
- Small commits with one-line messages; stage explicit paths (never `git add -A`); leave `git status --porcelain` clean.

## Conventions

- One folder per skill under `skills/<name>/`. The folder name matches the `name` in `SKILL.md` front matter (Agent Skills spec).
- Required file: `SKILL.md`. Conventional optional dirs: `scripts/`, `references/`, `assets/`. See `docs/skill-format.md` and https://agentskills.io/specification.
- Examples are invented and clearly fake. No client data, no private Gold Valley content, no real people, companies, or numbers.
- Safety level for every listing is draft-only until a later spec says otherwise.

## How we build (software factory rules)

1. **Spec first.** Build only what the spec's requirements and acceptance criteria (ACs) ask for. Respect "Out of scope". The smallest change that fully meets the spec wins; no extra options, hidden defaults or fallbacks the spec didn't ask for.
2. **Build report rule.** The PR description starts with the build report from `.github/pull_request_template.md`. Its first line is exactly `STATUS: READY` or `STATUS: BLOCKED`. For every AC in the spec, give the command you ran, its real output, and PASS / FAIL / NOT RUN. "Tests pass" without output is not evidence. If you can't meet the spec (it contradicts itself, it needs a decision only Mike can make, or the environment fails), write `STATUS: BLOCKED` and explain under `## Blocked`. Never paper over a failure.
3. **Reviews.** Each round is reviewed through four lenses (Security, Code, Tests and evals, UX), each ending in `VERDICT: PASS` or `VERDICT: CHANGES`. Address every CHANGES finding, or say in the build report's Log why you didn't. Notes are optional.
4. **Max 3 rounds.** Round 1 plus at most 2 rework rounds. If findings are still open after round 3, stop and hand over to Mike with the open findings; don't keep looping.
5. **No auto-merge.** Never merge, rebase onto `main`, force-push, enable auto-merge, change branch protection or push to `main`. Mike reviews and merges every PR himself. Open the PR as a draft and stop.

## Always to a human (Mike): flag these in the build report

Any change that touches one of these must be listed under "Always-to-human flags" with the file and the reason. Some need Mike's OK **before** you do them (marked ⛔); don't do those without it in the spec.

- License text or a license change
- ⛔ Public exposure: changing visibility, enabling GitHub Pages, tunnels, binding to `0.0.0.0`
- `.github/workflows/` or other CI/runtime config
- New dependency: Python package, Action, or external tool
- Public copy: README index, skill descriptions, anything a stranger would read as Gold Valley
- ⛔ Money: paid services, API keys, anything that could bill
- Auth, secrets handling, or a secret scan bypass
- Product decisions: what is free vs paid, adding a skill, changing draft-only

## Never

- Commit secrets, keys, tokens, `.env`, or real personal data.
- Copy private Gold Valley content (voice guides, client files, internal notes) into this repo.
- Use paid APIs or add packages beyond pytest, PyYAML, and skills-ref.
- Change this repo's visibility or enable GitHub Pages.
- Enable auto-merge, merge a PR, or push extra commits to `main`.
- Invent clients, quotes, or numbers in examples. Mark every example as fictional.
