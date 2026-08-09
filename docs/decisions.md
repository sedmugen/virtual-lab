# Design Decisions

Key technical choices made in this project and the rationale behind them.

---

## 1. OpenAI Assistants API over Chat Completions

**Decision:** Use the Assistants API (beta threads) rather than plain Chat Completions.

**Rationale:** The Assistants API maintains conversation state server-side across
multiple runs. This enables the "shared thread" model where all agents in a meeting
see the same evolving conversation without manual context management. It also
supports native tool use (function calling) for the `pubmed_search` integration.

**Trade-off:** The Assistants API is more expensive and slower than stateless chat
calls, and the beta API surface has changed between library versions.

---

## 2. Multi-provider LLM Configuration

**Decision:** Abstract the provider behind a `get_config()` factory in `config.py`
rather than hard-coding OpenAI.

**Rationale:** The upstream `zou-group/virtual-lab` code assumed OpenAI exclusively.
Adding BigModel (GLM-4-Flash) and OpenRouter support allows cost-free experimentation
with a free-tier model during development before switching to GPT-4o for production
runs. Changing `ACTIVE_PROVIDER` is a single-line switch.

**Trade-off:** The Assistants API used for meeting orchestration is an OpenAI-specific
API. BigModel and OpenRouter compatibility applies only to the underlying model
selection — the beta threads endpoint may not be available on all providers.

---

## 3. Data Lake File-based Storage

**Decision:** Use a local file-based Data Lake (`data_lake/raw/`, `data_lake/processed/`)
rather than a database.

**Rationale:** For a research prototype, file-based storage is simpler to set up,
requires no database infrastructure, and is easily inspectable. Timestamped filenames
preserve audit trails of API responses.

**Trade-off:** Does not scale to large datasets or concurrent writes. A future version
should migrate to PostgreSQL for the structured store and a vector DB for semantic
search (see `data_integration_analysis/integration_plan.md`).

---

## 4. ESM → AlphaFold-Multimer → Rosetta Pipeline

**Decision:** Score nanobody candidates with three complementary models in sequence.

**Rationale:** ESM log-likelihood ratios are fast and sequence-based.
AlphaFold-Multimer adds structural context (interface pLDDT).
Rosetta provides physics-based binding energy (ΔG). The weighted combination
`WS = 0.2·ESM + 0.5·AF + 0.3·Rosetta` balances speed with accuracy.

**Trade-off:** The pipeline requires substantial compute (GPU for ESM and AlphaFold,
Rosetta licence). A 4-round design loop for 4 nanobodies produced 92 candidates total.
