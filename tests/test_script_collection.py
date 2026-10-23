import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from analyze_sources import analyze
from collect_web import AccessBlocked, collect, parse_html


class ScriptCollectionTests(unittest.TestCase):
    def test_http_200_challenge_stops_host_and_survives_resume(self):
        urls = ["https://example.org/challenge", "https://example.org/next"]
        calls = []

        def fetch(url, _):
            calls.append(url)
            return (
                b"<html><title>Just a moment</title><p>Verify you are human</p></html>",
                "utf-8",
            )

        with tempfile.TemporaryDirectory() as folder:
            for _ in range(2):
                state = collect(
                    urls,
                    Path(folder),
                    {"example.org"},
                    fetch=fetch,
                    sleep=lambda _: None,
                )
                self.assertFalse(state["sources"])
                self.assertEqual(state["blocked_hosts"], ["example.org"])
                self.assertEqual(state["failures"][urls[0]]["type"], "AccessBlocked")
            self.assertEqual(calls, [urls[0]])

    def test_challenge_titles_are_distinct_from_an_article_discussing_verification(
        self,
    ):
        for title in (
            "CAPTCHA",
            "Access denied",
            "Just a moment...",
            "Verify you are human",
            "安全验证",
            "访问受限",
        ):
            with self.subTest(title=title), self.assertRaises(AccessBlocked):
                parse_html(
                    f"<html><title>{title}</title><p>challenge</p></html>".encode()
                )
        self.assertIn(
            "Verify you are human",
            parse_html(
                b"<title>How verification works</title><p>Verify you are human</p>"
            ),
        )

    def test_archive_resume_and_domain_stop_do_not_repeat_requests(self):
        urls = [
            "https://example.org/one",
            "https://example.org/two",
            "https://other.example/three",
        ]
        calls = []

        def fetch(url, _):
            calls.append(url)
            if "example.org" in url:
                raise AccessBlocked("HTTP 403")
            return "<p>合成来源原句</p>".encode(), "utf-8"

        with tempfile.TemporaryDirectory() as folder:
            state = collect(
                urls,
                Path(folder),
                {"example.org", "other.example"},
                fetch=fetch,
                sleep=lambda _: None,
            )
            self.assertEqual(len(calls), 2)
            self.assertEqual(len(state["sources"]), 1)
            collect(
                urls,
                Path(folder),
                {"example.org", "other.example"},
                fetch=fetch,
                sleep=lambda _: None,
            )
            self.assertEqual(len(calls), 2)

    def test_text_rules_keep_mentions_requests_and_explanations_separate(self):
        texts = parse_html(
            "<nav>广告</nav><p>求这个表情包素材</p><p>合成梗这个梗的意思是示例说明。</p><p>合成梗用于测试</p>".encode()
        )
        item = {
            "source_id": "web:fixture",
            "url": "https://example.org",
            "texts": [
                {"text": text, "locator": f"/texts/{i}/text"}
                for i, text in enumerate(texts)
            ],
        }
        with tempfile.TemporaryDirectory() as folder:
            artifact = Path(folder) / "source.json"
            artifact.write_text(json.dumps(item, ensure_ascii=False), encoding="utf-8")
            item["text_evidence"] = {
                "path": artifact.name,
                "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
            }
            result = analyze(
                [item, item],
                [
                    {
                        "id": "synthetic",
                        "name": "合成梗",
                        "use_pattern": "合成梗用于测试",
                    }
                ],
                Path(folder),
            )
            artifact.write_text("{}", encoding="utf-8")
            invalid = analyze(
                [item],
                [
                    {
                        "id": "synthetic",
                        "name": "合成梗",
                        "use_pattern": "合成梗用于测试",
                    }
                ],
                Path(folder),
            )
            self.assertEqual(invalid["metrics"]["V_observed_use"], 0)
            self.assertTrue(invalid["invalid"])
        self.assertEqual(result["metrics"]["V_observed_use"], 1)
        self.assertEqual(result["metrics"]["Q_request_sentences"], 1)
        self.assertEqual(result["metrics"]["M_new_memes"], 0)
        self.assertEqual(result["definitions"][0]["definition_excerpt"], "示例说明")
        self.assertEqual(len(result["mentions"]), 1)
        self.assertFalse(result["public_import_authorized"])
        self.assertNotIn("广告", texts)


if __name__ == "__main__":
    unittest.main()
