"""Tests for scripts/validate_skills.py.

Covers missing front matter, missing required keys, name/folder mismatch,
and a non-semver version, plus a valid skill that should pass.
"""

from __future__ import annotations

import sys
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_skills  # noqa: E402

VALID_SKILL = dedent(
    """\
    ---
    name: demo-skill
    description: A demo skill used only in tests.
    version: 1.0.0
    license: MIT
    tools: [none]
    ---

    # Demo skill
    Do the job. Never publish.
    """
)


def _write_skill(
    tmp_path: Path, folder: str = "demo-skill", skill_md: str = VALID_SKILL
) -> Path:
    skill_dir = tmp_path / "skills" / folder
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")
    (skill_dir / "README.md").write_text("how to use\n", encoding="utf-8")
    (skill_dir / "checks.md").write_text("checks\n", encoding="utf-8")
    return skill_dir


def test_valid_skill_has_no_errors(tmp_path: Path) -> None:
    skill_dir = _write_skill(tmp_path)
    assert validate_skills.validate_skill(skill_dir) == []


def test_no_front_matter(tmp_path: Path) -> None:
    skill_dir = _write_skill(tmp_path, skill_md="# No yaml here\n")
    errors = validate_skills.validate_skill(skill_dir)
    assert errors
    assert any("front matter" in e.lower() for e in errors)


def test_missing_required_key(tmp_path: Path) -> None:
    md = dedent(
        """\
        ---
        name: demo-skill
        description: Missing version on purpose.
        license: MIT
        tools: [none]
        ---
        Body
        """
    )
    skill_dir = _write_skill(tmp_path, skill_md=md)
    errors = validate_skills.validate_skill(skill_dir)
    assert any("version" in e.lower() for e in errors)


def test_name_mismatch(tmp_path: Path) -> None:
    md = VALID_SKILL.replace("name: demo-skill", "name: other-name")
    skill_dir = _write_skill(tmp_path, skill_md=md)
    errors = validate_skills.validate_skill(skill_dir)
    assert any("name" in e.lower() and "folder" in e.lower() for e in errors)


def test_bad_version(tmp_path: Path) -> None:
    md = VALID_SKILL.replace("version: 1.0.0", "version: uno")
    skill_dir = _write_skill(tmp_path, skill_md=md)
    errors = validate_skills.validate_skill(skill_dir)
    assert any("version" in e.lower() or "semver" in e.lower() for e in errors)


def test_cli_exits_nonzero_when_a_skill_is_invalid(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    _write_skill(tmp_path, skill_md="# no front matter\n")
    monkeypatch.chdir(tmp_path)
    rc = validate_skills.main()
    captured = capsys.readouterr()
    assert rc != 0
    assert captured.out or captured.err


def test_repo_skills_validate() -> None:
    errors: list[str] = []
    for skill_dir in validate_skills.iter_skill_dirs(ROOT):
        errors.extend(validate_skills.validate_skill(skill_dir))
    assert errors == []
