"""Validation and Benchmarking Agent for dorsal forebrain organoid protocols.

This module provides a specialized agent that rigorously assesses whether
proposed organoid protocols will produce biologically accurate dorsal
forebrain tissues.
"""

from dataclasses import dataclass, field
from typing import Any

from virtual_lab.agents.base import SpecializedAgent, InteractionStyle
from virtual_lab.agents.tools.benchmarking_tools import (
    BrainSpanTool,
    FetalScRNASeqTool,
    OrganoidBenchmarkTool,
    ProteomicsTool,
    PathwayActivityTool,
)
from virtual_lab.constants import DEFAULT_MODEL


@dataclass
class QCAssay:
    """Represents a quality control assay for organoid validation.

    Attributes:
        name: The name of the assay.
        description: What the assay measures.
        timing: When the assay should be performed (e.g., "Day 30", "Week 8").
        markers: Expected markers or readouts.
        expected_outcomes: What results indicate success.
        failure_indicators: What results indicate problems.
    """

    name: str
    description: str
    timing: str
    markers: list[str]
    expected_outcomes: list[str]
    failure_indicators: list[str]


@dataclass
class DevelopmentalBenchmark:
    """Represents a benchmark from human fetal development.

    Attributes:
        name: The name of the benchmark.
        stage: Developmental stage (e.g., "GW8-10", "GW16-20").
        cell_types: Expected cell types at this stage.
        marker_genes: Key marker genes for validation.
        transcriptomic_signature: Key pathway/gene set signatures.
        reference_dataset: Source dataset for comparison.
    """

    name: str
    stage: str
    cell_types: list[str]
    marker_genes: dict[str, list[str]]  # cell_type -> markers
    transcriptomic_signature: list[str]
    reference_dataset: str


