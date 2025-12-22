"""Base class for specialized agents in the virtual lab framework.

This module provides an extended Agent class that supports:
- Specialized tools and capabilities
- Defined responsibilities and interaction styles
- Domain-specific prompt generation
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

from virtual_lab.agent import Agent
from virtual_lab.constants import DEFAULT_MODEL

if TYPE_CHECKING:
    from virtual_lab.agents.tools.base import Tool


class InteractionStyle(Enum):
    """Defines how an agent interacts with other agents."""

    COLLABORATIVE = "collaborative"
    SKEPTICAL = "skeptical"
    SUPPORTIVE = "supportive"
    ANALYTICAL = "analytical"
    DIRECTIVE = "directive"


@dataclass
class SpecializedAgent:
    """A specialized agent with extended capabilities.

    This class extends the base Agent concept with:
    - Defined responsibilities
    - Associated tools
    - Interaction style
    - Domain-specific prompts

    Attributes:
        name: The name/identifier of the agent.
        title: The formal title of the agent.
        expertise: The agent's area of expertise.
        goal: The agent's primary goal.
        role: The agent's role in the team.
        responsibilities: List of specific responsibilities.
        tools: List of tools the agent can use.
        interaction_style: How the agent interacts with others.
        system_prompt: Optional custom system prompt override.
        model: The LLM model to use.
    """

    name: str
    title: str
    expertise: str
    goal: str
    role: str
    responsibilities: list[str] = field(default_factory=list)
    tools: list["Tool"] = field(default_factory=list)
    interaction_style: InteractionStyle = InteractionStyle.COLLABORATIVE
    system_prompt: str | None = None
    model: str = DEFAULT_MODEL

    def __post_init__(self) -> None:
        """Validate the agent configuration after initialization."""
        if not self.name:
            raise ValueError("Agent name cannot be empty")
        if not self.title:
            raise ValueError("Agent title cannot be empty")

    @property
    def prompt(self) -> str:
        """Generate the full system prompt for this agent.

        Returns:
            The complete system prompt including role, responsibilities,
            tools, and interaction style.
        """
        if self.system_prompt:
            return self.system_prompt

        sections = [
            f"You are a {self.title}.",
            f"Your expertise is in {self.expertise}.",
            f"Your goal is to {self.goal}.",
            f"Your role is to {self.role}.",
        ]

        if self.responsibilities:
            responsibilities_text = "\n".join(
                f"- {resp}" for resp in self.responsibilities
            )
            sections.append(f"\nYour responsibilities include:\n{responsibilities_text}")

        if self.tools:
            tools_text = "\n".join(f"- {tool.name}: {tool.description}" for tool in self.tools)
            sections.append(f"\nYou have access to the following tools:\n{tools_text}")

        interaction_descriptions = {
            InteractionStyle.SKEPTICAL: (
                "\nYour interaction style is skeptical and rigorous. "
                "Challenge claims from other agents, demand evidence, "
                "and ensure all assertions are well-supported."
            ),
            InteractionStyle.COLLABORATIVE: (
                "\nYour interaction style is collaborative. "
                "Work constructively with other agents to achieve shared goals."
            ),
            InteractionStyle.SUPPORTIVE: (
                "\nYour interaction style is supportive. "
                "Help other agents succeed and provide constructive feedback."
            ),
            InteractionStyle.ANALYTICAL: (
                "\nYour interaction style is analytical. "
                "Focus on data-driven insights and systematic analysis."
            ),
            InteractionStyle.DIRECTIVE: (
                "\nYour interaction style is directive. "
                "Provide clear guidance and make decisive recommendations."
            ),
        }
        sections.append(interaction_descriptions[self.interaction_style])

        return " ".join(sections[:4]) + "".join(sections[4:])

    @property
    def message(self) -> dict[str, str]:
        """Returns the message for the agent in OpenAI API form.

        Returns:
            A dictionary with 'role' and 'content' keys.
        """
        return {
            "role": "system",
            "content": self.prompt,
        }

    def to_base_agent(self) -> Agent:
        """Convert to a base Agent instance for compatibility.

        Returns:
            A base Agent instance with the core properties.
        """
        return Agent(
            title=self.title,
            expertise=self.expertise,
            goal=self.goal,
            role=self.role,
            model=self.model,
        )

    def get_tool(self, tool_name: str) -> "Tool | None":
        """Get a tool by name.

        Args:
            tool_name: The name of the tool to retrieve.

        Returns:
            The tool if found, None otherwise.
        """
        for tool in self.tools:
            if tool.name == tool_name:
                return tool
        return None

    def add_tool(self, tool: "Tool") -> None:
        """Add a tool to this agent.

        Args:
            tool: The tool to add.
        """
        if tool not in self.tools:
            self.tools.append(tool)

    def remove_tool(self, tool_name: str) -> bool:
        """Remove a tool by name.

        Args:
            tool_name: The name of the tool to remove.

        Returns:
            True if the tool was removed, False if not found.
        """
        for i, tool in enumerate(self.tools):
            if tool.name == tool_name:
                self.tools.pop(i)
                return True
        return False

    def __hash__(self) -> int:
        """Returns the hash of the agent based on name."""
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        """Check equality based on name."""
        if not isinstance(other, SpecializedAgent):
            return False
        return self.name == other.name

    def __str__(self) -> str:
        """Returns the string representation (title)."""
        return self.title

    def __repr__(self) -> str:
        """Returns a detailed representation."""
        return f"SpecializedAgent(name='{self.name}', title='{self.title}')"
