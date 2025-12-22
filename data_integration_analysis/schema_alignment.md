# Schema & Ontology Alignment Strategy

To ensure interoperability between materials science (inorganic/polymer) and biological (cell behavior) domains, we must adopt a multi-ontology approach.

## 1. Core Ontologies

| Domain | Ontology | Purpose |
| :--- | :--- | :--- |
| **Materials** | **EMMO (European Materials & Modelling Ontology)** | High-level framework for material physics and characterization. |
| **Chemistry** | **ChEBI (Chemical Entities of Biological Interest)** | Small molecules, drugs, and polymer monomers. |
| **Polymers** | **Polymer Ontology (Polymer)** | Specifically for macromolecular structures (if available via MatPortal). |
| **Biology** | **CBO (Cell Behavior Ontology)** | Describing cell phenotypes, adhesion, and migration. |
| **General** | **QUDT (Quantities, Units, Dimensions and Types)** | Standardizing units (Pa, J, kg/m³). |

## 2. Data Schema (JSON-LD Recommendation)

We recommend using **JSON-LD** (Linked Data) for the internal data representation. This allows the data to be "self-describing" and mapped to the ontologies above.

### Example Material Record (JSON-LD)

```json
{
  "@context": {
    "schema": "http://schema.org/",
    "qudt": "http://qudt.org/schema/qudt/",
    "chebi": "http://purl.obolibrary.org/obo/CHEBI_",
    "mat": "http://emmo.info/emmo#"
  },
  "@type": "mat:Material",
  "name": "Polyethylene Glycol Diacrylate (PEGDA) Hydrogel",
  "identifiers": {
    "pubchem_cid": "123456",
    "inchikey": "XEF..."
  },
  "properties": [
    {
      "@type": "mat:MechanicalProperty",
      "name": "Elastic Modulus",
      "value": 15.5,
      "unit": "qudt:KiloPASCAL"
    },
    {
      "@type": "mat:ChemicalProperty",
      "name": "Water Content",
      "value": 90,
      "unit": "qudt:Pf"
    }
  ],
  "biological_interaction": {
    "@type": "cbo:CellAdhesion",
    "target_cell": "Fibroblast",
    "viability_score": 0.95,
    "source_dataset": "3D_Bioprinting_Hub_CSV_v1.2"
  }
}
```

## 3. Mapping Strategy

1.  **Direct Mapping:** Where APIs provide IDs (e.g., PubChem CID), use them directly.
2.  **Semantic Search:** Use embeddings (e.g., from `sentence-transformers`) to map free-text descriptions like "high stiffness" to quantitative ranges in the database (e.g., "Young's Modulus > 1 GPa").
3.  **MatPortal Lookup:** Periodically run scripts to validate standard names against MatPortal to ensure nomenclature consistency.