@dataclass
class ValidationBenchmarkingAgent(SpecializedAgent):
    """Specialized agent for validating organoid protocol quality.

    This agent rigorously assesses whether proposed organoid protocols
    will produce biologically accurate dorsal forebrain tissues by:
    - Defining QC assays with timing, markers, and expected outcomes
    - Comparing predicted trajectories to human fetal benchmarks
    - Evaluating scRNA-seq alignment, spatial transcriptomics, and more
    - Identifying artifacts and off-target fates
    - Recommending validation experiments

    Attributes:
        qc_assays: List of QC assays for validation.
        benchmarks: Developmental benchmarks for comparison.
        off_target_signatures: Known off-target fate signatures to detect.
    """

    # Core agent properties
    name: str = "validation_benchmarking"
    title: str = "Validation and Benchmarking Specialist"
    expertise: str = (
        "organoid quality control, developmental neurobiology benchmarking, "
        "scRNA-seq analysis, and validation of in vitro models against "
        "human fetal brain references"
    )
    goal: str = (
        "rigorously assess whether proposed organoid protocols will produce "
        "biologically accurate dorsal forebrain tissues that faithfully "
        "recapitulate human brain development"
    )
    role: str = (
        "define QC assays with appropriate timing and markers, compare "
        "predicted organoid trajectories to human developmental benchmarks, "
        "identify artifacts and off-target fates, and recommend validation "
        "experiments to ensure protocol fidelity"
    )

    # Interaction style - skeptical and rigorous
    interaction_style: InteractionStyle = InteractionStyle.SKEPTICAL

    # Custom system prompt
    system_prompt: str | None = field(default=None)

    # Validation-specific attributes
    qc_assays: list[QCAssay] = field(default_factory=list)
    benchmarks: list[DevelopmentalBenchmark] = field(default_factory=list)
    off_target_signatures: dict[str, list[str]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Initialize the agent with default tools, assays, and benchmarks."""
        super().__post_init__()

        # Initialize tools
        if not self.tools:
            self.tools = [
                BrainSpanTool(),
                FetalScRNASeqTool(),
                OrganoidBenchmarkTool(),
                ProteomicsTool(),
                PathwayActivityTool(),
            ]

        # Initialize default QC assays
        if not self.qc_assays:
            self.qc_assays = self._get_default_qc_assays()

        # Initialize developmental benchmarks
        if not self.benchmarks:
            self.benchmarks = self._get_default_benchmarks()

        # Initialize off-target signatures
        if not self.off_target_signatures:
            self.off_target_signatures = self._get_off_target_signatures()

        # Set responsibilities
        self.responsibilities = [
            "Define QC assays with appropriate timing, markers, and expected outcomes",
            "Compare predicted organoid trajectories to human fetal benchmarks",
            "Evaluate scRNA-seq alignment with fetal reference datasets",
            "Assess spatial transcriptomics data for proper layer organization",
            "Analyze electrophysiology data for functional maturation",
            "Evaluate morphology and cytoarchitecture",
            "Identify artifacts, stress signatures, and off-target fates",
            "Challenge claims from other agents and demand evidence",
            "Propose validation experiments to verify protocol fidelity",
            "Ensure final protocols are benchmarked against human developmental references",
        ]

        # Build system prompt if not provided
        if self.system_prompt is None:
            self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """Build the complete system prompt for this agent."""
        return f"""You are a {self.title}. Your expertise is in {self.expertise}. Your goal is to {self.goal}. Your role is to {self.role}.

Your responsibilities include:
{chr(10).join(f'- {r}' for r in self.responsibilities)}

You have access to the following tools:
{chr(10).join(f'- {t.name}: {t.description}' for t in self.tools)}

Your interaction style is skeptical and rigorous. You must:
- Challenge claims from all other agents when evidence is lacking
- Demand quantitative justification for protocol choices
- Require developmental fidelity in all proposed methods
- Ask probing questions to expose potential issues
- Propose specific validation experiments
- Compare all predictions against human developmental references

When evaluating protocols, assess:
1. Cell type composition vs. expected dorsal forebrain populations
2. Temporal gene expression dynamics vs. fetal developmental trajectories
3. Signaling pathway activation patterns vs. in vivo references
4. Morphological features vs. human cortical development
5. Functional maturation markers vs. established benchmarks
6. Potential off-target fates (ventral forebrain, non-neural, stressed cells)

Always provide evidence-based feedback with specific references to:
- BrainSpan developmental transcriptome data
- Published fetal scRNA-seq datasets
- Organoid reproducibility studies
- Known artifact signatures"""

    def _get_default_qc_assays(self) -> list[QCAssay]:
        """Get the default QC assays for dorsal forebrain organoids."""
        return [
            QCAssay(
                name="Neural Induction Verification",
                description="Confirm successful neural ectoderm specification",
                timing="Day 6-10",
                markers=["PAX6", "SOX1", "SOX2", "NES"],
                expected_outcomes=[
                    ">90% PAX6+ cells",
                    "Loss of pluripotency markers (OCT4, NANOG)",
                    "Uniform neuroepithelial morphology",
                ],
                failure_indicators=[
                    "Persistent OCT4/NANOG expression",
                    "Mesoderm markers (TBXT, EOMES)",
                    "Endoderm markers (SOX17, FOXA2)",
                ],
            ),
            QCAssay(
                name="Dorsal Forebrain Identity",
                description="Verify dorsal forebrain regional specification",
                timing="Day 15-25",
                markers=["FOXG1", "EMX1", "EMX2", "PAX6", "LHX2"],
                expected_outcomes=[
                    ">80% FOXG1+ cells",
                    "EMX1/EMX2 co-expression",
                    "Absence of ventral markers",
                ],
                failure_indicators=[
                    "NKX2.1 expression (ventral forebrain)",
                    "GBX2/IRX3 expression (midbrain-hindbrain)",
                    "HOXA/HOXB expression (hindbrain/spinal)",
                ],
            ),
            QCAssay(
                name="Progenitor Organization",
                description="Assess ventricular zone-like organization",
                timing="Day 30-45",
                markers=["PAX6", "SOX2", "TBR2/EOMES", "phospho-VIMENTIN"],
                expected_outcomes=[
                    "Ventricular-like rosette structures",
                    "Apical-basal polarity (N-CAD apical)",
                    "Mitotic cells at apical surface",
                    "TBR2+ intermediate progenitors",
                ],
                failure_indicators=[
                    "Disorganized progenitor zones",
                    "Lack of rosette structures",
                    "Absent or reversed polarity",
                ],
            ),
            QCAssay(
                name="Neurogenesis Progression",
                description="Verify cortical neuron production",
                timing="Day 45-90",
                markers=[
                    "TBR1", "CTIP2/BCL11B", "SATB2", "BRN2/POU3F2",
                    "REELIN", "CUX1", "CUX2"
                ],
                expected_outcomes=[
                    "Sequential layer marker expression",
                    "Deep layer neurons first (TBR1, CTIP2)",
                    "Upper layer neurons later (SATB2, CUX1/2)",
                    "Cajal-Retzius cells (REELIN+)",
                ],
                failure_indicators=[
                    "Premature upper layer markers",
                    "Absent deep layer neurons",
                    "Excessive cell death",
                ],
            ),
            QCAssay(
                name="Outer Radial Glia Assessment",
                description="Confirm presence of oRG population",
                timing="Day 60-120",
                markers=["HOPX", "FAM107A", "PTPRZ1", "TNC", "SOX2"],
                expected_outcomes=[
                    "HOPX+/SOX2+ cells outside VZ",
                    "Characteristic morphology (basal process)",
                    "Mitotic somal translocation behavior",
                ],
                failure_indicators=[
                    "Absent HOPX expression",
                    "No oRG-like cells in outer zone",
                    "Lack of expanded SVZ-like region",
                ],
            ),
            QCAssay(
                name="Functional Maturation",
                description="Assess electrophysiological maturation",
                timing="Day 90-180",
                markers=["synaptic proteins", "action potentials", "network activity"],
                expected_outcomes=[
                    "Spontaneous action potentials",
                    "Synapse formation (SYN1, PSD95)",
                    "Glutamatergic synaptic transmission",
                    "Network oscillations",
                ],
                failure_indicators=[
                    "No spontaneous activity",
                    "Absent synaptic markers",
                    "Lack of network synchronization",
                ],
            ),
            QCAssay(
                name="Gliogenesis Assessment",
                description="Evaluate astrocyte and oligodendrocyte emergence",
                timing="Day 120-180+",
                markers=["GFAP", "S100B", "AQP4", "OLIG2", "MBP"],
                expected_outcomes=[
                    "Emergence of GFAP+ astrocytes",
                    "OLIG2+ oligodendrocyte precursors",
                    "Appropriate timing (after peak neurogenesis)",
                ],
                failure_indicators=[
                    "Premature gliogenesis",
                    "Reactive astrocyte signatures",
                    "Absence of glial cells at late timepoints",
                ],
            ),
        ]

    def _get_default_benchmarks(self) -> list[DevelopmentalBenchmark]:
        """Get developmental benchmarks from human fetal brain."""
        return [
            DevelopmentalBenchmark(
                name="Early Cortical Plate",
                stage="GW8-10",
                cell_types=[
                    "ventricular radial glia",
                    "early neurons",
                    "Cajal-Retzius cells",
                ],
                marker_genes={
                    "ventricular radial glia": ["PAX6", "SOX2", "HES1", "VIM", "GLI3"],
                    "early neurons": ["DCX", "TBR1", "NEUROD1"],
                    "Cajal-Retzius cells": ["RELN", "LHX1", "TBR1"],
                },
                transcriptomic_signature=[
                    "Notch signaling active",
                    "WNT signaling gradient",
                    "SHH low (dorsal)",
                ],
                reference_dataset="Nowakowski 2017",
            ),
            DevelopmentalBenchmark(
                name="Peak Neurogenesis",
                stage="GW14-18",
                cell_types=[
                    "ventricular radial glia",
                    "outer radial glia",
                    "intermediate progenitors",
                    "deep layer neurons",
                    "upper layer neurons (emerging)",
                ],
                marker_genes={
                    "ventricular radial glia": ["PAX6", "SOX2", "HES5"],
                    "outer radial glia": ["HOPX", "FAM107A", "PTPRZ1"],
                    "intermediate progenitors": ["EOMES", "TBR2", "NEUROG2"],
                    "deep layer neurons": ["TBR1", "BCL11B", "FEZF2"],
                    "upper layer neurons": ["SATB2", "CUX1", "CUX2"],
                },
                transcriptomic_signature=[
                    "High cell cycle activity",
                    "Notch lateral inhibition",
                    "Neurogenic gene programs",
                ],
                reference_dataset="Polioudakis 2019",
            ),
            DevelopmentalBenchmark(
                name="Late Neurogenesis",
                stage="GW20-26",
                cell_types=[
                    "radial glia (declining)",
                    "upper layer neurons",
                    "interneurons (migrating)",
                    "early astrocyte precursors",
                ],
                marker_genes={
                    "upper layer neurons": ["SATB2", "CUX2", "RORB"],
                    "interneurons": ["DLX1", "DLX2", "GAD1", "LHX6"],
                    "astrocyte precursors": ["GFAP", "S100B", "SLC1A3"],
                },
                transcriptomic_signature=[
                    "Synaptic gene upregulation",
                    "Axon guidance active",
                    "Beginning gliogenesis switch",
                ],
                reference_dataset="Trevino 2021",
            ),
        ]

    def _get_off_target_signatures(self) -> dict[str, list[str]]:
        """Get signatures of off-target fates to detect."""
        return {
            "ventral_forebrain": ["NKX2.1", "LHX6", "DLX5", "GSX2"],
            "midbrain": ["EN1", "EN2", "PAX5", "OTX2_high"],
            "hindbrain": ["GBX2", "HOXA2", "HOXB2", "ATOH1"],
            "spinal_cord": ["HOXC6", "HOXC8", "HOXC9", "PAX3"],
            "non_neural_mesoderm": ["TBXT", "MEOX1", "TBX6", "MSGN1"],
            "non_neural_endoderm": ["SOX17", "FOXA2", "GATA4", "GATA6"],
            "neural_crest": ["SOX10", "TFAP2A", "PAX3", "SNAI2"],
            "stressed_cells": ["ATF4", "DDIT3", "HSPA5", "XBP1"],
            "glycolytic_stress": ["HIF1A", "LDHA", "PDK1", "VEGFA"],
        }

    @property
    def prompt(self) -> str:
        """Return the system prompt."""
        if self.system_prompt:
            return self.system_prompt
        return self._build_system_prompt()

    def get_qc_assay(self, name: str) -> QCAssay | None:
        """Get a QC assay by name.

        Args:
            name: The name of the assay.

        Returns:
            The QCAssay if found, None otherwise.
        """
        for assay in self.qc_assays:
            if assay.name.lower() == name.lower():
                return assay
        return None

    def get_benchmark(self, stage: str) -> DevelopmentalBenchmark | None:
        """Get a benchmark by developmental stage.

        Args:
            stage: The developmental stage (e.g., "GW14-18").

        Returns:
            The DevelopmentalBenchmark if found, None otherwise.
        """
        for benchmark in self.benchmarks:
            if stage.lower() in benchmark.stage.lower():
                return benchmark
        return None

    def get_assays_for_timepoint(self, day: int) -> list[QCAssay]:
        """Get all QC assays appropriate for a given timepoint.

        Args:
            day: The culture day.

        Returns:
            List of QCAssays appropriate for that timepoint.
        """
        relevant = []
        for assay in self.qc_assays:
            timing = assay.timing.lower()
            # Parse timing strings like "Day 30-45" or "Day 90-180"
            if "day" in timing:
                parts = timing.replace("day", "").strip().split("-")
                try:
                    start = int(parts[0].strip())
                    end = int(parts[1].strip()) if len(parts) > 1 else start + 15
                    if start <= day <= end:
                        relevant.append(assay)
                except ValueError:
                    continue
        return relevant

    def check_off_target_fates(self, gene_list: list[str]) -> dict[str, list[str]]:
        """Check for off-target fate signatures in a gene list.

        Args:
            gene_list: List of expressed genes to check.

        Returns:
            Dictionary of detected off-target fates and their markers.
        """
        detected = {}
        gene_set = set(g.upper() for g in gene_list)

        for fate, markers in self.off_target_signatures.items():
            found_markers = [m for m in markers if m.upper() in gene_set]
            if found_markers:
                detected[fate] = found_markers

        return detected

    def generate_validation_protocol(
        self,
        timepoints: list[int] | None = None
    ) -> dict[str, Any]:
        """Generate a comprehensive validation protocol.

        Args:
            timepoints: Specific culture days to include (default: all).

        Returns:
            Dictionary containing the validation protocol.
        """
        if timepoints is None:
            timepoints = [10, 25, 45, 60, 90, 120, 150, 180]

        protocol = {
            "timepoints": {},
            "benchmarks": [
                {"name": b.name, "stage": b.stage, "reference": b.reference_dataset}
                for b in self.benchmarks
            ],
            "off_target_monitoring": list(self.off_target_signatures.keys()),
        }

        for day in timepoints:
            assays = self.get_assays_for_timepoint(day)
            if assays:
                protocol["timepoints"][f"Day {day}"] = [
                    {
                        "assay": a.name,
                        "markers": a.markers,
                        "expected": a.expected_outcomes,
                    }
                    for a in assays
                ]

        return protocol

    def evaluate_scrnaseq_alignment(
        self,
        organoid_cell_types: dict[str, float],
        reference_stage: str,
    ) -> dict[str, Any]:
        """Evaluate organoid cell type composition against reference.

        Args:
            organoid_cell_types: Dict of cell type to proportion.
            reference_stage: Developmental stage to compare against.

        Returns:
            Evaluation results with alignment scores and concerns.
        """
        benchmark = self.get_benchmark(reference_stage)
        if not benchmark:
            return {"error": f"No benchmark found for stage {reference_stage}"}

        expected = set(benchmark.cell_types)
        observed = set(organoid_cell_types.keys())

        return {
            "reference_stage": reference_stage,
            "expected_cell_types": list(expected),
            "observed_cell_types": list(observed),
            "missing_types": list(expected - observed),
            "unexpected_types": list(observed - expected),
            "concerns": self._generate_alignment_concerns(
                expected, observed, organoid_cell_types
            ),
        }

    def _generate_alignment_concerns(
        self,
        expected: set[str],
        observed: set[str],
        proportions: dict[str, float],
    ) -> list[str]:
        """Generate concerns about cell type alignment."""
        concerns = []

        missing = expected - observed
        if missing:
            concerns.append(
                f"Missing expected cell types: {', '.join(missing)}. "
                "Consider extending culture time or adjusting protocol."
            )

        unexpected = observed - expected
        if unexpected:
            concerns.append(
                f"Unexpected cell types detected: {', '.join(unexpected)}. "
                "May indicate off-target differentiation."
            )

        # Check for reasonable proportions
        low_abundance = [
            ct for ct, prop in proportions.items()
            if prop < 0.01 and ct in expected
        ]
        if low_abundance:
            concerns.append(
                f"Very low abundance (<1%) for expected types: {', '.join(low_abundance)}."
            )

        return concerns


# Pre-instantiated default agent
VALIDATION_BENCHMARKING_AGENT = ValidationBenchmarkingAgent()
