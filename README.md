# Internet Meme Radar Skill

An evidence-first Codex skill for researching internet memes, slang, viral jokes, short-video formats, comment culture, and platform-specific references without inventing origins or overstating popularity.

Part of [CyberMemoir](https://github.com/CyberMemoir), an open-source internet culture memory initiative developed and maintained by [Cogstruct AI](https://github.com/Cogstruct-ai).

> 🏆 **小红书悬赏人气 REDSkill 第 17 名**

## Highlights

- Verifies time-sensitive trend claims with dated, platform-specific evidence.
- Separates literal meaning, actual usage, tone, origin, popularization, and lifecycle.
- Detects repost inflation, fandom bursts, creator-only virality, and manufactured campaigns.
- Covers TikTok, Douyin, YouTube Shorts, Bilibili, Xiaohongshu/RED, Weibo, Kuaishou, Instagram Reels, and X.
- Includes a dedicated Xiaohongshu research playbook and an auditable trend-score calculator.
- Reports access limits, sampling bias, contradictions, and calibrated confidence.

## Example prompts

- “这个梗是什么意思？现在在小红书还火吗？”
- “Trace the earliest verifiable source of this reaction image.”
- “Compare how this phrase is used on Douyin and Bilibili.”
- “Is this audio an organic trend or a seeded campaign?”
- “Explain these 20 phrases in a compact risk-and-confidence table.”

## Structure

```text
internet-meme-radar-skill/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── evidence-rubric.md
│   ├── lifecycle.md
│   ├── platform-methods.md
│   ├── safety.md
│   ├── taxonomy.md
│   └── xiaohongshu.md
├── scripts/
│   ├── trend_score.py
│   └── validate_skill.py
└── tests/test_trend_score.py
```

## Validate

```bash
python3 scripts/validate_skill.py
python3 -m unittest discover -s tests -v
python3 scripts/trend_score.py \
  --recency 90 --repetition 75 --creator-spread 70 \
  --comment-adoption 65 --remix-potential 60 --platform-spread 40
```

## Install

Copy the repository into your Codex skills directory:

```bash
git clone https://github.com/CyberMemoir/internet-meme-radar-skill.git \
  ~/.codex/skills/internet-meme-radar
```

Restart or reload Codex so the skill metadata is discovered.

## Research principle

A viral post is not automatically a trend. The skill requires evidence of reuse, creator diversity, audience adoption, and an explicit time window before making a popularity claim.

## License

Apache-2.0 — see [LICENSE](LICENSE).
