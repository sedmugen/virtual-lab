"""Unit tests for utility functions."""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from virtual_lab.utils import (
    count_tokens,
    compute_token_cost,
    convert_messages_to_discussion,
    get_summary,
)


class TestUtils(unittest.TestCase):
    def test_count_tokens(self) -> None:
        tokens = count_tokens("Hello world")
        self.assertGreater(tokens, 0)

    def test_compute_token_cost(self) -> None:
        cost = compute_token_cost("gpt-4o", input_token_count=1000, output_token_count=1000)
        self.assertGreater(cost, 0.0)

        cost_unknown = compute_token_cost("unknown-model", 1000, 1000)
        self.assertEqual(cost_unknown, 0.0)

    def test_convert_messages_to_discussion(self) -> None:
        messages = [
            {"assistant_id": "ast_1", "content": [{"text": {"value": "Hello team"}}]},
            {"assistant_id": None, "content": [{"text": {"value": "User response"}}]},
        ]
        id_map = {"ast_1": "Principal Investigator"}

        discussion = convert_messages_to_discussion(messages, id_map)
        self.assertEqual(len(discussion), 2)
        self.assertEqual(discussion[0]["agent"], "Principal Investigator")
        self.assertEqual(discussion[0]["message"], "Hello team")
        self.assertEqual(discussion[1]["agent"], "User")
        self.assertEqual(discussion[1]["message"], "User response")

    def test_get_summary(self) -> None:
        discussion = [
            {"agent": "PI", "message": "Opening"},
            {"agent": "PI", "message": "Final Summary Statement"},
        ]
        summary = get_summary(discussion)
        self.assertEqual(summary, "Final Summary Statement")


if __name__ == "__main__":
    unittest.main()
