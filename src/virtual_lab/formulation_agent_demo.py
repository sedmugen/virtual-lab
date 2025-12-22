# src/virtual_lab/formulation_agent_demo.py

import os
import sys
from dotenv import load_dotenv

# Add the project root to sys.path explicitly for standalone execution
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

# Load environment variables from .env file
load_dotenv()

# Import the tools using a relative import from the current directory (src/virtual_lab/)
from .tools.formulation import search_bioprinting_params, suggest_hydrogel

# Define a simplified Agent class locally to avoid any dependencies on the main package's import structure
class Agent:
    def __init__(self, title: str, expertise: str, goal: str, role: str, model: str) -> None:
        self.title = title
        self.expertise = expertise
        self.goal = goal
        self.role = role
        self.model = model

    @property
    def prompt(self) -> str:
        return (
            f"You are a {self.title}. "
            f"Your expertise is in {self.expertise}. "
            f"Your goal is to {self.goal}. "
            f"Your role is to {self.role}."
        )

# Mocking an LLM interaction for the purpose of this demo
# In the full system, this would use the OpenAI API and function calling.
class FormulationAgentDemo:
    def __init__(self):
        # Define the persona using the existing Agent class structure
        self.agent_persona = Agent(
            title="Formulation Scientist",
            expertise="Polymer chemistry, hydrogels, and 3D bioprinting",
            goal="Design a feasible delivery system for nanobodies",
            role="Recommend hydrogels and define printing parameters",
            model="gpt-4o"
        )
        print(f"Initialized Agent: {self.agent_persona.title}")
        print(f"Context: {self.agent_persona.prompt}\n")

    def run_task(self, user_query):
        print(f"--- Receiving Query: '{user_query}' ---")
        
        # Simple keyword-based intent classification for this demo
        # (Replacing full LLM function calling for speed/reliability in this test)
        response = ""
        
        if "print" in user_query.lower() or "parameter" in user_query.lower():
            # Extract material name (mock extraction)
            materials = ["Alginate", "GelMA", "PEG-DA", "Collagen"]
            target_material = next((m for m in materials if m.lower() in user_query.lower()), None)
            
            if target_material:
                print(f"[Agent Decision]: User is asking about bioprinting {target_material}. invoking tool 'search_bioprinting_params'வுகளை...")
                tool_output = search_bioprinting_params(target_material)
                response = f"Based on the Data Lake, here is the protocol for {target_material}:\n{tool_output}"
            else:
                response = "I can help with bioprinting, but I need to know which material (Alginate, GelMA, etc.) you are interested in."
                
        elif "suggest" in user_query.lower() or "find" in user_query.lower():
            # Extract application
            print(f"[Agent Decision]: User is asking for a hydrogel suggestion. invoking tool 'suggest_hydrogel'...")
            tool_output = suggest_hydrogel("tissue engineering") # Defaulting to tissue engineering for demo
            response = f"Here are some hydrogels from our database suitable for tissue engineering:\n{tool_output}"
            
        else:
            response = "I am the Formulation Specialist. I can help you select hydrogels or find bioprinting parameters."
            
        print(f"\n[Agent Response]:\n{response}")

if __name__ == "__main__":
    # Load env (though not strictly needed for this mock demo, good practice)
    load_dotenv()
    
    # Instantiate the agent
    specialist = FormulationAgentDemo()
    
    # Run Scenario 1: Bioprinting Query
    specialist.run_task("What are the printing parameters for Alginate?")
    
    print("-" * 30)
    
    # Run Scenario 2: Discovery Query
    specialist.run_task("Can you suggest a hydrogel for tissue engineering?")
