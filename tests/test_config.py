"""Unit tests for config module."""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from virtual_lab.config import get_config


class TestConfig(unittest.TestCase):
    def test_config_exports(self) -> None:
        key, url, model = get_config()
        self.assertIsInstance(key, str)
        self.assertIn(model, ["gpt-4o", "glm-4-flash"])


if __name__ == "__main__":
    unittest.main()
