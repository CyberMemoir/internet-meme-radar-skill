from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from trend_score import calculate, label  # noqa: E402


class TrendScoreTests(unittest.TestCase):
    def test_weighted_score(self):
        signals = {
            "recency": 100,
            "repetition": 80,
            "creator_spread": 60,
            "comment_adoption": 40,
            "remix_potential": 20,
            "platform_spread": 0,
        }
        self.assertEqual(calculate(signals), 63.0)

    def test_boundaries(self):
        self.assertEqual(label(20), "insufficient-or-not-a-meme")
        self.assertEqual(label(40), "niche-or-weak")
        self.assertEqual(label(60), "real-but-limited")
        self.assertEqual(label(80), "strong-platform-trend")
        self.assertEqual(label(80.1), "major-cross-platform-trend")

    def test_rejects_out_of_range_values(self):
        signals = {name: 50 for name in (
            "recency", "repetition", "creator_spread", "comment_adoption",
            "remix_potential", "platform_spread"
        )}
        signals["recency"] = 101
        with self.assertRaises(ValueError):
            calculate(signals)


if __name__ == "__main__":
    unittest.main()
