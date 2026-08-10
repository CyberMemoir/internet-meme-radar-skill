---
name: internet-meme-radar
description: Research and explain current internet memes, slang, viral jokes, short-video trends, comment-section references, sounds, hashtags, edit formats, and visual templates. Use for meaning, origin, tone, lifecycle, popularity, cross-platform spread, or safe usage questions involving TikTok, Douyin, YouTube Shorts, Bilibili, Xiaohongshu/RED, Weibo, Kuaishou, Instagram Reels, X, and related communities; verify time-sensitive claims with recent evidence and label uncertainty.
---

# Internet Meme Radar

Analyze memes as changing cultural signals rather than fixed dictionary entries. Separate meaning, usage, origin, lifecycle, platform context, risk, and confidence.

## Research route

1. **Scope the claim.** Identify the exact phrase or format, target platform/community, locale, and time window. Ask for missing artifacts only when they materially affect the answer.
2. **Normalize the query.** Generate spelling, punctuation, hashtag, emoji, translation, pinyin/romanization, homophone, and deliberate-misspelling variants. Add intent terms such as meaning, origin, template, sound, or trend.
3. **Collect evidence.** For current-status claims, prefer 5–10 dated examples from independent creators on the target platform, then 2–5 cross-platform examples and 1–3 contextual sources when useful. Deduplicate reposts.
4. **Map claims to sources.** Read `references/evidence-rubric.md` for source tiers, recency windows, and the evidence ledger. Do not use one source to support a claim it does not establish.
5. **Classify the format.** Read `references/taxonomy.md` when the type is ambiguous. Apply multiple labels when needed.
6. **Explain meaning and use.** Separate literal meaning from pragmatic meaning. Describe tone, audience, common setup, typical response, and whether use is sincere, ironic, mocking, cute, edgy, or nostalgic.
7. **Trace origin cautiously.** Distinguish creation, earliest verifiable artifact, and later popularization. Label the result `Confirmed`, `Likely`, `Possible`, `Unknown`, or `Misattributed`.
8. **Assess lifecycle.** Read `references/lifecycle.md`. Report `Emerging`, `Rising`, `Mainstream`, `Niche`, `Declining`, `Outdated`, `Revived`, `Manufactured`, or `Unknown`; always bind the label to a platform/community and time window.
9. **Check misuse risk.** Flag insulting, political, sexual, age-sensitive, regional, fandom-specific, commercial, outdated, or context-dependent use. Read `references/safety.md` for risky trends.
10. **Calibrate confidence.** Use `High` only for multiple consistent recent sources; `Medium` for a clear meaning with partial origin/spread evidence; `Low` for sparse, stale, conflicting, or inaccessible evidence.

For platform-specific collection signals, read `references/platform-methods.md`. For Xiaohongshu/RED research, also read `references/xiaohongshu.md`.

## Evidence rules

- Never call a meme current or trending without recent dated evidence.
- Treat feeds, search ordering, and visible engagement as samples—not population statistics.
- Separate organic adoption from one-creator virality, repost networks, fandom bursts, and coordinated marketing.
- State access limits and missing evidence. When direct access is unavailable, request representative links, screenshots, captions, dates, sounds, hashtags, or comments.
- Cite sources when browsing; identify which conclusion each source supports.
- Use only normally accessible public evidence, user-provided material, or official APIs. Do not bypass access controls or collect private information.

## Answer formats

For a quick definition, answer in 2–5 sentences: meaning, tone, one natural example, and one caveat. For research requests, use:

```markdown
## Meme Summary

**Phrase / format:** ...
**Meaning:** ...
**How people use it:** ...
**Tone and audience:** ...
**Origin:** Confirmed / Likely / Possible / Unknown / Misattributed — ...
**Current lifecycle:** ... on [platform/community] during [time window]
**Platform context:** ...
**Examples:**
1. ...
2. ...
**Misuse risk:** ...
**Confidence:** High / Medium / Low
**Evidence and limits:** ...
```

For batches, use:

```markdown
| Phrase | Type | Meaning | Platform + window | Lifecycle | Risk | Confidence |
|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... |
```

Explain only the most important, risky, or uncertain items after the table.

## Optional trend score

Calculate a score only when every component has enough evidence. Score each component from 0–100, explain the inputs, then run `scripts/trend_score.py` or use:

```text
0.30 × Recency
+ 0.20 × Repetition
+ 0.15 × CreatorSpread
+ 0.15 × CommentAdoption
+ 0.10 × RemixPotential
+ 0.10 × PlatformSpread
```

A score is a structured estimate, not a platform statistic. Never use it to conceal missing data.

## Final check

- Verify that dates match the claimed time window.
- Separate literal meaning, actual usage, and tone.
- Distinguish origin from popularization.
- Bind lifecycle claims to a platform or community.
- Mention contradictions, access gaps, and sample bias.
- Justify the confidence label.
