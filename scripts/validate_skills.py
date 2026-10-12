#!/usr/bin/env python3
"""Validate skills/*/SKILL.md against the Agent Skills spec.

Rules match agentskills.io/specification and skills-ref:
required name + description; optional license, compatibility, metadata,
allowed-tools; no other front-matter keys.

Exit 0 when every skill passes. Exit non-zero with a clear message on failure.
Stdlib plus PyYAML.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

REQUIRED_KEYS = ("name", "description")
ALLOWED_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_COMPATIBILITY = 500
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


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


def _validate_name(name: Any, skill_dir: Path, skill_md: Path) -> list[str]:
    errors: list[str] = []
    if not isinstance(name, str) or not name.strip():
        errors.append(f"{skill_md}: Field 'name' must be a non-empty string")
        return errors
    name = name.strip()
    if len(name) > MAX_NAME:
        errors.append(
            f"{skill_md}: Skill name '{name}' exceeds {MAX_NAME} character limit "
            f"({len(name)} chars)"
        )
    if name != name.lower():
        errors.append(f"{skill_md}: Skill name '{name}' must be lowercase")
    if name.startswith("-") or name.endswith("-"):
        errors.append(f"{skill_md}: Skill name cannot start or end with a hyphen")
    if "--" in name:
        errors.append(f"{skill_md}: Skill name cannot contain consecutive hyphens")
    if not NAME_RE.fullmatch(name):
        # Keep the skills-ref wording for letters/digits/hyphens even when
        # NAME_RE already failed for another reason (e.g. underscore).
        if not all(c.isalnum() or c == "-" for c in name) or any(
            c.isupper() for c in name
        ):
            errors.append(
                f"{skill_md}: Skill name '{name}' contains invalid characters. "
                "Only letters, digits, and hyphens are allowed."
            )
        elif not errors:
            errors.append(
                f"{skill_md}: Skill name '{name}' is not a valid kebab-case name"
            )
    if skill_dir.name != name:
        errors.append(
            f"{skill_md}: Directory name '{skill_dir.name}' must match skill name '{name}'"
        )
    return errors


def _validate_description(description: Any, skill_md: Path) -> list[str]:
    if not isinstance(description, str) or not description.strip():
        return [f"{skill_md}: Field 'description' must be a non-empty string"]
    if len(description) > MAX_DESCRIPTION:
        return [
            f"{skill_md}: Description exceeds {MAX_DESCRIPTION} character limit "
            f"({len(description)} chars)"
        ]
    return []


def validate_skill(skill_dir: Path) -> list[str]:
    """Return a list of error messages. Empty means the skill is valid."""
    errors: list[str] = []
    skill_dir = Path(skill_dir)
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.is_file():
        errors.append(f"{skill_dir}: Missing required file: SKILL.md")
        return errors

    data, fm_error = _load_front_matter(skill_md)
    if fm_error:
        errors.append(fm_error)
        return errors

    assert data is not None
    extra = sorted(set(data.keys()) - ALLOWED_FIELDS)
    if extra:
        errors.append(
            f"{skill_md}: Unexpected fields in frontmatter: {', '.join(extra)}. "
            f"Only {sorted(ALLOWED_FIELDS)} are allowed."
        )

    if "name" not in data:
        errors.append(f"{skill_md}: Missing required field in frontmatter: name")
    else:
        errors.extend(_validate_name(data["name"], skill_dir, skill_md))

    if "description" not in data:
        errors.append(f"{skill_md}: Missing required field in frontmatter: description")
    else:
        errors.extend(_validate_description(data["description"], skill_md))

    if "compatibility" in data:
        compat = data["compatibility"]
        if not isinstance(compat, str):
            errors.append(f"{skill_md}: Field 'compatibility' must be a string")
        elif len(compat) > MAX_COMPATIBILITY:
            errors.append(
                f"{skill_md}: Compatibility exceeds {MAX_COMPATIBILITY} character limit "
                f"({len(compat)} chars)"
            )

    if "allowed-tools" in data and not isinstance(data["allowed-tools"], str):
        errors.append(
            f"{skill_md}: Field 'allowed-tools' must be a space-separated string"
        )

    if "license" in data and not isinstance(data["license"], str):
        errors.append(f"{skill_md}: Field 'license' must be a string")

    if "metadata" in data:
        meta = data["metadata"]
        if not isinstance(meta, dict):
            errors.append(
                f"{skill_md}: Field 'metadata' must be a map from string keys to string values"
            )
        else:
            for key, value in meta.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    errors.append(
                        f"{skill_md}: metadata[{key!r}] must be a string "
                        f"(got {type(value).__name__})"
                    )

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
