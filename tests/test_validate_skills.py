"""Tests for scripts/validate_skills.py against the Agent Skills spec.

Required front-matter: name, description.
Allowed optional: license, compatibility, metadata, allowed-tools.
Unexpected keys (version, tools, …) fail. See agentskills.io/specification.
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
    description: A demo skill used only in tests. Use when validating front matter.
    license: MIT
    metadata:
      version: "1.0.0"
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
    return skill_dir


def test_valid_skill_has_no_errors(tmp_path: Path) -> None:
    skill_dir = _write_skill(tmp_path)
    assert validate_skills.validate_skill(skill_dir) == []


def test_minimal_name_and_description_pass(tmp_path: Path) -> None:
    md = dedent(
        """\
        ---
        name: demo-skill
        description: Minimal valid skill.
        ---
        Body
        """
    )
    assert validate_skills.validate_skill(_write_skill(tmp_path, skill_md=md)) == []


def test_no_front_matter(tmp_path: Path) -> None:
    skill_dir = _write_skill(tmp_path, skill_md="# No yaml here\n")
    errors = validate_skills.validate_skill(skill_dir)
    assert errors
    assert any("front matter" in e.lower() or "frontmatter" in e.lower() for e in errors)


def test_missing_description(tmp_path: Path) -> None:
    md = dedent(
        """\
        ---
        name: demo-skill
        license: MIT
        ---
        Body
        """
    )
    errors = validate_skills.validate_skill(_write_skill(tmp_path, skill_md=md))
    assert any("description" in e.lower() for e in errors)


def test_name_mismatch(tmp_path: Path) -> None:
    md = VALID_SKILL.replace("name: demo-skill", "name: other-name")
    errors = validate_skills.validate_skill(_write_skill(tmp_path, skill_md=md))
    assert any("name" in e.lower() and "director" in e.lower() for e in errors)


def test_unexpected_version_field(tmp_path: Path) -> None:
    md = dedent(
        """\
        ---
        name: demo-skill
        description: Top-level version is not an allowed field.
        version: 1.0.0
        ---
        Body
        """
    )
    errors = validate_skills.validate_skill(_write_skill(tmp_path, skill_md=md))
    assert any("version" in e.lower() and "unexpected" in e.lower() for e in errors)


def test_unexpected_tools_field(tmp_path: Path) -> None:
    md = dedent(
        """\
        ---
        name: demo-skill
        description: Top-level tools is not an allowed field.
        tools: ["none"]
        ---
        Body
        """
    )
    errors = validate_skills.validate_skill(_write_skill(tmp_path, skill_md=md))
    assert any("tools" in e.lower() and "unexpected" in e.lower() for e in errors)


def test_consecutive_hyphens_in_name(tmp_path: Path) -> None:
    md = dedent(
        """\
        ---
        name: demo--skill
        description: Consecutive hyphens are invalid.
        ---
        Body
        """
    )
    skill_dir = _write_skill(tmp_path, folder="demo--skill", skill_md=md)
    errors = validate_skills.validate_skill(skill_dir)
    assert any("consecutive" in e.lower() for e in errors)


def test_description_over_1024_chars(tmp_path: Path) -> None:
    md = dedent(
        f"""\
        ---
        name: demo-skill
        description: {"x" * 1025}
        ---
        Body
        """
    )
    errors = validate_skills.validate_skill(_write_skill(tmp_path, skill_md=md))
    assert any("1024" in e for e in errors)


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
