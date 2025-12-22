# Virtual Lab Context

## Overview
The **Virtual Lab** is a Python-based framework for conducting scientific research using a team of Large Language Model (LLM) agents. It automates the process of scientific discourse, planning, and critique. The primary demonstration of this system is the `nanobody_design` project, which designs nanobodies for SARS-CoV-2 variants.

## Core Framework (`src/virtual_lab`)
The core logic resides in `src/virtual_lab/`. It utilizes the OpenAI Assistants API to simulate "meetings" between agents with specific scientific roles.

### Key Components
- **Orchestration (`run_meeting.py`):** The central script that manages the conversation flow between agents. It supports:
  - **Team Meetings:** collaborative discussions involving multiple agents.
  - **Individual Meetings:** 1-on-1 sessions, typically between a researcher and a Scientific Critic.
- **Agents (`agent.py`):** Defines the `Agent` class, capturing the persona, expertise, role, and goal of each LLM participant (e.g., "Principal Investigator", "Immunologist").
- **Prompts (`prompts.py`):** Contains the system prompts that guide the agents' behavior and meeting structure.
- **Utilities (`utils.py`):**
  - **Tools:** Implements the `pubmed_search` tool for agents to retrieve literature.
  - **Cost Tracking:** Calculates and logs the cost of API usage (token counts) using pricing defined in `constants.py`.
  - **State Management:** Saves meeting transcripts to JSON and Markdown.
- **Configuration (`constants.py`):** Stores model pricing, tool definitions, and other static configuration.

## Application: Nanobody Design (`nanobody_design/`)
This directory contains a concrete application of the Virtual Lab to design high-affinity nanobodies for the SARS-CoV-2 spike protein (specifically the KP.3 variant).

### Workflow
The workflow involves an iterative cycle of design and validation, orchestrated by LLM agents and executed via shell scripts and Python modules.

1.  **Design (ESM):** Generate mutations of wild-type nanobodies (Ty1, H11-D4, Nb21, VHH-72) using ESM log-likelihood ratios.
2.  **Structure Prediction (AlphaFold-Multimer):** Predict the structure of the mutated nanobody-spike complex.
3.  **Scoring (Rosetta):** Calculate interface binding energies based on the predicted structures.
4.  **Selection:** Rank and select top candidates based on a weighted score of ESM, AlphaFold, and Rosetta metrics.
5.  **Synthesis Prep:** Prepare sequences for experimental validation (adding leader sequences and His-tags).

### Key Files
- **`run_nanobody_design.ipynb`:** The notebook that initializes the agents and runs the simulated meetings to plan the research.
- **`workflow.md`:** Documentation of the shell commands used for the computational pipeline (ESM -> AlphaFold -> Rosetta).
- **`nanobody_constants.py`:** Project-specific constants, including agent definitions (Immunologist, Machine Learning Specialist, etc.) and prompt templates for this specific scientific domain.
- **`scripts/`:** Contains the implementation of the computational models and data processing steps.
- **`designed/`:** Stores the output data (CSV scores, PDB structures) from each round of design.

## Technical Details
- **Dependencies:** `openai`, `torch`, `biopython`, `pandas`, `notebook`, `tiktoken`.
- **LLM Models:** Primarily uses `gpt-4o` and `gpt-4o-mini`.
- **Environment:** Requires an OpenAI API key.
