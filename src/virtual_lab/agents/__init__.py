"""Specialized agents module for the virtual lab framework.

This module provides modular, domain-specific agents that extend the base
Agent class with specialized capabilities, tools, and interaction patterns.
"""

from virtual_lab.agents.base import SpecializedAgent, InteractionStyle
from virtual_lab.agents.validation_benchmarking import (
    ValidationBenchmarkingAgent,
    VALIDATION_BENCHMARKING_AGENT,
)

__all__ = [
    "SpecializedAgent",
    "InteractionStyle",
    "ValidationBenchmarkingAgent",
    "VALIDATION_BENCHMARKING_AGENT",
]
