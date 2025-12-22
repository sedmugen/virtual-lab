# Agents Module Documentation

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Module Structure](#module-structure)
4. [Core Components](#core-components)
   - [Base Classes](#base-classes)
   - [Tool System](#tool-system)
   - [Validation & Benchmarking Agent](#validation--benchmarking-agent)
5. [Design Patterns & Decisions](#design-patterns--decisions)
6. [Usage Guide](#usage-guide)
7. [Extending the Framework](#extending-the-framework)
8. [Integration with Virtual Lab](#integration-with-virtual-lab)
9. [API Reference](#api-reference)

---

## Overview

The **Agents Module** extends the Virtual Lab framework with specialized, domain-specific agents that go beyond the basic `Agent` class. While the original `Agent` class is a simple data container with four properties (title, expertise, goal, role), the agents module introduces:

- **Specialized Agents**: Extended agents with tools, responsibilities, and interaction styles
- **Tool System**: A modular framework for integrating external data sources and analysis capabilities
- **Domain Knowledge**: Pre-configured QC assays, developmental benchmarks, and validation protocols

### Why This Module Exists

The original Virtual Lab framework was designed for general-purpose AI-human collaboration in scientific research. The agents module addresses the need for:

1. **Domain Specificity**: Agents with deep knowledge in specific scientific domains
2. **Tool Integration**: Structured access to databases, APIs, and analysis tools
3. **Behavioral Patterns**: Defined interaction styles (skeptical, collaborative, etc.)
4. **Validation Protocols**: Pre-defined quality control workflows

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Virtual Lab Framework                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐     ┌─────────────────────────────────────────┐   │
│  │    Agent     │     │            Agents Module                 │   │
│  │   (base)     │     │                                         │   │
│  │              │     │  ┌─────────────────────────────────┐    │   │
│  │ - title      │     │  │      SpecializedAgent           │    │   │
│  │ - expertise  │◄────┼──│                                 │    │   │
│  │ - goal       │     │  │  - name, title, expertise       │    │   │
│  │ - role       │     │  │  - goal, role                   │    │   │
│  │ - model      │     │  │  - responsibilities: list       │    │   │
│  │              │     │  │  - tools: list[Tool]            │    │   │
│  │ + prompt     │     │  │  - interaction_style: Enum      │    │   │
│  │ + message    │     │  │  - system_prompt: str           │    │   │
│  │              │     │  │                                 │    │   │
│  └──────────────┘     │  │  + to_base_agent()              │    │   │
│                       │  │  + get_tool()                   │    │   │
│                       │  │  + add_tool() / remove_tool()   │    │   │
│                       │  └─────────────────────────────────┘    │   │
│                       │                    │                     │   │
│                       │                    ▼                     │   │
│                       │  ┌─────────────────────────────────┐    │   │
│                       │  │  ValidationBenchmarkingAgent    │    │   │
│                       │  │                                 │    │   │
│                       │  │  - qc_assays: list[QCAssay]     │    │   │
│                       │  │  - benchmarks: list[Benchmark]  │    │   │
│                       │  │  - off_target_signatures: dict  │    │   │
│                       │  │                                 │    │   │
│                       │  │  + get_assays_for_timepoint()   │    │   │
│                       │  │  + check_off_target_fates()     │    │   │
│                       │  │  + generate_validation_protocol()│   │   │
│                       │  │  + evaluate_scrnaseq_alignment()│    │   │
│                       │  └─────────────────────────────────┘    │   │
│                       │                                         │   │
│                       │  ┌─────────────────────────────────┐    │   │
│                       │  │          Tools Module           │    │   │
│                       │  │                                 │    │   │
│                       │  │  Tool (ABC)                     │    │   │
│                       │  │  ├── BrainSpanTool              │    │   │
│                       │  │  ├── FetalScRNASeqTool          │    │   │
│                       │  │  ├── OrganoidBenchmarkTool      │    │   │
│                       │  │  ├── ProteomicsTool             │    │   │
│                       │  │  └── PathwayActivityTool        │    │   │
│                       │  │                                 │    │   │
│                       │  │  ToolRegistry (Singleton)       │    │   │
│                       │  └─────────────────────────────────┘    │   │
│                       └─────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                      run_meeting()                            │   │
│  │  Orchestrates team/individual meetings using OpenAI API      │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
User Request
     │
     ▼
┌─────────────────┐
│ SpecializedAgent │
│                  │
│  1. Parse request│
│  2. Select tools │
│  3. Generate     │
│     response     │
└────────┬─────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│   Tool Layer    │────▶│ External Data   │
│                 │     │ - BrainSpan     │
│ - execute()     │     │ - scRNA-seq DBs │
│ - validate()    │     │ - Benchmarks    │
└─────────────────┘     └─────────────────┘
         │
         ▼
┌─────────────────┐
│  Response with  │
│  evidence-based │
│  validation     │
└─────────────────┘
```

---

## Module Structure

```
src/virtual_lab/agents/
│
├── __init__.py                    # Package exports
│   Exports: SpecializedAgent, InteractionStyle,
│            ValidationBenchmarkingAgent, VALIDATION_BENCHMARKING_AGENT
│
├── base.py                        # Base classes for specialized agents
│   Classes: InteractionStyle (Enum), SpecializedAgent (dataclass)
│
├── validation_benchmarking.py     # The Validation & Benchmarking Agent
│   Classes: QCAssay, DevelopmentalBenchmark, ValidationBenchmarkingAgent
│   Constants: VALIDATION_BENCHMARKING_AGENT
│
├── agent.md                       # This documentation file
│
└── tools/                         # Tool subsystem
    │
    ├── __init__.py                # Tool exports
    │   Exports: Tool, ToolRegistry, BrainSpanTool, FetalScRNASeqTool,
    │            OrganoidBenchmarkTool, ProteomicsTool, PathwayActivityTool
    │
    ├── base.py                    # Abstract tool interface
    │   Classes: Tool (ABC), ToolRegistry (Singleton)
    │
    └── benchmarking_tools.py      # Concrete tool implementations
        Classes: BrainSpanTool, FetalScRNASeqTool, OrganoidBenchmarkTool,
                 ProteomicsTool, PathwayActivityTool
```

---

## Core Components

### Base Classes

#### InteractionStyle (Enum)

Defines how an agent interacts with other agents in team meetings.

```python
from enum import Enum

class InteractionStyle(Enum):
    COLLABORATIVE = "collaborative"  # Works constructively with others
    SKEPTICAL = "skeptical"          # Challenges claims, demands evidence
    SUPPORTIVE = "supportive"        # Helps others succeed
    ANALYTICAL = "analytical"        # Focuses on data-driven insights
    DIRECTIVE = "directive"          # Provides clear guidance
```

**Why use an Enum?**
- Type safety: Prevents typos like `"skepticl"` vs `"skeptical"`
- IDE support: Autocomplete and validation
- Documentation: Self-documenting code
- Extensibility: Easy to add new styles

**How it affects behavior:**
The interaction style is included in the agent's system prompt, influencing how the LLM behaves during meetings:

```python
# In SpecializedAgent.prompt property:
interaction_descriptions = {
    InteractionStyle.SKEPTICAL: (
        "Your interaction style is skeptical and rigorous. "
        "Challenge claims from other agents, demand evidence, "
        "and ensure all assertions are well-supported."
    ),
    # ... other styles
}
```

#### SpecializedAgent (Dataclass)

A `dataclass` that extends the concept of the basic `Agent` with additional capabilities.

```python
@dataclass
class SpecializedAgent:
    # Identity
    name: str                                    # Unique identifier
    title: str                                   # Display name
    expertise: str                               # Area of knowledge
    goal: str                                    # Primary objective
    role: str                                    # Role in team

    # Extended capabilities
    responsibilities: list[str]                  # Specific duties
    tools: list[Tool]                            # Available tools
    interaction_style: InteractionStyle          # Behavior pattern
    system_prompt: str | None                    # Custom prompt override
    model: str                                   # LLM model to use
```

**Key Methods:**

| Method | Description |
|--------|-------------|
| `prompt` | Property that generates the full system prompt |
| `message` | Returns OpenAI API format `{"role": "system", "content": ...}` |
| `to_base_agent()` | Converts to base `Agent` for compatibility |
| `get_tool(name)` | Retrieves a tool by name |
| `add_tool(tool)` | Adds a new tool |
| `remove_tool(name)` | Removes a tool by name |

**Why a dataclass?**
- Automatic `__init__`, `__repr__`, `__eq__` generation
- Clean, declarative syntax
- Default values with `field(default_factory=...)`
- Type hints are first-class citizens

---

### Tool System

#### Tool (Abstract Base Class)

All tools inherit from this abstract class, ensuring a consistent interface.

```python
@dataclass
class Tool(ABC):
    name: str           # Unique identifier (e.g., "brainspan")
    description: str    # Human-readable description
    version: str        # Semantic version
    enabled: bool       # Whether tool is active

    @abstractmethod
    def execute(self, **kwargs) -> dict[str, Any]:
        """Run the tool with given parameters."""
        pass

    @abstractmethod
    def validate_params(self, **kwargs) -> bool:
        """Check if parameters are valid."""
        pass

    def get_schema(self) -> dict[str, Any]:
        """Return JSON schema for tool parameters."""
        pass
```

**Why Abstract Base Class (ABC)?**
- Enforces interface contract: All tools MUST implement `execute()` and `validate_params()`
- Prevents instantiation of incomplete tools
- Documents expected behavior
- Enables polymorphism: `for tool in agent.tools: tool.execute(...)`

#### ToolRegistry (Singleton)

Centralized registry for managing available tools.

```python
class ToolRegistry:
    _instance: "ToolRegistry | None" = None  # Singleton instance
    _tools: dict[str, Tool]                   # Tool storage

    def __new__(cls) -> "ToolRegistry":
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tools = {}
        return cls._instance
```

**Why Singleton?**
- Global access point for all tools
- Prevents duplicate registrations
- Consistent state across the application
- Easy to test with `reset()` method

**Usage:**
```python
registry = ToolRegistry()
registry.register(BrainSpanTool())
registry.register(FetalScRNASeqTool())

# Later, anywhere in code:
tool = ToolRegistry().get("brainspan")
```

#### Concrete Tools

Five specialized tools for organoid validation:

| Tool | Purpose | Key Data |
|------|---------|----------|
| `BrainSpanTool` | Human brain transcriptome | 14 brain regions, 31 developmental stages |
| `FetalScRNASeqTool` | Fetal brain scRNA-seq | 4 reference datasets, 9 cell types |
| `OrganoidBenchmarkTool` | Reproducibility studies | 4 benchmark studies, 7 quality metrics |
| `ProteomicsTool` | Protein expression data | 6 protein categories |
| `PathwayActivityTool` | Pathway analysis | 8 developmental pathways, 5 databases |

**Example Tool Implementation:**

```python
@dataclass
class BrainSpanTool(Tool):
    name: str = "brainspan"
    description: str = "Access BrainSpan human brain transcriptome data..."
    category: str = "reference_datasets"

    # Tool-specific data
    regions: list[str] = field(default_factory=lambda: [
        "dorsolateral prefrontal cortex",
        "hippocampus",
        # ... 14 regions total
    ])

    stages: list[str] = field(default_factory=lambda: [
        "8 pcw", "9 pcw", "12 pcw",  # Post-conception weeks
        # ... 31 stages from 8 pcw to 40 yrs
    ])

    def execute(self, **kwargs) -> dict[str, Any]:
        genes = kwargs.get("genes", [])
        regions = kwargs.get("regions", self.regions)
        stages = kwargs.get("stages", self.stages)

        return {
            "status": "success",
            "tool": self.name,
            "query": {"genes": genes, "regions": regions, "stages": stages},
            "data_source": "https://www.brainspan.org/",
        }

    def validate_params(self, **kwargs) -> bool:
        if "genes" in kwargs and not isinstance(kwargs["genes"], list):
            return False
        return True
```

---

### Validation & Benchmarking Agent

The main agent implementation, designed for rigorous quality control of organoid protocols.

#### QCAssay (Dataclass)

Represents a quality control assay with expected outcomes.

```python
@dataclass
class QCAssay:
    name: str                      # "Neural Induction Verification"
    description: str               # What the assay measures
    timing: str                    # "Day 6-10"
    markers: list[str]             # ["PAX6", "SOX1", "SOX2", "NES"]
    expected_outcomes: list[str]   # [">90% PAX6+ cells", ...]
    failure_indicators: list[str]  # ["Persistent OCT4/NANOG", ...]
```

**Pre-defined Assays:**

| Assay | Timing | Key Markers |
|-------|--------|-------------|
| Neural Induction Verification | Day 6-10 | PAX6, SOX1, SOX2, NES |
| Dorsal Forebrain Identity | Day 15-25 | FOXG1, EMX1, EMX2, LHX2 |
| Progenitor Organization | Day 30-45 | PAX6, SOX2, TBR2/EOMES |
| Neurogenesis Progression | Day 45-90 | TBR1, CTIP2, SATB2, CUX1 |
| Outer Radial Glia Assessment | Day 60-120 | HOPX, FAM107A, PTPRZ1 |
| Functional Maturation | Day 90-180 | Synaptic proteins, activity |
| Gliogenesis Assessment | Day 120-180+ | GFAP, S100B, OLIG2 |

#### DevelopmentalBenchmark (Dataclass)

Reference data from human fetal brain development.

```python
@dataclass
class DevelopmentalBenchmark:
    name: str                              # "Peak Neurogenesis"
    stage: str                             # "GW14-18" (gestational weeks)
    cell_types: list[str]                  # Expected cell populations
    marker_genes: dict[str, list[str]]     # Cell type -> marker genes
    transcriptomic_signature: list[str]    # Pathway activity patterns
    reference_dataset: str                 # Source publication
```

**Pre-defined Benchmarks:**

| Stage | Name | Reference |
|-------|------|-----------|
| GW8-10 | Early Cortical Plate | Nowakowski 2017 |
| GW14-18 | Peak Neurogenesis | Polioudakis 2019 |
| GW20-26 | Late Neurogenesis | Trevino 2021 |

#### ValidationBenchmarkingAgent

The main agent class combining all components.

```python
@dataclass
class ValidationBenchmarkingAgent(SpecializedAgent):
    # Pre-configured identity
    name: str = "validation_benchmarking"
    title: str = "Validation and Benchmarking Specialist"
    interaction_style: InteractionStyle = InteractionStyle.SKEPTICAL

    # Domain-specific data
    qc_assays: list[QCAssay]
    benchmarks: list[DevelopmentalBenchmark]
    off_target_signatures: dict[str, list[str]]
```

**Key Methods:**

```python
# Get QC assays for a specific culture day
assays = agent.get_assays_for_timepoint(60)
# Returns: [Neurogenesis Progression, Outer Radial Glia Assessment]

# Check for off-target differentiation
issues = agent.check_off_target_fates(["NKX2.1", "PAX6", "ATF4"])
# Returns: {"ventral_forebrain": ["NKX2.1"], "stressed_cells": ["ATF4"]}

# Generate complete validation protocol
protocol = agent.generate_validation_protocol(
    timepoints=[10, 25, 45, 60, 90, 120]
)

# Compare organoid to fetal reference
alignment = agent.evaluate_scrnaseq_alignment(
    organoid_cell_types={"radial glia": 0.3, "neurons": 0.5, ...},
    reference_stage="GW14-18"
)
```

**Off-Target Signatures:**

The agent monitors for 9 types of unwanted differentiation:

| Fate | Marker Genes |
|------|--------------|
| Ventral Forebrain | NKX2.1, LHX6, DLX5, GSX2 |
| Midbrain | EN1, EN2, PAX5, OTX2_high |
| Hindbrain | GBX2, HOXA2, HOXB2, ATOH1 |
| Spinal Cord | HOXC6, HOXC8, HOXC9, PAX3 |
| Mesoderm | TBXT, MEOX1, TBX6, MSGN1 |
| Endoderm | SOX17, FOXA2, GATA4, GATA6 |
| Neural Crest | SOX10, TFAP2A, PAX3, SNAI2 |
| Stressed Cells | ATF4, DDIT3, HSPA5, XBP1 |
| Glycolytic Stress | HIF1A, LDHA, PDK1, VEGFA |

---

## Design Patterns & Decisions

### 1. Dataclasses Over Regular Classes

**Decision:** Use `@dataclass` decorator for all data-holding classes.

**Rationale:**
- Reduces boilerplate code
- Automatic `__init__`, `__repr__`, `__eq__`, `__hash__`
- Clear, declarative syntax
- Built-in support for default values via `field()`

**Example:**
```python
# Without dataclass (verbose)
class QCAssay:
    def __init__(self, name, description, timing, markers, expected, failures):
        self.name = name
        self.description = description
        self.timing = timing
        self.markers = markers
        self.expected_outcomes = expected
        self.failure_indicators = failures

    def __repr__(self):
        return f"QCAssay(name={self.name!r}, ...)"

    def __eq__(self, other):
        if not isinstance(other, QCAssay):
            return False
        return self.name == other.name and ...

# With dataclass (clean)
@dataclass
class QCAssay:
    name: str
    description: str
    timing: str
    markers: list[str]
    expected_outcomes: list[str]
    failure_indicators: list[str]
```

### 2. Abstract Base Class for Tools

**Decision:** Use ABC for the `Tool` base class.

**Rationale:**
- Enforces implementation of required methods
- Prevents instantiation of incomplete tools
- Enables static type checking
- Documents the expected interface

### 3. Singleton Pattern for ToolRegistry

**Decision:** Implement ToolRegistry as a singleton.

**Rationale:**
- Single source of truth for available tools
- Global access without passing instances
- Prevents duplicate registrations
- Thread-safe initialization (in Python)

**Implementation:**
```python
class ToolRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tools = {}
        return cls._instance
```

### 4. Composition Over Inheritance

**Decision:** `SpecializedAgent` contains a list of `Tool` objects rather than inheriting from a tool-aware base.

**Rationale:**
- Flexible: Add/remove tools at runtime
- Decoupled: Tools don't know about agents
- Testable: Mock tools easily
- Extensible: New tool types don't require agent changes

### 5. Property-Based Prompt Generation

**Decision:** Generate system prompts dynamically via `@property`.

**Rationale:**
- Always reflects current state
- No synchronization issues
- Customizable via `system_prompt` override
- Includes all responsibilities and tools

### 6. Backward Compatibility

**Decision:** Provide `to_base_agent()` method for compatibility with existing code.

**Rationale:**
- Existing `run_meeting()` function expects `Agent` objects
- Gradual migration path
- No breaking changes to existing workflows

---

## Usage Guide

### Basic Usage

```python
from virtual_lab import VALIDATION_BENCHMARKING_AGENT

# Use the pre-configured agent
agent = VALIDATION_BENCHMARKING_AGENT

# Get the system prompt for the LLM
print(agent.prompt)

# Check what tools are available
for tool in agent.tools:
    print(f"{tool.name}: {tool.description}")
```

### QC Assay Queries

```python
# Get all assays for a specific timepoint
day_60_assays = agent.get_assays_for_timepoint(60)

for assay in day_60_assays:
    print(f"\n{assay.name} ({assay.timing})")
    print(f"Markers: {', '.join(assay.markers)}")
    print("Expected outcomes:")
    for outcome in assay.expected_outcomes:
        print(f"  - {outcome}")
```

### Off-Target Detection

```python
# Check a gene list for off-target signatures
expressed_genes = [
    "PAX6", "SOX2", "FOXG1",  # Expected dorsal forebrain
    "NKX2.1",                  # Ventral marker (off-target!)
    "ATF4", "DDIT3"            # Stress markers (concerning!)
]

issues = agent.check_off_target_fates(expressed_genes)

if issues:
    print("WARNING: Off-target fates detected!")
    for fate, markers in issues.items():
        print(f"  {fate}: {markers}")
```

### Generating Validation Protocols

```python
# Generate a comprehensive validation protocol
protocol = agent.generate_validation_protocol(
    timepoints=[10, 25, 45, 60, 90, 120, 150]
)

# Access timepoint-specific assays
for timepoint, assays in protocol["timepoints"].items():
    print(f"\n{timepoint}:")
    for assay in assays:
        print(f"  - {assay['assay']}")
        print(f"    Markers: {assay['markers']}")
```

### scRNA-seq Alignment Evaluation

```python
# Compare organoid cell composition to fetal reference
organoid_data = {
    "ventricular radial glia": 0.25,
    "outer radial glia": 0.15,
    "intermediate progenitors": 0.20,
    "deep layer neurons": 0.30,
    "upper layer neurons": 0.10,
}

evaluation = agent.evaluate_scrnaseq_alignment(
    organoid_cell_types=organoid_data,
    reference_stage="GW14-18"
)

print("Missing cell types:", evaluation["missing_types"])
print("Unexpected types:", evaluation["unexpected_types"])
print("Concerns:")
for concern in evaluation["concerns"]:
    print(f"  - {concern}")
```

### Integration with run_meeting()

```python
from virtual_lab import run_meeting, VALIDATION_BENCHMARKING_AGENT
from virtual_lab.prompts import PRINCIPAL_INVESTIGATOR

# Convert to base agent for compatibility
validation_agent = VALIDATION_BENCHMARKING_AGENT.to_base_agent()

# Use in a team meeting
summary = run_meeting(
    meeting_type="team",
    agenda="Review the proposed dorsal forebrain organoid protocol",
    save_dir=Path("./meetings"),
    team_lead=PRINCIPAL_INVESTIGATOR,
    team_members=(validation_agent,),
    num_rounds=3,
)
```

### Creating Custom Agents

```python
from virtual_lab.agents import SpecializedAgent, InteractionStyle
from virtual_lab.agents.tools import BrainSpanTool

# Create a custom specialized agent
my_agent = SpecializedAgent(
    name="spatial_analyst",
    title="Spatial Transcriptomics Specialist",
    expertise="spatial gene expression analysis and tissue architecture",
    goal="validate spatial organization of organoid tissues",
    role="analyze spatial transcriptomics data and compare to references",
    responsibilities=[
        "Evaluate layer organization using spatial markers",
        "Assess cell type localization patterns",
        "Compare to fetal cortex spatial references",
    ],
    tools=[BrainSpanTool()],
    interaction_style=InteractionStyle.ANALYTICAL,
)
```

---

## Extending the Framework

### Adding a New Tool

1. Create a new tool class in `tools/` directory:

```python
# tools/my_new_tool.py
from dataclasses import dataclass, field
from typing import Any
from virtual_lab.agents.tools.base import Tool

@dataclass
class MyNewTool(Tool):
    name: str = "my_tool"
    description: str = "Description of what the tool does"
    category: str = "analysis"  # Optional categorization

    # Tool-specific configuration
    my_config: list[str] = field(default_factory=list)

    def execute(self, **kwargs) -> dict[str, Any]:
        """Implement the tool's main functionality."""
        param1 = kwargs.get("param1", "default")

        # Your implementation here
        result = self._do_something(param1)

        return {
            "status": "success",
            "tool": self.name,
            "result": result,
        }

    def validate_params(self, **kwargs) -> bool:
        """Validate input parameters."""
        if "param1" in kwargs:
            if not isinstance(kwargs["param1"], str):
                return False
        return True

    def _do_something(self, param: str) -> str:
        """Private helper method."""
        return f"Processed: {param}"
```

2. Export from `tools/__init__.py`:

```python
from virtual_lab.agents.tools.my_new_tool import MyNewTool

__all__ = [
    # ... existing exports
    "MyNewTool",
]
```

### Adding a New Specialized Agent

1. Create a new agent file:

```python
# my_agent.py
from dataclasses import dataclass, field
from virtual_lab.agents.base import SpecializedAgent, InteractionStyle
from virtual_lab.agents.tools import MyNewTool

@dataclass
class MySpecializedAgent(SpecializedAgent):
    # Set defaults for your agent type
    name: str = "my_agent"
    title: str = "My Specialist"
    expertise: str = "specific domain expertise"
    goal: str = "achieve specific objective"
    role: str = "perform specific role"
    interaction_style: InteractionStyle = InteractionStyle.ANALYTICAL

    # Agent-specific data
    my_data: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__post_init__()

        # Initialize tools
        if not self.tools:
            self.tools = [MyNewTool()]

        # Set responsibilities
        self.responsibilities = [
            "First responsibility",
            "Second responsibility",
        ]

    def my_custom_method(self) -> dict:
        """Add domain-specific methods."""
        return {"data": self.my_data}

# Pre-instantiated default
MY_AGENT = MySpecializedAgent()
```

2. Export from `agents/__init__.py`:

```python
from virtual_lab.agents.my_agent import MySpecializedAgent, MY_AGENT

__all__ = [
    # ... existing exports
    "MySpecializedAgent",
    "MY_AGENT",
]
```

### Adding New Interaction Styles

```python
# In base.py
class InteractionStyle(Enum):
    COLLABORATIVE = "collaborative"
    SKEPTICAL = "skeptical"
    SUPPORTIVE = "supportive"
    ANALYTICAL = "analytical"
    DIRECTIVE = "directive"
    # Add new style
    EXPLORATORY = "exploratory"

# Add description in SpecializedAgent.prompt property
interaction_descriptions = {
    # ... existing descriptions
    InteractionStyle.EXPLORATORY: (
        "Your interaction style is exploratory. "
        "Ask open-ended questions, consider alternative hypotheses, "
        "and encourage creative problem-solving."
    ),
}
```

---

## Integration with Virtual Lab

### How It Fits

The agents module is designed to integrate seamlessly with the existing Virtual Lab framework:

```
┌─────────────────────────────────────────────────────────────┐
│                    Existing Virtual Lab                      │
│                                                              │
│  ┌────────────┐    ┌─────────────┐    ┌─────────────────┐   │
│  │   Agent    │    │ run_meeting │    │    prompts.py   │   │
│  │  (basic)   │───▶│   function  │◀───│  PRINCIPAL_INV  │   │
│  └────────────┘    └─────────────┘    │ SCIENTIFIC_CRIT │   │
│        ▲                              └─────────────────┘   │
│        │                                                     │
│        │ to_base_agent()                                     │
│        │                                                     │
│  ┌─────┴──────────────────────────────────────────────────┐ │
│  │                    Agents Module                        │ │
│  │                                                         │ │
│  │  SpecializedAgent ────▶ ValidationBenchmarkingAgent    │ │
│  │         │                                               │ │
│  │         ▼                                               │ │
│  │     Tools ────▶ BrainSpan, scRNA-seq, Benchmarks...    │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Compatibility Layer

The `to_base_agent()` method ensures backward compatibility:

```python
# SpecializedAgent -> Agent conversion
def to_base_agent(self) -> Agent:
    return Agent(
        title=self.title,
        expertise=self.expertise,
        goal=self.goal,
        role=self.role,
        model=self.model,
    )
```

This allows using specialized agents with the existing `run_meeting()` function without modification.

---

## API Reference

### Classes

#### `SpecializedAgent`

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Unique identifier |
| `title` | `str` | Display name |
| `expertise` | `str` | Area of expertise |
| `goal` | `str` | Primary objective |
| `role` | `str` | Role in team |
| `responsibilities` | `list[str]` | Specific duties |
| `tools` | `list[Tool]` | Available tools |
| `interaction_style` | `InteractionStyle` | Behavior pattern |
| `system_prompt` | `str \| None` | Custom prompt override |
| `model` | `str` | LLM model |

| Method | Returns | Description |
|--------|---------|-------------|
| `prompt` | `str` | Generated system prompt |
| `message` | `dict` | OpenAI API format |
| `to_base_agent()` | `Agent` | Convert to base Agent |
| `get_tool(name)` | `Tool \| None` | Get tool by name |
| `add_tool(tool)` | `None` | Add a tool |
| `remove_tool(name)` | `bool` | Remove tool by name |

#### `ValidationBenchmarkingAgent`

Inherits from `SpecializedAgent` with additional:

| Attribute | Type | Description |
|-----------|------|-------------|
| `qc_assays` | `list[QCAssay]` | QC assay definitions |
| `benchmarks` | `list[DevelopmentalBenchmark]` | Reference benchmarks |
| `off_target_signatures` | `dict[str, list[str]]` | Off-target markers |

| Method | Returns | Description |
|--------|---------|-------------|
| `get_qc_assay(name)` | `QCAssay \| None` | Get assay by name |
| `get_benchmark(stage)` | `DevelopmentalBenchmark \| None` | Get benchmark by stage |
| `get_assays_for_timepoint(day)` | `list[QCAssay]` | Assays for culture day |
| `check_off_target_fates(genes)` | `dict[str, list[str]]` | Detect off-target |
| `generate_validation_protocol(timepoints)` | `dict` | Full protocol |
| `evaluate_scrnaseq_alignment(...)` | `dict` | Alignment evaluation |

#### `Tool` (Abstract)

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Unique identifier |
| `description` | `str` | Human-readable description |
| `version` | `str` | Semantic version |
| `enabled` | `bool` | Whether tool is active |

| Method | Returns | Description |
|--------|---------|-------------|
| `execute(**kwargs)` | `dict` | Run the tool (abstract) |
| `validate_params(**kwargs)` | `bool` | Validate params (abstract) |
| `get_schema()` | `dict` | JSON schema for params |

#### `ToolRegistry`

| Method | Returns | Description |
|--------|---------|-------------|
| `register(tool)` | `None` | Register a tool |
| `unregister(name)` | `bool` | Unregister a tool |
| `get(name)` | `Tool \| None` | Get tool by name |
| `list_tools()` | `list[str]` | List all tool names |
| `get_tools_by_category(cat)` | `list[Tool]` | Filter by category |
| `clear()` | `None` | Remove all tools |
| `reset()` | `None` | Reset singleton (classmethod) |

### Constants

| Name | Type | Description |
|------|------|-------------|
| `VALIDATION_BENCHMARKING_AGENT` | `ValidationBenchmarkingAgent` | Pre-configured agent instance |

---

## Summary

The Agents Module provides a modular, extensible framework for creating specialized AI agents in the Virtual Lab. Key takeaways:

1. **Modularity**: Clean separation between base classes, tools, and agent implementations
2. **Type Safety**: Extensive use of type hints and enums for robust code
3. **Extensibility**: Easy to add new tools, agents, and interaction styles
4. **Compatibility**: Seamless integration with existing Virtual Lab code
5. **Domain Knowledge**: Pre-configured QC assays and developmental benchmarks

For questions or contributions, refer to the main Virtual Lab repository.
