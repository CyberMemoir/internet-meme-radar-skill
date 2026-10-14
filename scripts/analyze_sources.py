"""Apply explicit text rules to archived JSONL. No models, network calls or publication."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

RULE_VERSION = "text-use-v1"
REQUEST = re.compile(
    r"(?:求.{0,30}(?:表情包|素材|模板)|(?:哪个|什么).{0,20}梗.{0,20}(?:适合|用)|(?:表情包|素材|模板).{0,20}(?:在哪|哪里|怎么找))"
)


def bound_text(item: dict, field: dict, source_root: Path | None) -> bool:
    reference = item.get("text_evidence") or item.get("evidence")
    if source_root is None or not isinstance(reference, dict):
        return False
    try:
        path = (source_root / reference["path"]).resolve()
        path.relative_to(source_root.resolve())
        if path.stat().st_size > 4_000_000:
            return False
        body = path.read_bytes()
        if hashlib.sha256(body).hexdigest() != reference["sha256"]:
            return False
        value = json.loads(body)
        locator = field["locator"]
        if not locator.startswith("/"):
            return False
        for part in locator[1:].split("/"):
            key = part.replace("~1", "/").replace("~0", "~")
            value = value[int(key)] if isinstance(value, list) else value[key]
        return value == field["text"]
    except (KeyError, IndexError, ValueError, TypeError, OSError):
        return False


def analyze(items, catalog: list[dict], source_root: Path | None = None) -> dict:
    uses, mentions, requests, definitions, invalid = [], [], [], [], []
    seen, source_ids = set(), set()
    for item in items:
        source_id = item["source_id"]
        source_ids.add(source_id)
        url = item["url"]
        for field in item.get("texts", []):
            text = field["text"]
            locator = field["locator"]
            fingerprint = hashlib.sha256(
                (source_id + "\0" + locator + "\0" + text).encode()
            ).hexdigest()
            if fingerprint in seen:
                continue
            seen.add(fingerprint)
            if not bound_text(item, field, source_root):
                invalid.append(
                    {
                        "source_id": source_id,
                        "locator": locator,
                        "status": "invalid_evidence",
                    }
                )
                continue
            qualifying = [
                meme["id"]
                for meme in catalog
                if meme.get("use_pattern") and re.fullmatch(meme["use_pattern"], text)
            ]
            if len(set(qualifying)) > 1:
                invalid.append(
                    {
                        "source_id": source_id,
                        "locator": locator,
                        "status": "ambiguous_identity",
                    }
                )
                continue
            evidence = {
                "source_id": source_id,
                "url": url,
                "locator": locator,
                "text_sha256": hashlib.sha256(text.encode()).hexdigest(),
                "source_evidence": item.get("evidence"),
                "text_evidence": item.get("text_evidence") or item.get("evidence"),
                "observed_at": item.get("observed_at")
                or (item.get("evidence") or {}).get("observed_at"),
                "original_text": text,
            }
            if REQUEST.search(text):
                requests.append(
                    {
                        **evidence,
                        "evidence_layer": "real_expression",
                        "is_actual_search_log": False,
                        "rule_version": RULE_VERSION,
                    }
                )
            for meme in catalog:
                names = [meme["name"], *meme.get("aliases", [])]
                if not any(name and name in text for name in names):
                    continue
                base = {
                    **evidence,
                    "meme_id": meme["id"],
                    "rule_version": RULE_VERSION,
                    "definition_change": False,
                    "usage_context_change": False,
                }
                pattern = meme.get("use_pattern")
                # Exact operator-specified full-text patterns decide qualification, not fuzzy similarity.
                if pattern and re.fullmatch(pattern, text):
                    uses.append(
                        {
                            **base,
                            "status": "rule_accepted_use",
                            "relation": "observed_use",
                        }
                    )
                else:
                    mentions.append({**base, "status": "mention_only"})
                for name in names:
                    explanation = re.search(
                        re.escape(name)
                        + r"[”\"']?(?:这个梗|这个表达)的意思是([^。！？\n]+)",
                        text,
                    )
                    if explanation:
                        definitions.append(
                            {
                                **base,
                                "status": "definition_excerpt_candidate",
                                "definition_excerpt": explanation.group(1),
                                "span": list(explanation.span(1)),
                                "span_unit": "unicode_codepoints_half_open",
                            }
                        )
    return {
        "rule_version": RULE_VERSION,
        "uses": uses,
        "mentions": mentions,
        "requests": requests,
        "definitions": definitions,
        "invalid": invalid,
        "metrics": {
            "unique_sources": len(source_ids),
            "V_observed_use": len(uses),
            "Q_request_sentences": len(requests),
            "M_new_memes": 0,
        },
        "public_import_authorized": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument(
        "--catalog",
        type=Path,
        required=True,
        help="Explicit names, IDs, aliases and use_pattern",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    catalog = json.loads(args.catalog.read_text(encoding="utf-8-sig"))
    if not isinstance(catalog, list) or any(
        not row.get("id") or not row.get("name") for row in catalog
    ):
        raise ValueError("Catalog requires explicit IDs and nonempty names")
    if len({row["id"] for row in catalog}) != len(catalog):
        raise ValueError("Duplicate catalog identities")
    with args.input.open(encoding="utf-8-sig") as stream:
        result = analyze(
            (json.loads(line) for line in stream if line.strip()),
            catalog,
            args.input.parent,
        )
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps(result["metrics"]))


if __name__ == "__main__":
    main()
