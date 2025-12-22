# Integration Strategy: Materials & Formulation Data in Nanobody Lab

## 1. Context & Rationale

The current **Virtual Lab** focuses on the *computational design* of high-affinity nanobodies (Sequence $\to$ Structure $\to$ Binding Score). However, a complete therapeutic development pipeline extends beyond the molecule itself to its **formulation**, **delivery**, and **experimental validation**.

The resources integrated into `src/data_integration` (Hydrogels, Bioprinting, Chemical Properties, Signaling) serve as the foundation for **"Phase 2"** of the Virtual Lab: **Therapeutic Formulation & Delivery**.

### The "Phase 2" Workflow
1.  **Design:** (Existing) Agents design a high-affinity Nanobody against SARS-CoV-2.
2.  **Formulate:** Agents use **HydrogelDB** and **PubChem** to select a biocompatible hydrogel carrier for the nanobody (e.g., for a nasal spray or wound dressing).
3.  **Manufacture:** Agents use **3D Bioprinting Data Hub** to determine the optimal printing parameters (nozzle temp, speed) to fabricate this hydrogel without denaturing the nanobody.
4.  **Validate:** Agents use **Signaling Pathways Project** and **PubChem** to predict potential off-target toxicity or cell signaling responses of the carrier material.

## 2. Technical Integration Plan

To bridge the gap between the existing `Agent` classes and the new Data Lake, we will implement a **Tool Interface**.

### Step A: Wrap Modules as Agent Tools
The current agents use `pubmed_search` as a tool. We will create similar wrapper functions for our data modules that return natural-language summaries.

**Example Tool Definition (`src/virtual_lab/tools/materials_tools.py`):**
```python
def query_material_properties(material_name: str) -> str:
    """
    Tool for agents to look up material properties.
    Wraps 'materials_project_integration.py' and 'matweb_integration.py'.
    """
    # Call internal module
    result = get_material_summary(material_name)
    if not result:
        return f"No data found for {material_name}."
    
    # Format as natural language for the LLM
    return f"Material {result['formula']} has a formation energy of {result['formation_energy_per_atom']} eV/atom and is {'stable' if result['is_stable'] else 'unstable'}."
```

### Step B: Create New Specialist Agents
We will define new agent personas in `nanobody_design/nanobody_constants.py` who possess these tools.

1.  **Formulation Scientist:**
    *   *Expertise:* Polymer chemistry, hydrogels, drug delivery.
    *   *Tools:* `HydrogelDB`, `PubChem`, `MatPortal`.
    *   *Goal:* Select the optimal carrier matrix for the designed nanobody.
2.  **Bio-Manufacturing Engineer:**
    *   *Expertise:* 3D bioprinting, rheology.
    *   *Tools:* `BioprintingDataHub`.
    *   *Goal:* Define the fabrication protocol.
3.  **Toxicologist:**
    *   *Expertise:* Cell signaling, chemical safety.
    *   *Tools:* `SignalingPathways`, `PubChem`.
    *   *Goal:* Assess safety of the formulation.

### Step C: Update Orchestration (`run_meeting.py`)
Modify the meeting loop to include these new agents in specific "Formulation Meetings" after the "Design Selection" phase is complete.

## 3. Data Flow Diagram

```mermaid
graph TD
    subgraph "Phase 1: Design (Existing)"
        A[Immunologist]
        B[ML Specialist]
        C[AlphaFold/Rosetta]
        A <--> B
        B --> C
        C --> D[Final Nanobody Sequence]
    end

    subgraph "Phase 2: Formulation (New)"
        D --> E[Formulation Scientist]
        E -- "Query: Biocompatible Hydrogels" --> F[HydrogelDB]
        E -- "Query: Chemical Stability" --> G[PubChem]
        
        E --> H[Selected Carrier (e.g., PEG-DA)]
        
        H --> I[Bio-Manufacturing Engineer]
        I -- "Query: Printing Params" --> J[Bioprinting Hub]
        
        I --> K[Final Fabrication Protocol]
    end
```

## 4. How to Use the Data Lake Now

Until the Agent Tool Wrappers are fully implemented, you can use the data lake manually to inform your "human-in-the-loop" decisions during the simulation.

1.  **Run Integration:** `python -m src.data_integration.main` to refresh data.
2.  **Query Lake:** Use the CSVs in `src/data_integration/data_lake/processed/` to find parameters.
    *   *Example:* If the agents design a fragile nanobody, check `bioprinting_hub.csv` to ensure the printing temperature for your chosen hydrogel is $< 37^\circ C$.

## 5. Future Roadmap
1.  **Refine Tools:** Implement the `tools/materials_tools.py` wrapper.
2.  **Agent Prompting:** Update `nanobody_constants.py` with the new agent definitions.
3.  **Simulation:** Run a "Full Stack" meeting that starts with a sequence and ends with a 3D printing protocol.
