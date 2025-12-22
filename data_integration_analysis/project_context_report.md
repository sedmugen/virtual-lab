# Data Integration Layer: Project Context & Status Report

**Date:** December 7, 2025
**Module:** `src/data_integration`

## 1. Project Overview & Objective
The primary goal of this phase was to architect and implement a **Data Integration Layer** capable of ingesting, normalizing, and storing heterogeneous data from various materials science and biological resources. This layer serves as the foundation for a unified "Virtual Lab" system that allows for cross-domain querying (e.g., finding hydrogels compatible with specific cell signaling pathways).

## 2. Methodology & Workflow
We adopted an **Iterative, Resource-Centric Workflow**:

1.  **Analysis First:** We began by rigorously analyzing 10 potential resources to understand their data types, access methods (API vs. Scraping vs. File), and limitations.
2.  **Step-by-Step Implementation:** We integrated resources one by one, verifying functionality immediately with isolated test scripts (`if __name__ == "__main__":` blocks).
3.  **Fail-Fast & Adapt:**
    *   When **MatWeb** scraping proved fragile, we pivoted to a manual curation strategy recommendation.
    *   When **ChEBI** and **MatPortal** APIs were down/unreachable, we marked them as "Blocked" and proceeded with available resources to maintain momentum.
    *   For file-based resources (**3D Bioprinting**, **Signaling Pathways**), we simulated the environment with sample CSVs to ensure code readiness.
4.  **Unification:** We culminated the effort by building an **Orchestrator (`main.py`)** that ties all individual modules into a coherent execution flow, establishing a "Data Lake" architecture.

## 3. Current Implementation Status

We analyzed 10 resources. **5 are currently operational** and integrated.

| Resource | Integration Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| **PubChem** | API (`pubchempy`) | 🟢 **Operational** | successfully resolves chemical names to CIDs and SMILES. |
| **Materials Project** | API (`mp-api`) | 🟢 **Operational** | Retrieving material properties (DFT data) using API Key. |
| **HydrogelDB** | OAI-PMH (Simulated) | 🟢 **Operational** | XML metadata harvesting logic is implemented and tested. |
| **3D Bioprinting Hub** | CSV Loader (`pandas`) | 🟢 **Operational** | robust loading and basic cleaning of local CSV datasets. |
| **Signaling Pathways** | CSV Loader (`pandas`) | 🟢 **Operational** | Parsing and cleaning of gene expression datasets. |
| **ChEBI** | REST API | 🔴 **Blocked** | External API returning 500 Errors. Retry logic needed. |
| **MatPortal** | REST API | 🔴 **Blocked** | SSL/Certificate errors on remote server. |
| **MatWeb** | Web Scraper | ❌ **Failed** | Site structure and bot protection make scraping unreliable. |
| **PolyInfo** | N/A | ⛔ **Skipped** | Access highly restricted (requires contract). |
| **BioMatDB** | N/A | ⛔ **Skipped** | In early development; no stable endpoint. |

## 4. System Architecture: The "Data Lakehouse"

We established a directory-based Data Lake architecture in `src/data_integration/data_lake/`.

1.  **Ingestion Layer (`src/data_integration/*.py`)**:
    *   Standalone modules responsible for connecting to specific external sources.
    *   Handles authentication (API Keys via `.env`).
2.  **Raw Storage (`data_lake/raw/`)**:
    *   Stores data exactly as received (JSON/CSV) with timestamps.
    *   Ensures full auditability and allows for re-processing without re-fetching.
3.  **Processing Layer (`clean_*` functions)**:
    *   Standardizes column names (snake_case).
    *   Converts data types (strings to floats).
4.  **Processed Storage (`data_lake/processed/`)**:
    *   Clean, analysis-ready CSV files ready for downstream databases or ML models.

## 5. Directory Structure
```text
D:\GitHub\virtual-lab-euler\
├── .env                          # API Keys (MP_API_KEY, etc.)
├── data_integration_analysis/    # Documentation & Sample Data
│   ├── integration_plan.md       # Initial architectural plan
│   ├── resources_overview.md     # Detailed analysis of external sites
│   ├── 3d_bioprinting_...csv     # Sample data
│   └── signaling_pathways...csv  # Sample data
└── src/
    └── data_integration/
        ├── data_lake/            # STORAGE
        │   ├── raw/
        │   └── processed/
        ├── bioprinting_...py     # Module
        ├── hydrogeldb_...py      # Module
        ├── main.py               # ORCHESTRATOR
        ├── materials_project...py# Module
        ├── pubchem_...py         # Module
        └── signaling_...py       # Module
```

## 6. Technical Recommendations & Missed Items

While the current prototype is functional, a production-grade system requires:

1.  **Logging:** Currently using `print()`. Replace with Python's `logging` module to track execution history, errors, and data volume stats to a file.
2.  **Configuration Management:** Move hardcoded URLs and default parameters to a `config.yaml` or `settings.py` file, separating code from configuration.
3.  **Data Validation:** Implement **Pydantic** models to strictly validate incoming data schema (e.g., ensuring "pH" is a float between 0-14).
4.  **AsyncIO:** For API-heavy integrations (PubChem, Materials Project), switching to asynchronous requests (`aiohttp`) would significantly speed up bulk data fetching.
5.  **Unit Testing:** We have basic `if __name__ == "__main__":` blocks. We need a proper test suite using `pytest` to mock API responses and ensure stability.

## 7. Future Roadmap (Next Steps)

1.  **Database Implementation:** Transition from file-based "Processed" storage to a queryable database (**PostgreSQL** or **SQLite**).
2.  **Unified Search:** Build a simple query engine to search across all ingested data (e.g., "Find me materials with density < 3.0 mentioned in Bioprinting papers").
3.  **Resilience:** Implement "Expontential Backoff" retry logic for the ChEBI and MatPortal APIs to handle temporary outages automatically.
