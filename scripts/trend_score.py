#!/usr/bin/env python3
"""Calculate a transparent meme trend score from six normalized signals."""

from __future__ import annotations

import argparse
import json
from typing import Mapping


WEIGHTS = {
    "recency": 0.30,
    "repetition": 0.20,
    "creator_spread": 0.15,
    "comment_adoption": 0.15,
    "remix_potential": 0.10,
    "platform_spread": 0.10,
}


def calculate(signals: Mapping[str, float]) -> float:
    missing = set(WEIGHTS) - set(signals)
    extra = set(signals) - set(WEIGHTS)
    if missing or extra:
        raise ValueError(f"signals mismatch; missing={sorted(missing)}, extra={sorted(extra)}")
    for name, value in signals.items():
        if not 0 <= value <= 100:
            raise ValueError(f"{name} must be between 0 and 100")
    return round(sum(signals[name] * weight for name, weight in WEIGHTS.items()), 1)


def label(score: float) -> str:
    if score <= 20:
        return "insufficient-or-not-a-meme"
    if score <= 40:
        return "niche-or-weak"
    if score <= 60:
        return "real-but-limited"
    if score <= 80:
        return "strong-platform-trend"
    return "major-cross-platform-trend"


def main() -> int:
    parser = argparse.ArgumentParser()
    for key in WEIGHTS:
        parser.add_argument(f"--{key.replace('_', '-')}", type=float, required=True)
    args = parser.parse_args()
    signals = {key: getattr(args, key) for key in WEIGHTS}
    score = calculate(signals)
    print(json.dumps({"score": score, "label": label(score)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
