"""Unit tests for prompt formatting functions."""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from virtual_lab.agent import Agent
from virtual_lab.prompts import (
    PRINCIPAL_INVESTIGATOR,
    format_agenda,
    format_agenda_questions,
    format_agenda_rules,
    team_meeting_start_prompt,
)


class TestPrompts(unittest.TestCase):
    def test_format_agenda(self) -> None:
        result = format_agenda("Analyze SARS-CoV-2 spike protein.")
        self.assertIn("Agenda:\nAnalyze SARS-CoV-2 spike protein.", result)

    def test_format_agenda_questions(self) -> None:
        questions = ("What is the affinity?", "Is it stable?")
        result = format_agenda_questions(questions)
        self.assertIn("Agenda Questions:", result)
        self.assertIn("1. What is the affinity?", result)
        self.assertIn("2. Is it stable?", result)

    def test_format_agenda_rules(self) -> None:
        rules = ("Be concise.", "Cite literature.")
        result = format_agenda_rules(rules)
        self.assertIn("Agenda Rules:", result)
        self.assertIn("1. Be concise.", result)

    def test_team_meeting_start_prompt(self) -> None:
        lead = PRINCIPAL_INVESTIGATOR
        member = Agent("Biologist", "genomics", "analyze data", "report findings", "gpt-4o")
        prompt = team_meeting_start_prompt(
            team_lead=lead,
            team_members=(member,),
            agenda="Design vaccine candidate.",
        )
        self.assertIn("beginning of a team meeting", prompt)
        self.assertIn("Principal Investigator", prompt)
        self.assertIn("Biologist", prompt)


if __name__ == "__main__":
    unittest.main()
