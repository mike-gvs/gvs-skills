# Content drafting agent

Turn a filled voice guide plus rough notes into one blog post, two LinkedIn posts, and a newsletter blurb. Safety level: **draft-only**. The skill never sends or publishes.

You need no extra tools or API keys. Use it in Claude, ChatGPT, Cursor, or any chat by pasting the files.

## Before you start

1. Copy `templates/voice-guide-template.md` and fill in every bracket with your own words. Do not paste a private voice guide from someone else.
2. Gather rough notes (facts only). Look at `examples/input-notes.md` for the shape. All names and numbers in the example are invented.
3. Keep `checks.md` handy. The assistant must run it on every draft.

## Claude (Agent Skills / Projects)

1. Add this folder as a skill (Claude Agent Skills) or drop `SKILL.md` plus `checks.md` and the filled voice guide into a Project.
2. In a new chat, attach your filled voice guide and your notes.
3. Ask: "Follow the content-drafting-agent skill. Draft the four pieces. Run checks.md. List ask-the-owner questions. Do not publish."
4. Review the drafts yourself. Publish only if you choose to, outside this skill.

## ChatGPT (custom GPT or project instructions)

1. Create a custom GPT, or open a Project, and paste `SKILL.md` into the instructions.
2. Upload `checks.md` and your filled voice guide as project files (or paste them in the first message).
3. Paste your rough notes and ask for the four drafts.
4. Do not enable actions that send email, post, or call an API.

## Cursor (rules)

1. Copy `SKILL.md` into a project rule (for example `.cursor/rules/content-drafting-agent.mdc`) or point the agent at this folder.
2. Put your filled voice guide and notes in the repo or attach them in the chat.
3. Ask the agent to follow the skill, run `checks.md`, and stop after the drafts.
4. Do not ask it to commit secrets, change repo visibility, enable Pages, or publish the posts.

## Any chat (paste)

1. Paste `SKILL.md` into the chat.
2. Paste your filled voice guide and your notes.
3. Paste `checks.md` and say: "Run these checks. Ask the owner anything you cannot confirm. Never send or publish."
4. Copy the drafts out by hand when you are ready.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Instructions the assistant follows |
| `templates/voice-guide-template.md` | Blank voice guide you fill in |
| `examples/input-notes.md` | Invented sample notes |
| `examples/output-draft.md` | Invented sample drafts that pass the checks |
| `checks.md` | AI-tells check and ask-the-owner list |
