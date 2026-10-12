#!/usr/bin/env python3
"""Validate skills/*/SKILL.md front matter and required files.

Exit 0 when every skill passes. Exit non-zero with a clear message on failure.
Stdlib plus PyYAML only.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

REQUIRED_KEYS = ("name", "description", "version", "license", "tools")
REQUIRED_FILES = ("SKILL.md", "README.md", "checks.md")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _load_front_matter(skill_md: Path) -> tuple[dict[str, Any] | None, str | None]:
    """Return (data, error). error is set when front matter is missing or unparseable."""
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None, f"{skill_md}: missing YAML front matter (must start with ---)"
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, f"{skill_md}: front matter is not closed with a second ---"
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        return None, f"{skill_md}: front matter is not parseable YAML: {exc}"
    if not isinstance(data, dict):
        return None, f"{skill_md}: front matter must be a YAML mapping"
    return data, None


def validate_skill(skill_dir: Path) -> list[str]:
    """Return a list of error messages. Empty means the skill is valid."""
    errors: list[str] = []
    skill_dir = Path(skill_dir)
    folder = skill_dir.name
    skill_md = skill_dir / "SKILL.md"

    for name in REQUIRED_FILES:
        path = skill_dir / name
        if not path.is_file():
            errors.append(f"{skill_dir}: required file missing: {name}")

    if not skill_md.is_file():
        return errors

    data, fm_error = _load_front_matter(skill_md)
    if fm_error:
        errors.append(fm_error)
        return errors

    assert data is not None
    for key in REQUIRED_KEYS:
        if key not in data or data[key] in (None, ""):
            errors.append(f"{skill_md}: missing required key: {key}")

    name = data.get("name")
    if name is not None:
        if not isinstance(name, str) or not KEBAB.fullmatch(name):
            errors.append(
                f"{skill_md}: name must be kebab-case (got {name!r})"
            )
        elif name != folder:
            errors.append(
                f"{skill_md}: name {name!r} does not match folder {folder!r}"
            )

    description = data.get("description")
    if description is not None:
        if not isinstance(description, str):
            errors.append(f"{skill_md}: description must be a string")
        else:
            if "\n" in description.strip():
                errors.append(f"{skill_md}: description must be one line")
            if len(description) > 200:
                errors.append(
                    f"{skill_md}: description must be <= 200 characters "
                    f"(got {len(description)})"
                )

    version = data.get("version")
    if version is not None:
        version_str = str(version)
        # YAML may parse 1.0.0 as a string already; 1.0 as a float.
        if not isinstance(version, str) or not SEMVER.fullmatch(version_str):
            errors.append(
                f"{skill_md}: version must be semver MAJOR.MINOR.PATCH "
                f"(got {version!r})"
            )

    license_value = data.get("license")
    if license_value is not None and license_value != "MIT":
        errors.append(f"{skill_md}: license must be MIT (got {license_value!r})")

    tools = data.get("tools")
    if tools is not None and not isinstance(tools, list):
        errors.append(f"{skill_md}: tools must be a list (got {type(tools).__name__})")

    return errors


def iter_skill_dirs(root: Path) -> list[Path]:
    skills = root / "skills"
    if not skills.is_dir():
        return []
    return sorted(p.parent for p in skills.glob("*/SKILL.md"))


def main(argv: list[str] | None = None) -> int:
    root = Path.cwd() if not argv else Path(argv[0])
    skill_dirs = iter_skill_dirs(root)
    if not skill_dirs:
        print(f"No skills found under {root / 'skills'}", file=sys.stderr)
        return 1

    failed = False
    for skill_dir in skill_dirs:
        errors = validate_skill(skill_dir)
        if errors:
            failed = True
            print(f"FAIL {skill_dir.relative_to(root)}")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"OK   {skill_dir.relative_to(root)}")

    if failed:
        print("validate_skills: one or more skills failed", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
