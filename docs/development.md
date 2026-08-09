# Developer Guide

Guide for contributing, extending agents, adding new tools, and developing Data Lake integrations in Virtual Lab.

---

## Code Base Structure

```
src/
├── virtual_lab/             # Core Python package
│   ├── agent.py             # Agent dataclass representation
│   ├── config.py            # Multi-provider LLM API initialization
│   ├── constants.py         # Pricing, temperatures, tool definitions
│   ├── prompts.py           # Structured meeting prompt generators
│   ├── run_meeting.py       # Meeting orchestration engine
│   ├── utils.py             # Token counting, PubMed search, saving utils
│   └── tools/               # Agent-callable tools
│       └── formulation.py   # Data Lake lookup wrappers
└── data_integration/        # Offline ETL pipelines & Data Lake
    ├── main.py              # Orchestrator
    └── data_lake/           # raw/ and processed/ datasets
```

---

## Core Development Patterns

### Adding a Custom Agent

Agents are immutable representations defined via the `Agent` dataclass:

```python
from virtual_lab import Agent

my_agent = Agent(
    title="Structural Bioinformatician",
    expertise="high-throughput docking and binding site analysis",
    goal="evaluate structural feasibility of designed interfaces",
    role="critique binding pose predictions and surface complementarity",
    model="gpt-4o",
)
```

### Creating an Agent Tool

Tools are functions wrapped in OpenAI function definition schemas:

1. **Define the Python function in `src/virtual_lab/tools/`:**
   ```python
   def my_tool(query: str) -> str:
       # Tool logic
       return f"Result for {query}"
   ```

2. **Define the JSON schema in `src/virtual_lab/constants.py`:**
   ```python
   MY_TOOL_DESCRIPTION = {
       "type": "function",
       "function": {
           "name": "my_tool",
           "description": "Description of what the tool does.",
           "parameters": { ... },
       },
   }
   ```

3. **Register execution in `src/virtual_lab/utils.py` inside `run_tools()`.**

---

## Testing

Run unit tests with `pytest`:

```bash
pytest tests/ -v
```

Ensure all tests pass before submitting pull requests.

---

## Formatting & Linting Standard

Virtual Lab uses standard PEP 8 formatting conventions:
- Type annotations on all public functions.
- 4-space indentation.
- Standard Google / Sphinx docstring format.
- No debug `print` statements or leftover commented-out blocks.
