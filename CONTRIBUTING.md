# Contributing

Thank you for your interest in contributing to Virtual Lab.

---

## Environment Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/sedmugen/virtual-lab.git
   cd virtual-lab
   ```

2. **Create a Python 3.12 environment**
   ```bash
   conda create -y -n virtual_lab python=3.12
   conda activate virtual_lab
   ```

3. **Install the package in editable mode**
   ```bash
   # Core only
   pip install -e .

   # With nanobody-design extras
   pip install -e ".[nanobody-design]"

   # With data-integration extras
   pip install -e ".[data-integration]"
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Fill in the keys you need (see .env.example for details)
   ```

5. **Choose your LLM provider**
   Open `src/virtual_lab/config.py` and set `ACTIVE_PROVIDER` to one of:
   `"openai"` | `"openrouter"` | `"bigmodel"`

---

## Branch Naming

```
<category>/<short-description>
```

Approved categories: `feature/` `bugfix/` `hotfix/` `docs/` `chore/` `refactor/` `test/`

Examples:
- `feature/materials-tool-wrappers`
- `bugfix/pubmed-rate-limit`
- `docs/architecture-diagram`

---

## Commit Style — Conventional Commits

```
<type>(optional-scope): imperative description under ~72 chars
```

Approved types: `feat` `fix` `refactor` `docs` `style` `test` `chore` `perf` `build` `ci`

Rules:
- Imperative mood: "add X", not "added X" or "adds X".
- One logical change per commit.
- Avoid: `Update`, `Changes`, `Fix`, `final`, `new`, `wip`.

Examples:
```
feat(config): add OpenRouter as a supported LLM provider
fix(utils): replace assert with ValueError for message validation
docs(readme): add architecture diagram to overview section
chore(deps): add data-integration optional dependency group
```

---

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

---

## Project Structure Quick Reference

```
src/virtual_lab/      # Installable Python package
src/data_integration/ # ETL pipelines (optional, not part of the package)
nanobody_design/      # Case study notebooks and scripts
assets/               # Images, GIFs, videos for documentation
docs/                 # Architecture and design documentation
tests/                # Unit and integration tests
```

See `docs/architecture.md` for a detailed system overview.
