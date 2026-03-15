from __future__ import annotations

import unittest

from ifoundyou.core import normalize_target


class NormalizeTargetTests(unittest.TestCase):
    def test_detects_domain(self) -> None:
        result = normalize_target("example.com")
        self.assertEqual(result["host"], "example.com")
        self.assertFalse(result["is_ip"])

    def test_detects_url(self) -> None:
        result = normalize_target("https://openai.com/blog")
        self.assertEqual(result["host"], "openai.com")
        self.assertEqual(result["scheme"], "https")

    def test_detects_ip(self) -> None:
        result = normalize_target("8.8.8.8")
        self.assertTrue(result["is_ip"])


if __name__ == "__main__":
    unittest.main()

