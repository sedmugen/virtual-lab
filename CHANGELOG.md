# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [Unreleased]

## [1.1.0] — 2025

### Added
- Multi-provider LLM configuration (`src/virtual_lab/config.py`): switch between
  OpenAI, OpenRouter, and BigModel (GLM-4-Flash) by changing `ACTIVE_PROVIDER`.
- `data-integration` optional dependency group in `pyproject.toml`.
- Data Integration layer (`src/data_integration/`) — ETL pipelines for:
  - PubChem (chemical properties)
  - Materials Project (material properties via `mp-api`)
  - HydrogelDB (OAI-PMH metadata harvesting)
  - MatWeb (web scraping via BeautifulSoup)
  - MatPortal (ontology-aligned materials data)
  - ChEBI (chemical entity annotations)
  - 3D Bioprinting Data Hub (CSV ingest)
  - Signaling Pathways Project (CSV ingest)
- Data Lake file structure (`src/data_integration/data_lake/raw/` and `processed/`).
- Formulation agent demo (`src/virtual_lab/formulation_agent_demo.py`).
- Formulation tool wrappers (`src/virtual_lab/tools/formulation.py`) for agent use.
- `docs/` folder with architecture, API, and design-decision documentation.
- `assets/` folder with architecture diagrams and visual assets.
- `CONTRIBUTING.md` and `.env.example` for contributor onboarding.

### Changed
- `pyproject.toml` project URLs updated to `sedmugen/virtual-lab`.
- `config.py` provider-selection logic refactored into `get_config()` factory.
- Dead code removed from `utils.py`, `prompts.py`, and `constants.py`.
- `assert` statements replaced with explicit `ValueError` raises in `utils.py`.
- `src/data_integration/` converted to a proper Python package.

### Fixed
- Debug `print("DEBUG team contents:")` removed from `run_meeting.py`.
- Duplicate local `Agent` class removed from `formulation_agent_demo.py`.
- Tamil Unicode artefact removed from `formulation_agent_demo.py`.
- Docstring typo "tean meeting" corrected to "team meeting" in `prompts.py`.

## [1.0.0] — 2025

### Added
- Initial release (upstream `zou-group/virtual-lab` v1.0.0).
- `run_meeting()` — core API for team and individual LLM agent meetings.
- `Agent` class for defining LLM agent personas (title, expertise, goal, role, model).
- `PRINCIPAL_INVESTIGATOR` and `SCIENTIFIC_CRITIC` default agent definitions.
- `pubmed_search` tool: agents can retrieve biomedical literature from PubMed Central.
- Structured prompt templates for meeting types, agendas, questions, and rules.
- Token counting and USD cost estimation after each meeting.
- JSON and Markdown transcript persistence for all meetings.
- Nanobody design pipeline application (`nanobody_design/`):
  - ESM log-likelihood ratio scoring of mutations.
  - AlphaFold-Multimer interface pLDDT scoring.
  - Rosetta binding energy (delta G) calculation.
  - 4-round iterative design loop.
  - 92 experimentally validated nanobodies (SARS-CoV-2 KP.3 spike RBD).
- Published in: Swanson, K. et al. Nature (2025). https://doi.org/10.1038/s41586-025-09442-9
