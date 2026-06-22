---
name: internet-meme-radar
description: Use when users ask about current internet memes, slang, viral jokes, short-video trends, comment-section references, platform-specific culture, or whether a phrase, sound, hashtag, edit format, or visual template is trending. This skill emphasizes evidence, recency, platform context, origin uncertainty, tone, and safe compliance for platforms such as TikTok, Douyin, YouTube Shorts, Bilibili, Xiaohongshu, Weibo, Kuaishou, Instagram Reels, and X.
---

# Internet Meme Radar

Use this skill to analyze memes as living cultural signals, not dictionary entries. Always separate meaning, usage, origin, popularity, platform context, misuse risk, and confidence.

## Core Rule

Do not claim a meme is "currently trending" without recent evidence. If current evidence is unavailable, say so and ask for a link, screenshot, caption, comments, sound name, hashtag, or sample posts.

## Compliance

Use allowed evidence only: user-provided links/screenshots/text, official APIs, public pages that may be accessed normally, reputable explainers, search snippets, and manually supplied samples. Do not bypass login, paywalls, rate limits, CAPTCHAs, signatures, device fingerprints, anti-bot systems, or platform risk controls. Do not use private cookies, stolen tokens, unauthorized accounts, or hidden browser automation. Do not collect private user information.

For harmful, sexual, bullying, self-harm, dangerous challenge, drugs, weapons, illegal behavior, minors, or harassment-related trends, summarize safely and avoid amplifying operational details.

## Workflow

1. Normalize the query.
   - Extract original phrase, hashtags, spelling variants, abbreviations, homophones, emoji variants, punctuation variants, translated forms, romanization/pinyin if relevant, and "meaning/origin/trend" search forms.
2. Collect a focused evidence sample.
   - Prefer 5-10 recent examples from the target platform if available.
   - Add 2-5 cross-platform examples if the meme appears elsewhere.
   - Add 1-3 explanation sources when useful.
   - Use comments to confirm shared interpretation when possible.
3. Classify meme type.
   - Use the taxonomy in `references/taxonomy.md` when classification is non-obvious.
4. Explain literal meaning.
5. Explain actual usage.
   - Include tone, situations, comment patterns, audience, whether it is sincere, ironic, mocking, cringe, cute, wholesome, edgy, etc.
6. Trace origin cautiously.
   - Use labels: Confirmed origin, Likely origin, Possible origin, Unknown origin, Misattributed origin.
   - Never invent one origin when evidence is weak or conflicting.
7. Estimate current popularity.
   - Use labels: Emerging, Rising, Mainstream, Niche, Declining, Outdated, Unknown.
   - For platform-specific method details, read `references/platform-methods.md`.
8. Check misuse risk.
   - Flag if it may be insulting, age-sensitive, political, sexual, controversial, regional, fandom-specific, outdated, or likely to sound awkward outside its context.
9. Assign confidence.
   - High: multiple recent examples, consistent usage, clear context, reliable support.
   - Medium: meaning is likely clear, but origin/popularity/platform spread is partly uncertain.
   - Low: few examples, multiple meanings, private-joke signal, stale sources, or insufficient access.
10. Answer in the user's language unless they ask otherwise.

## Output Format

Use this structure unless the user requests a quick answer, a table, or another format:

```markdown
## Meme Summary

**Phrase / Trend:**  
...

**Meaning:**  
...

**How people use it:**  
...

**Tone:**  
...

**Origin:**  
...

**Current popularity:**  
...

**Platform context:**  
...

**Example usage:**  
1. ...
2. ...
3. ...

**Misuse risk:**  
...

**Confidence:** High / Medium / Low

**Why this confidence:**  
...
```

## Batch Format

When the user gives many possible memes, return:

```markdown
| Phrase | Meme Type | Meaning | Current Status | Risk | Confidence |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |
```

Then explain only the most important or uncertain items.

## Trend Score

Only calculate a 0-100 trend score when evidence is strong enough. Use:

```text
Trend Score =
0.30 * Recency
+ 0.20 * Repetition
+ 0.15 * CrossCreatorSpread
+ 0.15 * CommentAdoption
+ 0.10 * RemixPotential
+ 0.10 * CrossPlatformSpread
```

Labels: 0-20 not a meme or too little evidence; 21-40 niche/weak signal; 41-60 real but limited trend; 61-80 strong platform trend; 81-100 major cross-platform meme.

## Evidence Notes

If web access is available and the user asks about "latest/current/today/recent/trending", browse or otherwise verify current evidence. Cite sources or describe user-provided evidence. If platform access is blocked or uncertain, say what evidence is missing and request specific samples.

Before finalizing, check:

- Literal meaning and actual usage are separated.
- Origin is not invented.
- Current popularity is supported or labeled unknown.
- Platform context and tone are included.
- Misuse risk is included.
- Confidence level is justified.
