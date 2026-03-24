# Paper Plan

## Title

Function Follows Proteoform: A Computation-Backed Re-analysis of Adult Zebrafish Telencephalon and Optic Tectum Top-Down Proteomics

## Paper Type

Short computational biology / proteomics re-analysis note

## Claims-Evidence Matrix

| Claim | Evidence | Section |
|-------|----------|---------|
| Adult telencephalon and optic tectum are sharply separated at the proteoform level | Region totals, unique fractions, Jaccard overlap, protein overlap | Results |
| The source paper's marker proteoforms align strongly with known regional function | Marker counts, log-bias values, exact-test result, leave-one-out robustness | Results |
| The pilot's technical sensitivity is strong enough to make small-region top-down proteomics biologically legible | Duplicate means, CVs, single-run high water mark, cells-per-run estimate | Methods + Results |
| The dataset is sufficiently PTM-rich to justify proteoform-level interpretation | PTM totals and composition | Results + Discussion |

## Section Plan

1. Introduction
   - Motivate why region-function legibility matters in spatial proteomics.
   - Introduce telencephalon and optic tectum as contrasting adult zebrafish brain regions.
   - State that this paper re-analyzes published counts rather than producing new wet-lab measurements.

2. Data and Analysis Setup
   - Describe the source paper and local curated evidence file.
   - Explain derived metrics: Jaccard overlap, specialization fractions, log-bias, exact-test table, robustness, PTM burden.
   - Clarify the limits of the curated-marker analysis.

3. Results
   - Region separation.
   - Function-aligned marker concentration.
   - PTM inventory and technical sensitivity.

4. Discussion
   - Explain what the re-analysis adds beyond the source paper's narrative presentation.
   - Emphasize conservative scope.
   - Point to future raw-data and multi-region extensions.

5. Conclusion
   - Close on reproducible function-legibility as a useful frame for small proteomics pilots.

6. Reproducibility Appendix
   - File inventory, formulas, and provenance note.

## Figures

| Figure | Data source | Purpose |
|--------|-------------|---------|
| Fig. 1 `fig1_region_overview.pdf` | `results/region_summary.csv` | Show total and unique/shared separation |
| Fig. 2 `fig2_marker_bias.pdf` | `results/marker_bias.csv` | Show marker-level regional bias |
| Fig. 3 `fig3_axis_alignment.pdf` | `results/axis_summary.csv`, `results/leave_one_out_alignment.csv` | Show axis-level concentration and robustness |
| Fig. 4 `fig4_ptm_and_sensitivity.pdf` | `results/ptm_summary.csv`, `results/technical_replicate_summary.csv` | Show PTM inventory and technical sensitivity |

