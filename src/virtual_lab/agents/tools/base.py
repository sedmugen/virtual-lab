"""Base tool interface for specialized agents.

This module defines the abstract interface for tools that agents can use,
along with a registry for managing available tools.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Tool(ABC):
    """Abstract base class for agent tools.

    Tools provide agents with access to external data sources,
    computational resources, or analytical capabilities.

    Attributes:
        name: The unique identifier for this tool.
        description: A human-readable description of what the tool does.
        version: The version of the tool.
        enabled: Whether the tool is currently enabled.
    """

    name: str
    description: str
    version: str = "1.0.0"
    enabled: bool = True

    @abstractmethod
    def execute(self, **kwargs: Any) -> dict[str, Any]:
        """Execute the tool with the given parameters.

        Args:
            **kwargs: Tool-specific parameters.

        Returns:
            A dictionary containing the tool's output.
        """
        pass

    @abstractmethod
    def validate_params(self, **kwargs: Any) -> bool:
        """Validate the input parameters before execution.

        Args:
            **kwargs: Parameters to validate.

        Returns:
            True if parameters are valid, False otherwise.
        """
        pass

    def get_schema(self) -> dict[str, Any]:
        """Get the JSON schema for this tool's parameters.

        Returns:
            A JSON schema dictionary describing the tool's parameters.
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {},
        }

    def __hash__(self) -> int:
        """Hash based on tool name."""
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        """Equality based on tool name."""
        if not isinstance(other, Tool):
            return False
        return self.name == other.name


class ToolRegistry:
    """Registry for managing available tools.

    Provides centralized access to tools and allows dynamic
    registration and retrieval.
    """

    _instance: "ToolRegistry | None" = None
    _tools: dict[str, Tool]

    def __new__(cls) -> "ToolRegistry":
        """Singleton pattern for the registry."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tools = {}
        return cls._instance

    def register(self, tool: Tool) -> None:
        """Register a tool in the registry.

        Args:
            tool: The tool to register.

        Raises:
            ValueError: If a tool with the same name already exists.
        """
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered")
        self._tools[tool.name] = tool

    def unregister(self, tool_name: str) -> bool:
        """Unregister a tool from the registry.

        Args:
            tool_name: The name of the tool to unregister.

        Returns:
            True if the tool was unregistered, False if not found.
        """
        if tool_name in self._tools:
            del self._tools[tool_name]
            return True
        return False

    def get(self, tool_name: str) -> Tool | None:
        """Get a tool by name.

        Args:
            tool_name: The name of the tool to retrieve.

        Returns:
            The tool if found, None otherwise.
        """
        return self._tools.get(tool_name)

    def list_tools(self) -> list[str]:
        """List all registered tool names.

        Returns:
            A list of registered tool names.
        """
        return list(self._tools.keys())

    def get_tools_by_category(self, category: str) -> list[Tool]:
        """Get all tools in a specific category.

        Args:
            category: The category to filter by.

        Returns:
            A list of tools in the specified category.
        """
        return [
            tool for tool in self._tools.values()
            if hasattr(tool, "category") and tool.category == category
        ]

    def clear(self) -> None:
        """Clear all registered tools."""
        self._tools.clear()

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton instance (useful for testing)."""
        cls._instance = None
