# Standalone collection and rule analysis

These scripts run without Codex, an LLM, embeddings, OCR, ASR, learned language
identification, or per-record approval. The original interactive research skill is
still available; it is not the scheduler for this mode.

```sh
python scripts/collect_web.py --urls urls.txt --allow-host example.org --output .data/web-window-01
python scripts/analyze_sources.py --input .data/web-window-01/items.jsonl --catalog catalog.json --output .data/analysis.json
```

The URL list is explicit and bounded to 100 unique URLs, with serial requests at
least 20 seconds apart. This initial adapter does not automatically search the web
or follow new links. Redirects require a separately checked URL. Access restrictions
stop that host and remain in the checkpoint; failures are not retried automatically.
Run one process per output directory. Use only public, normally accessible sources
that permit the intended collection. Successful sources are not fetched again on
resume, and original observed times are retained. HTML is limited to 4 MB; strict
decoding failures are explicit. Text locators refer to parsed JSON, not HTML offsets.

HTTP 200 challenge pages with explicit verification/access-denied titles stop the
host too; they are not archived as successful article text. The stop remains in
the checkpoint across restarts. Ordinary articles discussing verification are
not classified from body keywords alone. The four offline tests include both
cases and persistent host-stop/resume behavior.

The analysis input is JSONL with source_id, url, texts[{text,locator}] and optional
source evidence. Accepting a rule match requires a local JSON evidence file, its
SHA-256, and a JSON pointer that resolves to the exact text. The path is confined to
the input archive. Missing or tampered binding produces invalid_evidence. A text_evidence
reference is used for extracted web text; raw HTML is retained separately. A catalog
entry has id, name, optional aliases, and optional
use_pattern: an operator-maintained Python regex that must match the complete text.
No gold set, model query file, or frozen research data is needed. Match rules require
development calibration; text names alone produce mention_only. Qualified use rules
produce rule_accepted_use, meaning the configured rule matched, not a historical
truth or media-derived relationship. This version emits observed_use, not derivative.

Source definitions are extracted only from an explicitly name-bound explanation
sentence and remain separate candidates. Existing definitions and usage context are
not updated. Demand-like original sentences are real_expression, not real submitted
search logs; rule matching does not establish that an author is human. Identity,
conflict handling and reuse evidence for formal new memes are not implemented here:
M_new_memes is explicitly zero, not an automatic approval. No script writes to the
business database. New formal entry qualification belongs to the shared analysis
pipeline, not a platform reader or this research skill.

Run offline checks with `python -m unittest discover -s tests`.

## Continuous server collection

For sustained collection use the shared [CyberMemoir collector](https://github.com/CyberMemoir/cyber-memoir/tree/codex/bilibili-text-collector-20261014/apps/collector).
Its web adapter supports explicit allowlisted HTTPS URL lists and RSS/Atom discovery,
durable scheduled windows, leases, per-platform process locks, bounded request pacing,
cross-window item/version/observation deduplication, immutable raw HTML plus parsed
text views, disk quotas, status metrics and verified backups. It does not import this
interactive skill or run an agent. Standalone collect_web.py remains the bounded
manual-window helper, not a sustained server scheduler.

Feed-discovered links must remain inside the exact host allowlist. Dynamic pages,
unexpected redirects and access challenges stop; there is no browser/model fallback.
Request and item budgets preserve explicit partial coverage. This is an archive,
not automatic formal meme admission. The legacy analysis helper expects its own
items.jsonl evidence layout; the shared collector export is a distinct versioned
source schema, not a drop-in input for analyze_sources.py.

Offline recovery checks do not establish live source availability. Complete the
shared service's Linux/live-window acceptance before expanding volume.

