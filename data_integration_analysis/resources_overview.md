# Data Resources Overview

This document summarizes the analysis of the external data resources for the unified materials-science software project.

| Resource | Type | Access | API/Method | Key Data |
| :--- | :--- | :--- | :--- | :--- |
| **MatWeb** | Materials Property Database | Freemium / Limited | Web Scraping (No official API) | Mechanical, thermal, and electrical properties of metals, plastics, and ceramics. |
| **Materials Project** | Computational Materials Science | Free (API Key required) | `mp-api` (Python SDK) / REST API | Crystal structures, band structures, thermodynamic data, phase diagrams. |
| **HydrogelDB** | Hydrogel Materials Data | Free | OAI-PMH (Metadata) / Manual Download | Hydrogel composition, preparation methods, properties (swelling, mechanical). |
| **PolyInfo** | Polymer Database | Restricted (NIMS) | Restricted API / SPARQL (requires login/contract) | Polymer structures, properties, processing conditions, polymerization methods. |
| **BioMatDB** | Biomaterials Database | In Development / Beta | Web Portal / Potential Future API | Biocompatibility, medical application suitability, material properties. |
| **MatPortal** | Materials Ontology Repository | Free (API Key) | REST API | Ontologies, semantic metadata for materials science (alignment tools). |
| **Signaling Pathways Project (SPP)** (Cell Behavior) | Cell Signaling & Behavior | Free | Dataset Downloads / Web Access | Transcriptomic/ChIP-Seq datasets, receptor/enzyme signaling networks. |
| **3D Bioprinting Data Hub** | Bioprinting Parameters | Free | Manual Download (CSV) / Literature Mining | Bioink compositions, printing parameters, cell viability data. |
| **PubChem** | Chemical Database | Free | PUG REST API / `PubChemPy` | Chemical structures (SMILES/InChI), bioactivity, toxicity, physical properties. |
| **ChEBI** | Chemical Ontology | Free | REST API (SOAP deprecated) | Hierarchical ontology of small molecules, biological roles, functional groups. |

## Detailed Resource Analysis

### 1. MatWeb
*   **Status:** High-value data but difficult programmatic access.
*   **Data:** Commercial grade material properties.
*   **Integration:** Requires a custom web scraper using `requests` and `BeautifulSoup`. Respect `robots.txt` and rate limits.
*   **Alternative:** Use "MatMatch" or similar if they have better APIs, but MatWeb is the standard for legacy data.

### 2. Materials Project
*   **Status:** Gold standard for computational materials.
*   **Data:** Calculated quantum mechanical properties.
*   **Integration:** Official Python client `mp-api`.
*   **Constraint:** Data is theoretical/computational, not always experimental.

### 3. HydrogelDB (Hydrogel Database HD)
*   **Status:** Niche academic database.
*   **Data:** Experimental data on hydrogels.
*   **Integration:** Use `OAI-PMH` protocol for metadata harvesting. Actual property data might need to be parsed from the "description" fields or downloaded manually if endpoints don't expose full tabular data.

### 4. PolyInfo (NIMS)
*   **Status:** Highly restricted.
*   **Data:** Comprehensive polymer informatics.
*   **Integration:** **Blocked** for general automated pipelines without specific academic/corporate contracts.
*   **Workaround:** Use **PoLyInfo**'s open RDF subset if available, or fall back to **Polymer Genome** or **PubChem** for basic polymer units.

### 5. BioMatDB
*   **Status:** Early stage / EU Project.
*   **Integration:** Monitor for "Open API" releases. Currently, treat as a manual data source for validation or specific lookup.

### 6. MatPortal
*   **Status:** Semantic backbone.
*   **Data:** Ontologies (not material properties themselves).
*   **Integration:** Use to map terms between databases (e.g., mapping "Tensile Strength" in MatWeb to a standardized ontology term).

### 7. Signaling Pathways Project (SPP) / Cell Behavior
*   **Status:** Data repository.
*   **Integration:** Bulk download of transcriptomics datasets (CSV/Tab-delimited). Python `pandas` for processing.
*   **Usage:** Correlate material biocompatibility (from BioMatDB/HydrogelDB) with cell signaling responses (SPP).

### 8. 3D Bioprinting Data Hub
*   **Status:** Aggregated literature data.
*   **Integration:** Download CSVs periodically.
*   **Automation:** Write a script to check for updated CSV versions or use a "literature mining" agent (LLM-based) to parse new papers into this format.

### 9. PubChem
*   **Status:** Essential for chemical identity.
*   **Integration:** `PubChemPy` for easy property lookup and structure standardization (getting Canonical SMILES).

### 10. ChEBI
*   **Status:** Ontology authority.
*   **Integration:** REST API to retrieve "Is-a" relationships (e.g., verifying if a specific polymer monomer is classified correctly in biological contexts).
