"""AI-tells and packaging checks for the content-drafting-agent example."""

from __future__ import annotations

import re
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1] / "skills" / "content-drafting-agent"
OUTPUT = SKILL_DIR / "examples" / "output-draft.md"
CHECKS = SKILL_DIR / "checks.md"
SKILL_MD = SKILL_DIR / "SKILL.md"


def _banned_phrases() -> list[str]:
    text = CHECKS.read_text(encoding="utf-8")
    phrases: list[str] = []
    in_section = False
    for line in text.splitlines():
        if re.search(r"stock phrase", line, re.I):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section:
            stripped = line.strip()
            if stripped.startswith("- "):
                phrases.append(stripped[2:].strip().strip("`").lower())
    assert phrases, "checks.md must list banned stock phrases"
    return phrases


def test_example_output_has_no_em_dashes() -> None:
    text = OUTPUT.read_text(encoding="utf-8")
    assert "\u2014" not in text
    assert "—" not in text


def test_example_output_has_no_banned_stock_phrases() -> None:
    text = OUTPUT.read_text(encoding="utf-8").lower()
    found = [p for p in _banned_phrases() if p and p in text]
    assert found == [], f"banned stock phrases in example output: {found}"


def test_example_output_covers_the_four_drafts() -> None:
    text = OUTPUT.read_text(encoding="utf-8").lower()
    assert "blog" in text
    assert "linkedin" in text
    assert "newsletter" in text


def test_example_output_does_not_invent_clients_or_numbers() -> None:
    text = OUTPUT.read_text(encoding="utf-8")
    # Dollar amounts, percents, and quoted testimonials are invented claims.
    assert "$" not in text
    assert "%" not in text
    assert not re.search(r"\d{1,3}%", text)


def test_checks_md_has_ai_tells_and_ask_the_owner() -> None:
    text = CHECKS.read_text(encoding="utf-8").lower()
    assert "em dash" in text
    assert "stock phrase" in text
    assert "invent" in text
    assert "ask the owner" in text


def test_skill_md_is_draft_only() -> None:
    text = SKILL_MD.read_text(encoding="utf-8").lower()
    assert "never send" in text or "never publish" in text
    assert "ask the owner" in text
    assert "checks.md" in text
