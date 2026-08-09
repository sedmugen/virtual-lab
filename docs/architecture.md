# Architecture

Virtual Lab is composed of two loosely-coupled layers that can be used independently.

---

## Layer 1 — Meeting Orchestration

The core of the system is `run_meeting()` in `src/virtual_lab/run_meeting.py`.

```
Human Researcher
      │
      ▼
run_meeting(meeting_type, agenda, ...)
      │
      ├─ "team" meeting
      │      ├─ Principal Investigator  (team_lead)
      │      ├─ Immunologist             \
      │      ├─ ML Specialist             ├─ team_members (configurable)
      │      ├─ Computational Biologist  /
      │      └─ Scientific Critic
      │           └─ OpenAI Assistants API — shared Thread
      │
      └─ "individual" meeting
             ├─ Specialist Agent
             └─ Scientific Critic (automatic)
                  └─ OpenAI Assistants API — shared Thread

Optional tool: pubmed_search
  └─ NCBI E-utilities → PubMed Central full text

Outputs
  ├─ <save_dir>/<save_name>.json  (full discussion transcript)
  └─ <save_dir>/<save_name>.md   (human-readable Markdown)
```

### Meeting Flow

**Team meeting**
1. Start prompt injected into the shared Thread.
2. Team lead opens with initial thoughts.
3. Each team member speaks in turn (N rounds).
4. Team lead synthesises at the end of each round.
5. Final round: team lead writes a structured summary.

**Individual meeting**
1. Start prompt injected into the Thread.
2. Agent responds to the agenda.
3. Scientific Critic critiques.
4. Agent revises based on critique.
5. Repeat for N rounds.

---

## Layer 2 — Data Integration (this fork)

```
External Sources
  ├─ PubChem REST API
  ├─ Materials Project API (mp-api)
  ├─ HydrogelDB (OAI-PMH simulation)
  ├─ MatWeb (BeautifulSoup scraper)
  ├─ MatPortal REST API
  ├─ ChEBI REST API
  ├─ 3D Bioprinting Data Hub (CSV)
  └─ Signaling Pathways Project (CSV)
      │
      ▼
src/data_integration/main.py (orchestrator)
      │
      ├─ data_lake/raw/        ← timestamped raw dumps (JSON, CSV)
      └─ data_lake/processed/  ← cleaned, normalised DataFrames

Agent Tool Interface
  └─ src/virtual_lab/tools/formulation.py
       ├─ search_bioprinting_params(material_name) → str
       └─ suggest_hydrogel(application_type)       → str
```

### Phase 2 Formulation Vision (Planned)

After the Meeting Orchestration layer selects a nanobody candidate, a second
meeting phase uses the Data Integration layer to design a delivery system:

1. **Formulation Scientist** queries HydrogelDB → selects carrier hydrogel.
2. **Bio-Manufacturing Engineer** queries Bioprinting Hub → defines printing protocol.
3. **Toxicologist** queries Signaling Pathways + PubChem → assesses safety.

See `data_integration_analysis/integration_strategy_nanobody_lab.md` for full details.

---

## Key Design Decisions

See `docs/decisions.md` for rationale behind major technical choices.
