"""Constants for the organoid validation project.

This module defines all configuration for running validation meetings
for dorsal forebrain organoid protocols.
"""

from pathlib import Path

from virtual_lab.agent import Agent
from virtual_lab.prompts import SCIENTIFIC_CRITIC
from virtual_lab.agents import VALIDATION_BENCHMARKING_AGENT

# =============================================================================
# Meeting Configuration
# =============================================================================

num_iterations = 3  # Number of parallel discussion iterations
num_rounds = 2      # Number of discussion rounds per meeting

# =============================================================================
# Model Configuration
# =============================================================================

# Using OpenAI models (same as nanobody_design)
model = "gpt-4o-2024-08-06"
model_mini = "gpt-4o-mini-2024-07-18"

# =============================================================================
# Directory Structure
# =============================================================================

discussions_dir = Path("discussions")

# Workflow phases for organoid validation
workflow_phases = [
    "protocol_review",           # Initial review of proposed protocol
    "qc_assay_definition",       # Define QC assays and timing
    "benchmark_comparison",      # Compare to fetal benchmarks
    "off_target_assessment",     # Identify potential off-target fates
    "validation_experiments",    # Propose validation experiments
    "final_recommendations",     # Final protocol recommendations
]

# Create phase directories
discussions_phase_to_dir = {
    phase: discussions_dir / phase for phase in workflow_phases
}

# =============================================================================
# Background Prompts
# =============================================================================

background_prompt = """You are working on a research project to develop
dorsal forebrain organoids that faithfully recapitulate human cortical
development. The goal is to create reproducible, biologically accurate
organoid protocols that can be used for disease modeling, drug screening,
and understanding human brain development."""

organoid_context_prompt = """The team is developing a protocol for generating
dorsal forebrain organoids from human pluripotent stem cells. The protocol
should produce organoids containing the expected cell types (radial glia,
intermediate progenitors, cortical neurons) with proper spatial organization
and developmental timing that matches human fetal brain development."""

# =============================================================================
# Agent Definitions
# =============================================================================

# Team Lead - Principal Investigator
principal_investigator = Agent(
    title="Principal Investigator",
    expertise="stem cell biology and brain organoid development",
    goal="develop reproducible organoid protocols that accurately model human brain development",
    role="lead a team of experts to validate organoid protocols, make key decisions about quality control criteria, and ensure protocols meet developmental benchmarks",
    model=model,
)

# Scientific Critic (from prompts.py)
scientific_critic = SCIENTIFIC_CRITIC

# Validation & Benchmarking Specialist (our new agent)
# Convert to base Agent for compatibility with run_meeting
validation_specialist = VALIDATION_BENCHMARKING_AGENT.to_base_agent()

# Additional specialized agents for the team
developmental_biologist = Agent(
    title="Developmental Biologist",
    expertise="human cortical development and neurogenesis",
    goal="ensure organoid protocols recapitulate key aspects of human fetal brain development",
    role="provide expertise on developmental timing, cell type emergence, and morphogenetic processes",
    model=model,
)

stem_cell_specialist = Agent(
    title="Stem Cell Specialist",
    expertise="pluripotent stem cell culture and directed differentiation",
    goal="optimize stem cell handling and differentiation protocols for robust organoid generation",
    role="advise on media formulations, growth factors, and culture conditions for consistent results",
    model=model,
)

computational_analyst = Agent(
    title="Computational Biologist",
    expertise="single-cell RNA-seq analysis and transcriptomic benchmarking",
    goal="provide quantitative analysis of organoid transcriptomes against fetal references",
    role="analyze scRNA-seq data, perform trajectory analysis, and benchmark against BrainSpan and fetal datasets",
    model=model,
)

# =============================================================================
# Team Configurations
# =============================================================================

# Full validation team
validation_team_members = (
    validation_specialist,
    developmental_biologist,
    stem_cell_specialist,
    computational_analyst,
    scientific_critic,
)

# Focused QC team (smaller for faster iterations)
qc_team_members = (
    validation_specialist,
    developmental_biologist,
    scientific_critic,
)

# Benchmarking team
benchmarking_team_members = (
    validation_specialist,
    computational_analyst,
    scientific_critic,
)

# =============================================================================
# QC Markers Reference (for prompts)
# =============================================================================

# Key markers organized by category
DORSAL_FOREBRAIN_MARKERS = {
    "neural_induction": ["PAX6", "SOX1", "SOX2", "NES"],
    "dorsal_identity": ["FOXG1", "EMX1", "EMX2", "LHX2"],
    "radial_glia": ["PAX6", "SOX2", "HES1", "VIM", "GFAP"],
    "outer_radial_glia": ["HOPX", "FAM107A", "PTPRZ1", "TNC"],
    "intermediate_progenitors": ["EOMES", "TBR2", "NEUROG2"],
    "deep_layer_neurons": ["TBR1", "BCL11B", "CTIP2", "FEZF2"],
    "upper_layer_neurons": ["SATB2", "CUX1", "CUX2", "BRN2"],
    "cajal_retzius": ["REELIN", "LHX1", "TBR1"],
    "interneurons": ["DLX1", "DLX2", "GAD1", "LHX6"],
    "astrocytes": ["GFAP", "S100B", "AQP4", "SLC1A3"],
    "oligodendrocytes": ["OLIG2", "MBP", "SOX10"],
}

OFF_TARGET_MARKERS = {
    "ventral_forebrain": ["NKX2.1", "LHX6", "DLX5", "GSX2"],
    "midbrain": ["EN1", "EN2", "PAX5", "OTX2"],
    "hindbrain": ["GBX2", "HOXA2", "HOXB2"],
    "non_neural": ["TBXT", "SOX17", "FOXA2"],
    "stress_markers": ["ATF4", "DDIT3", "HSPA5"],
}

# =============================================================================
# Developmental Timepoints
# =============================================================================

# Standard QC timepoints (culture days)
QC_TIMEPOINTS = [10, 25, 45, 60, 90, 120, 150, 180]

# Mapping to approximate gestational weeks
DAY_TO_GW_APPROXIMATE = {
    10: "~GW5-6",
    25: "~GW7-8",
    45: "~GW9-11",
    60: "~GW12-14",
    90: "~GW16-18",
    120: "~GW20-22",
    150: "~GW24-26",
    180: "~GW28+",
}

# =============================================================================
# Example Protocol (for testing)
# =============================================================================

EXAMPLE_PROTOCOL = """
Dorsal Forebrain Organoid Protocol (Draft):

Day 0-6: Neural Induction
- Dissociate hPSCs to single cells
- Embed in Matrigel domes
- Culture in neural induction medium (dual SMAD inhibition)
- SB431542 (10 μM) + LDN193189 (100 nM)

Day 6-15: Dorsal Patterning
- Switch to patterning medium
- Add cyclopamine (1 μM) to inhibit SHH
- Maintain in low-attachment plates

Day 15-45: Early Organoid Expansion
- Transfer to spinning bioreactor
- Neural maintenance medium
- Media changes every 3 days

Day 45+: Maturation
- Continue in bioreactor
- Optional: Add BDNF/NT3 for neuronal maturation
- Long-term culture up to 180+ days
"""
