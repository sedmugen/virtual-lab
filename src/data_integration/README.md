# Data Integration Module (`src/data_integration`)

This module is responsible for ingesting, standardizing, and storing data from external materials science and biological resources.

## Quick Start

1.  **Setup Environment:**
    Ensure you have a `.env` file in the project root with the following keys:
    ```bash
    MP_API_KEY="your_materials_project_key"
    MATPORTAL_API_KEY="your_matportal_key"
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    # Or manually: pip install requests pandas pubchempy mp-api python-dotenv beautifulsoup4
    ```

3.  **Run Orchestrator:**
    Run the main script as a module to trigger all integrations:
    ```bash
    python -m src.data_integration.main
    ```

## Architecture
The system follows a "Data Lake" pattern:
*   **Extract:** Scripts fetch data from APIs or load local CSVs.
*   **Load (Raw):** Data is saved as-is to `data_lake/raw/` with timestamps.
*   **Transform:** Data is cleaned (normalization, type casting) and saved to `data_lake/processed/`.

## Available Integrations
*   `pubchem_integration.py`: Chemical name resolution (API).
*   `materials_project_integration.py`: Material properties (API).
*   `hydrogeldb_integration.py`: Metadata harvesting (OAI-PMH Simulation).
*   `bioprinting_data_hub_integration.py`: 3D printing parameters (CSV).
*   `signaling_pathways_integration.py`: Gene expression data (CSV).
