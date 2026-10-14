"""Collect an explicit public URL list without an AI agent, models or a search service."""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import socket
import time
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener


class AccessBlocked(RuntimeError):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise AccessBlocked("Redirect requires a separately checked URL; stopped")


class PageText(HTMLParser):
    """Conservative text blocks; no learned language identification or semantic inference."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skipped = 0
        self.parts = []
        self.blocks = []

    def flush(self):
        text = "".join(self.parts).strip()
        if text:
            self.blocks.append(text)
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "nav", "footer"}:
            self.skipped += 1
        if not self.skipped and tag in {
            "p",
            "div",
            "li",
            "h1",
            "h2",
            "h3",
            "br",
            "article",
        }:
            self.flush()

    def handle_endtag(self, tag):
        if tag in {"script", "style", "nav", "footer"}:
            self.skipped = max(0, self.skipped - 1)
        if not self.skipped and tag in {"p", "div", "li", "h1", "h2", "h3", "article"}:
            self.flush()

    def handle_data(self, data):
        if not self.skipped:
            self.parts.append(data)


def parse_html(body: bytes, charset="utf-8") -> list[str]:
    parser = PageText()
    parser.feed(body.decode(charset, errors="strict"))
    parser.flush()
    return parser.blocks


def fetch_public(url: str, allowed_hosts: set[str]) -> tuple[bytes, str]:
    parsed = urlsplit(url)
    if (
        parsed.scheme != "https"
        or parsed.hostname not in allowed_hosts
        or parsed.username
        or parsed.password
        or parsed.port not in (None, 443)
    ):
        raise ValueError("Only explicit allowlisted HTTPS URLs are accepted")
    answers = socket.getaddrinfo(parsed.hostname, 443, type=socket.SOCK_STREAM)
    if any(not ipaddress.ip_address(answer[4][0]).is_global for answer in answers):
        raise ValueError("Internal addresses are not public source material")
    try:
        request = Request(url, headers={"User-Agent": "CyberMemoir-WebCollector/1.0"})
        with build_opener(ProxyHandler({}), NoRedirect).open(
            request, timeout=20
        ) as response:
            if response.headers.get_content_type() != "text/html":
                raise ValueError("Only HTML is supported by this initial adapter")
            body = response.read(4_000_001)
            if len(body) > 4_000_000:
                raise ValueError("Page exceeds size budget")
            return body, response.headers.get_content_charset() or "utf-8"
    except HTTPError as exc:
        if exc.code in {401, 403, 412, 429, 461, 471}:
            raise AccessBlocked(f"HTTP {exc.code}; stop this host") from exc
        raise


def write_json(path: Path, value):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def collect(
    urls: list[str],
    output: Path,
    allowed_hosts: set[str],
    fetch=fetch_public,
    sleep=time.sleep,
    interval=20,
):
    if not 1 <= len(urls) <= 100 or len(set(urls)) != len(urls) or interval < 20:
        raise ValueError(
            "Use 1–100 unique URLs with at least 20 seconds between requests"
        )
    output.mkdir(parents=True, exist_ok=True)
    checkpoint = output / "checkpoint.json"
    config = {"urls": urls, "hosts": sorted(allowed_hosts)}
    state = (
        json.loads(checkpoint.read_text(encoding="utf-8"))
        if checkpoint.exists()
        else {
            "config": config,
            "sources": {},
            "failures": {},
            "blocked_hosts": [],
            "last_request_at": 0,
        }
    )
    if state["config"] != config:
        raise ValueError("Changed inputs require a new output directory")
    for url in urls:
        host = urlsplit(url).hostname
        if (
            url in state["sources"]
            or url in state["failures"]
            or host in state["blocked_hosts"]
        ):
            continue
        key = hashlib.sha256(url.encode()).hexdigest()
        raw = output / f"{key}.html"
        try:
            sleep(max(0, state["last_request_at"] + interval - time.time()))
            state["last_request_at"] = time.time()
            write_json(checkpoint, state)
            body, charset = fetch(url, allowed_hosts)
            raw.write_bytes(body)
            observed = datetime.now(UTC).isoformat()
            texts = [
                {"kind": "web_text", "text": text, "locator": f"/texts/{index}/text"}
                for index, text in enumerate(parse_html(body, charset))
            ]
            item = {
                "source_id": "web:" + key,
                "url": url,
                "platform": "web",
                "texts": texts,
                "author_public_id": None,
                "observed_at": observed,
                "status": "source_archived",
                "evidence": {
                    "path": raw.name,
                    "sha256": hashlib.sha256(body).hexdigest(),
                    "locator_basis": "parsed_text_artifact_not_HTML_offsets",
                },
                "is_actual_search_log": False,
            }
            artifact = output / f"{key}.json"
            write_json(artifact, item)
            item["text_evidence"] = {
                "path": artifact.name,
                "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
            }
            state["sources"][url] = item
        except Exception as exc:
            state["failures"][url] = {"type": type(exc).__name__, "message": str(exc)}
            if isinstance(exc, AccessBlocked):
                state["blocked_hosts"].append(host)
        write_json(checkpoint, state)
    text = "".join(
        json.dumps(item, ensure_ascii=False) + "\n"
        for item in state["sources"].values()
    )
    (output / "items.jsonl").write_text(text, encoding="utf-8")
    return state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--urls", type=Path, required=True, help="UTF-8 file, one explicit URL per line"
    )
    parser.add_argument("--allow-host", action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    urls = [
        line.strip()
        for line in args.urls.read_text(encoding="utf-8-sig").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    state = collect(urls, args.output, set(args.allow_host))
    print(
        json.dumps(
            {
                "sources": len(state["sources"]),
                "failures": len(state["failures"]),
                "blocked_hosts": state["blocked_hosts"],
            }
        )
    )
    return 2 if state["failures"] or state["blocked_hosts"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
