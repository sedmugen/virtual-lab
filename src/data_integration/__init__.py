"""Data integration ETL pipeline for Virtual Lab.

This package provides scripts to ingest, normalise, and store data from
external materials-science and biological databases into a local Data Lake.

Modules
-------
main
    Orchestrator — runs all integrations in sequence.
pubchem_integration
    Fetch canonical chemical data from PubChem REST API.
materials_project_integration
    Fetch material properties from the Materials Project API.
hydrogeldb_integration
    Harvest hydrogel metadata via simulated OAI-PMH protocol.
matweb_integration
    Scrape mechanical properties from MatWeb.
matportal_integration
    Retrieve ontology-aligned materials data from MatPortal.
chebi_integration
    Fetch chemical entity data from ChEBI.
bioprinting_data_hub_integration
    Ingest 3D bioprinting parameters from CSV exports.
signaling_pathways_integration
    Ingest gene expression / signaling pathway data from CSV exports.

Usage
-----
Run all integrations from the project root::

    python -m src.data_integration.main

Output is written to ``src/data_integration/data_lake/``:

* ``raw/``       — original API responses and CSV snapshots (timestamped).
* ``processed/`` — cleaned, normalised DataFrames ready for agent tool use.
"""
