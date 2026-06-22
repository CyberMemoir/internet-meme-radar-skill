# Internet Meme Radar Skill

Codex skill for analyzing current internet memes, slang, viral jokes, short-video trends, and platform-specific cultural references with evidence and uncertainty.

The skill is written in English for broad use. It can still answer in the user's language when a user asks in Chinese or another language.

## What It Helps With

- Explaining what a meme or slang phrase means.
- Checking whether a phrase, sound, hashtag, edit format, or visual template is actually trending.
- Separating literal meaning from real usage and tone.
- Avoiding invented origin stories.
- Comparing platform-specific context across TikTok, Douyin, YouTube Shorts, Bilibili, Xiaohongshu, Weibo, Kuaishou, Instagram Reels, and X.
- Labeling confidence based on evidence quality.

## Files

- `SKILL.md`: main skill instructions.
- `references/taxonomy.md`: meme type labels.
- `references/platform-methods.md`: platform research methods and trend signals.
- `references/safety.md`: safety and privacy notes.
- `scripts/validate_skill.py`: basic structure validator.

## Validate

```bash
python3 scripts/validate_skill.py
```

## Install Manually

Copy this folder into a Codex skills directory, or install it using your normal Codex skill workflow.
