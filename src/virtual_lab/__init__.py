"""Virtual Lab package."""

from virtual_lab.__about__ import __version__
from virtual_lab.agent import Agent
from virtual_lab.run_meeting import run_meeting

# Specialized agents
from virtual_lab.agents import (
    SpecializedAgent,
    InteractionStyle,
    ValidationBenchmarkingAgent,
    VALIDATION_BENCHMARKING_AGENT,
)


__all__ = [
    "__version__",
    "Agent",
    "run_meeting",
    # Specialized agents
    "SpecializedAgent",
    "InteractionStyle",
    "ValidationBenchmarkingAgent",
    "VALIDATION_BENCHMARKING_AGENT",
]
