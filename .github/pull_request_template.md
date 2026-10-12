STATUS: READY

<!-- First line must be exactly `STATUS: READY` or `STATUS: BLOCKED`. See AGENTS.md › "How we build". Rewrite this report at the end of every round; keep the Log. -->

# Build report: <spec title>

**Spec:** <path or link> · **Spec items:** <e.g. AC-1–AC-22> · **Base:** <branch @ sha> · **Head:** <sha> · **Round:** <1 | 2 | 3>

## Summary
<What this PR does, in a few lines.>

Files changed:
- `<path>`: <why>

## Acceptance criteria
<!-- One block per AC in the spec, same IDs and order. Real command, real output (trimmed), result. -->

### AC-<id> · <criterion>
- **Command:** `<command>`
- **Output:**
  ```
  <output>
  ```
- **Result:** PASS | FAIL | NOT RUN (<reason>)

## Validation (CI commands from AGENTS.md)
| Command | Result |
|---|---|
| `python scripts/validate_skills.py` | |
| `agentskills validate skills/content-drafting-agent` | |
| `pytest -q` | |
| `gitleaks detect --source . --no-banner` | |

## Always-to-human flags
<!-- Every item from the AGENTS.md list this PR touches, with file and reason. Write "None" only if truly none. -->
-

## Assumptions
<!-- Decisions the spec didn't settle. Mark [product decision → Mike] where it applies. -->
-

## Log
### Round 1
-

---
- [ ] Every AC above has a command and its output
- [ ] CI is green on the head commit
- [ ] No `.env`, secrets or real personal data committed
- [ ] Default config makes no paid or outbound provider calls
- [ ] I did not merge, enable auto-merge or push to `main` (Mike merges)
