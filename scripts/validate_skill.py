from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
REQUIRED_REFERENCES = {
    "taxonomy.md", "platform-methods.md", "safety.md",
    "evidence-rubric.md", "lifecycle.md", "xiaohongshu.md",
}


def fail(message: str) -> int:
    print(f"ERROR: {message}")
    return 1


def main() -> int:
    if not SKILL.exists():
        return fail("missing SKILL.md")
    text = SKILL.read_text(encoding="utf-8")
    match = re.fullmatch(r"---\n(.*?)\n---\n(.*)", text, re.DOTALL)
    if not match:
        return fail("SKILL.md needs closed YAML frontmatter")
    frontmatter, body = match.groups()
    keys = [line.split(":", 1)[0] for line in frontmatter.splitlines() if ":" in line]
    if keys != ["name", "description"]:
        return fail("frontmatter must contain only name and description, in that order")
    if "name: internet-meme-radar" not in frontmatter:
        return fail("unexpected skill name")
    if len(body.splitlines()) > 500:
        return fail("SKILL.md exceeds 500 lines")
    for marker in ("## Research route", "## Answer formats", "## Final check"):
        if marker not in body:
            return fail(f"missing section: {marker}")
    existing = {path.name for path in (ROOT / "references").glob("*.md")}
    missing = REQUIRED_REFERENCES - existing
    if missing:
        return fail(f"missing references: {', '.join(sorted(missing))}")
    if not (ROOT / "agents" / "openai.yaml").exists():
        return fail("missing agents/openai.yaml")
    print("Skill structure is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
