"""README skills registry must stay in sync with skills/ folders.

The Agent Skills spec has no repo-level registry file. The npx skills CLI
discovers SKILL.md under skills/<name>/. This catalog still keeps a human
registry table in README.md (name, description, install command, folder
link) and Claude Code's .claude-plugin/marketplace.json. Both must list
exactly the skill folders that exist.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
INSTALL_PREFIX = "npx skills add mike-gvs/gvs-skills --skill "


def _skill_folders() -> list[str]:
    skills = ROOT / "skills"
    return sorted(p.parent.name for p in skills.glob("*/SKILL.md"))


def _readme_skills_section() -> str:
    text = README.read_text(encoding="utf-8")
    match = re.search(r"^## Skills\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    assert match, "README.md must have a ## Skills section"
    return match.group(1)


def _parse_registry_rows() -> list[dict[str, str]]:
    section = _readme_skills_section()
    lines = [ln.strip() for ln in section.splitlines() if ln.strip().startswith("|")]
    assert len(lines) >= 3, "README ## Skills must contain a markdown table"
    headers = [h.strip().lower() for h in lines[0].strip("|").split("|")]
    for required in ("name", "description", "install"):
        assert required in headers, f"README registry table missing column {required!r}"
    rows: list[dict[str, str]] = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        assert len(cells) == len(headers), f"ragged registry row: {line}"
        rows.append(dict(zip(headers, cells)))
    assert rows, "README registry table has no skill rows"
    return rows


def _name_and_folder_from_cell(cell: str) -> tuple[str, str]:
    match = re.fullmatch(r"\[([a-z0-9]+(?:-[a-z0-9]+)*)\]\(([^)]+)\)", cell)
    assert match, f"Name cell must be a markdown link to the skill folder: {cell!r}"
    name, href = match.group(1), match.group(2).rstrip("/")
    assert href == f"skills/{name}", f"folder link for {name} must be skills/{name}/, got {href}"
    return name, href


def test_readme_registry_matches_skill_folders() -> None:
    folders = _skill_folders()
    assert folders, "expected at least one skill under skills/"
    rows = _parse_registry_rows()
    names: list[str] = []
    for row in rows:
        name, _href = _name_and_folder_from_cell(row["name"])
        names.append(name)
        assert row["description"], f"{name} is missing a one-line description"
        expected = f"`{INSTALL_PREFIX}{name}`"
        assert expected in row["install"], (
            f"{name} install cell must contain {expected}, got {row['install']!r}"
        )
    assert sorted(names) == folders, (
        f"README registry names {sorted(names)} != skills/ folders {folders}"
    )


def test_marketplace_matches_skill_folders() -> None:
    folders = set(_skill_folders())
    data = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    listed: set[str] = set()
    for plugin in data.get("plugins", []):
        source = plugin.get("source", "./skills")
        for rel in plugin.get("skills", []):
            listed.add(Path(source, rel).name)
    assert listed == folders, (
        f"marketplace.json skills {sorted(listed)} != skills/ folders {sorted(folders)}"
    )
