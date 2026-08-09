"""Standalone demo of the Formulation Scientist agent querying the Data Lake.

This script demonstrates how a Virtual Lab agent can use tool functions
backed by the ``src/data_integration`` Data Lake to:

1. Look up 3D bioprinting parameters for a target material.
2. Suggest a hydrogel suitable for a given tissue-engineering application.

Run directly::

    python -m src.virtual_lab.formulation_agent_demo

The Data Lake must be populated first::

    python -m src.data_integration.main
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import tools from the tools sub-package
from .tools.formulation import search_bioprinting_params, suggest_hydrogel

# Import the canonical Agent class
from .agent import Agent


class FormulationAgentDemo:
    """Mock demonstration of a Formulation Scientist agent.

    In the full system the agent would use the OpenAI function-calling API.
    Here, intent is classified with simple keyword matching so the demo
    runs without any API key.
    """

    def __init__(self) -> None:
        self.agent_persona = Agent(
            title="Formulation Scientist",
            expertise="Polymer chemistry, hydrogels, and 3D bioprinting",
            goal="Design a feasible delivery system for nanobodies",
            role="Recommend hydrogels and define printing parameters",
            model="gpt-4o",
        )
        print(f"Initialized Agent: {self.agent_persona.title}")
        print(f"Context: {self.agent_persona.prompt}\n")

    def run_task(self, user_query: str) -> None:
        """Classify the query and invoke the appropriate Data Lake tool.

        :param user_query: Natural-language question from the researcher.
        """
        print(f"--- Receiving Query: '{user_query}' ---")

        response = ""

        if "print" in user_query.lower() or "parameter" in user_query.lower():
            # Extract a known material name from the query
            materials = ["Alginate", "GelMA", "PEG-DA", "Collagen"]
            target_material = next(
                (m for m in materials if m.lower() in user_query.lower()), None
            )

            if target_material:
                print(
                    f"[Agent Decision]: User is asking about bioprinting "
                    f"{target_material}. Invoking tool 'search_bioprinting_params'..."
                )
                tool_output = search_bioprinting_params(target_material)
                response = (
                    f"Based on the Data Lake, here is the protocol for "
                    f"{target_material}:\n{tool_output}"
                )
            else:
                response = (
                    "I can help with bioprinting, but I need to know which material "
                    "(Alginate, GelMA, etc.) you are interested in."
                )

        elif "suggest" in user_query.lower() or "find" in user_query.lower():
            print(
                "[Agent Decision]: User is asking for a hydrogel suggestion. "
                "Invoking tool 'suggest_hydrogel'..."
            )
            tool_output = suggest_hydrogel("tissue engineering")
            response = (
                "Here are some hydrogels from our database suitable for tissue "
                f"engineering:\n{tool_output}"
            )

        else:
            response = (
                "I am the Formulation Specialist. I can help you select hydrogels "
                "or find bioprinting parameters."
            )

        print(f"\n[Agent Response]:\n{response}")


if __name__ == "__main__":
    specialist = FormulationAgentDemo()

    specialist.run_task("What are the printing parameters for Alginate?")

    print("-" * 30)

    specialist.run_task("Can you suggest a hydrogel for tissue engineering?")
