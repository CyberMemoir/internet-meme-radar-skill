from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"


def main() -> int:
    text = SKILL.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        print("SKILL.md must start with YAML frontmatter.")
        return 1

    try:
        _, frontmatter, body = text.split("---\n", 2)
    except ValueError:
        print("SKILL.md frontmatter is not closed.")
        return 1

    required = ("name:", "description:")
    missing = [key for key in required if key not in frontmatter]
    if missing:
        print(f"Missing frontmatter keys: {', '.join(missing)}")
        return 1

    if "Meme Summary" not in body:
        print("Expected Meme Summary output format in SKILL.md.")
        return 1

    for path in (
        ROOT / "references" / "taxonomy.md",
        ROOT / "references" / "platform-methods.md",
        ROOT / "references" / "safety.md",
    ):
        if not path.exists():
            print(f"Missing reference: {path.relative_to(ROOT)}")
            return 1

    print("Skill structure is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
