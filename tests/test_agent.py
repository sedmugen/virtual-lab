"""Unit tests for Agent dataclass."""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from virtual_lab.agent import Agent


class TestAgent(unittest.TestCase):
    def test_agent_initialization(self) -> None:
        agent = Agent(
            title="Immunologist",
            expertise="antibody engineering",
            goal="design binders",
            role="advise team",
            model="gpt-4o",
        )
        self.assertEqual(agent.title, "Immunologist")
        self.assertEqual(agent.expertise, "antibody engineering")
        self.assertEqual(agent.goal, "design binders")
        self.assertEqual(agent.role, "advise team")
        self.assertEqual(agent.model, "gpt-4o")

    def test_agent_prompt_property(self) -> None:
        agent = Agent(
            title="Chemist",
            expertise="small molecules",
            goal="optimize solubility",
            role="formulate compounds",
            model="gpt-4o",
        )
        expected_prompt = (
            "You are a Chemist. "
            "Your expertise is in small molecules. "
            "Your goal is to optimize solubility. "
            "Your role is to formulate compounds."
        )
        self.assertEqual(agent.prompt, expected_prompt)

    def test_agent_message_property(self) -> None:
        agent = Agent(
            title="Chemist",
            expertise="small molecules",
            goal="optimize solubility",
            role="formulate compounds",
            model="gpt-4o",
        )
        msg = agent.message
        self.assertEqual(msg["role"], "system")
        self.assertIn("You are a Chemist.", msg["content"])

    def test_agent_equality_and_hash(self) -> None:
        agent1 = Agent("A", "B", "C", "D", "gpt-4o")
        agent2 = Agent("A", "B", "C", "D", "gpt-4o")
        agent3 = Agent("X", "B", "C", "D", "gpt-4o")

        self.assertEqual(agent1, agent2)
        self.assertNotEqual(agent1, agent3)
        self.assertEqual(hash(agent1), hash(agent2))
        self.assertEqual(str(agent1), "A")
        self.assertEqual(repr(agent1), "A")


if __name__ == "__main__":
    unittest.main()
