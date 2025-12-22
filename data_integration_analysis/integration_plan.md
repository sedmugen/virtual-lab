# Unified Data Pipeline Architecture

## Architecture Diagram
```mermaid
graph TD
    subgraph "External Sources"
        MW[MatWeb (Scraper)]
        MP[Materials Project (API)]
        HDB[HydrogelDB (OAI-PMH)]
        PI[PolyInfo (Manual/RDF)]
        SPP[Signaling Project (CSV)]
        BPH[Bioprinting Hub (CSV)]
        PC[PubChem (API)]
        CH[ChEBI (API)]
        MPort[MatPortal (API)]
    end

    subgraph "Ingestion Layer (Python)"
        Scrapers[Custom Scrapers / Parsers]
        Clients[API Clients (mp-api, PubChemPy)]
        Normalizer[Data Normalizer & Unit Converter]
    end

    subgraph "Storage Layer"
        RawDB[(Raw Data Lake - JSON/Parquet)]
        CleanDB[(Structured Database - SQL/NoSQL)]
        VectorDB[(Vector Store for Semantic Search)]
    end

    subgraph "Application Layer"
        Search[Unified Search Engine]
        Analysis[Material-Cell Interaction Analysis]
        Export[API Gateway]
    end

    MW --> Scrapers
    MP --> Clients
    HDB --> Scrapers
    PI --> Scrapers
    SPP --> Scrapers
    BPH --> Scrapers
    PC --> Clients
    CH --> Clients
    MPort --> Normalizer

    Scrapers --> RawDB
    Clients --> RawDB

    RawDB --> Normalizer
    Normalizer --> CleanDB
    CleanDB --> VectorDB

    CleanDB --> Search
    CleanDB --> Analysis
    CleanDB --> Export
```

## Step-by-Step Integration Plan

### Phase 1: Ingestion (Extract)
1.  **API Clients:** Implement `mp-api` and `PubChemPy` scripts to fetch base material and chemical data.
2.  **Scrapers:** Build a robust `BeautifulSoup` scraper for MatWeb (with rate limiting).
3.  **Harvesters:** Write an OAI-PMH harvester for HydrogelDB metadata.
4.  **File Loaders:** Create scripts to ingest CSV dumps from SPP and 3D Bioprinting Data Hub.

### Phase 2: Normalization (Transform)
1.  **Ontology Mapping:** Use **MatPortal** and **ChEBI** to map heterogeneous terms (e.g., "Young's Modulus", "Elastic Modulus", "E-mod") to a single unique identifier (URI).
2.  **Unit Conversion:** All mechanical properties converted to SI units (Pa, Kg/m^3, etc.) using a standard library like `pint`.
3.  **Entity Resolution:** Use **PubChem** CIDs (Compound IDs) as the "Foreign Key" to link materials across databases where possible.

### Phase 3: Storage (Load)
1.  **Raw Store:** Save original JSON/HTML responses to a "Data Lake" (e.g., local directory or S3 bucket) for audit trails.
2.  **Structured Store:** Load cleaned, normalized data into a PostgreSQL database with a schema optimized for material properties and biological interactions.

### Phase 4: Application
1.  **Query Interface:** A Python API (FastAPI) that allows querying: *"Find me a hydrogel with Elastic Modulus > 10kPa that allows cell adhesion (linked to specific Integrin signaling pathways)."*

## Dataset Harmonization Strategy

*   **Units:** Enforce **SI Units** (International System of Units).
*   **Chemical IDs:** Use **InChIKey** as the primary deduplication key for small molecules.
*   **Material IDs:** Generate internal UUIDs for complex materials (composites, hydrogels) but link them to their constituents' InChIKeys.
*   **Metadata:** Adhere to the **Fair Data Principles**. Use schema.org/Material where applicable.
