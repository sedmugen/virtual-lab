# Setup & Installation Guide

This guide provides step-by-step instructions to set up Virtual Lab for local development, research experiments, or data integration workflows.

---

## Prerequisites

- **Python**: 3.10, 3.11, 3.12, or 3.13 (Python 3.12 recommended).
- **Conda / Mamba**: Recommended for environment management.
- **Git**: For version control.
- **API Keys**: At least one LLM provider key (OpenAI, BigModel, or OpenRouter).

---

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/sedmugen/virtual-lab.git
cd virtual-lab
```

### 2. Create a Virtual Environment

```bash
conda create -n virtual_lab python=3.12 -y
conda activate virtual_lab
```

### 3. Install Package Dependencies

Virtual Lab offers modular installation targets depending on your use case:

```bash
# Core framework only
pip install -e .

# Core + Nanobody design tools (ESM, Biopython, Torch, Seaborn)
pip install -e ".[nanobody-design]"

# Core + Data integration ETL tools (Materials Project, PubChem, BeautifulSoup)
pip install -e ".[data-integration]"

# Complete development environment (all extras)
pip install -e ".[nanobody-design,data-integration]"
```

### 4. Configure Environment Variables

Copy the template `.env.example` file to `.env`:

```bash
cp .env.example .env
```

Edit `.env` and set your API keys:

```env
OPENAI_API_KEY=sk-...
# Optional alternative providers:
BIGMODEL_API_KEY=...
OPENROUTER_API_KEY=...
```

---

## Verification

Verify your setup by running the configuration check:

```bash
python -m virtual_lab.config
```

Expected output:
```text
Provider : openai
Base URL : None
Model    : gpt-4o
Key      : sk-... (truncated)
```

Run unit tests to ensure everything is functioning correctly:

```bash
pytest tests/
```
