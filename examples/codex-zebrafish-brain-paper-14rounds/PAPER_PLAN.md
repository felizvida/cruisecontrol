# Paper Plan

## Title

Distinct Proteoform Profiles Mark Adult Zebrafish Telencephalon and Optic Tectum

## Paper Type

Short computational biology / proteomics paper based on public top-down proteomics tables

## Claims-Evidence Matrix

| Claim | Evidence | Section |
|-------|----------|---------|
| Adult telencephalon and optic tectum are sharply separated at the proteoform level | Article counts, strict exact-ID overlap, canonicalized diagnostics, fixed-margin nulls, protein and gene collapse | Results |
| Region-linked marker proteoforms align strongly with known regional function | Marker counts, exact test, family-size-preserving permutation, leave-one-out robustness, motor-family exclusion | Results |
| The separation survives review-requested robustness checks | Count-normalized rarefaction, duplicate-based detectability correction, misidentification ceilings, top-intensity restrictions, tissue-sentinel guardrails | Methods + Results |
| The dataset is PTM-rich, but the acetylation contrast should remain provisional | PTM totals, matched-marker acetylation, covariate model, inverse model, first-residue check | Results + Discussion |

## Section Plan

1. Introduction
   - Motivate why region-function legibility matters in spatial proteomics.
   - Introduce telencephalon and optic tectum as contrasting adult zebrafish brain regions.
   - State that this paper analyzes public processed tables rather than producing new wet-lab measurements.

2. Data and Analysis Setup
   - Describe the article, supplement, and deposited PRIDE region spreadsheets.
   - Explain derived metrics: exact-ID overlap, fixed-margin Jaccard nulls, canonicalization diagnostics, marker alignment, robustness checks, and PTM sensitivity.
   - Clarify technical-run scope and the absence of biological-replicate design in the public files.

3. Results
   - Region separation.
   - Function-aligned marker concentration.
   - PTM richness, technical sensitivity, and acetylation caution.

4. Discussion
   - Explain why proteoform-level identifiers preserve regional information that protein-level summaries partly blur.
   - Emphasize conservative scope, including tissue-purity and processed-table limits.
   - Point to future raw-feature, purity-measured, and multi-region extensions.

5. Conclusion
   - Close on distinct proteoform profiles as molecular signatures of the regions' different work.

6. Reproducibility Appendix
   - File inventory, formulas, and provenance note.

## Figures

| Figure | Data source | Purpose |
|--------|-------------|---------|
| Fig. 1 `fig1_region_overview.pdf` | `results/region_summary.csv` | Show total and unique/shared separation |
| Fig. 2 `fig2_marker_bias.pdf` | `results/marker_bias.csv` | Show marker-level regional bias |
| Fig. 3 `fig3_axis_alignment.pdf` | `results/axis_summary.csv`, `results/leave_one_out_alignment.csv` | Show axis-level concentration and robustness |
| Fig. 4 `fig4_ptm_and_sensitivity.pdf` | `results/ptm_summary.csv`, `results/technical_replicate_summary.csv` | Show PTM inventory and technical sensitivity |

## Review-Driven Tables

| Output | Purpose |
|--------|---------|
| `results/tissue_purity_sentinels.csv` | Quantify review-requested muscle, contractile, neuronal/synaptic, glial/myelin, and housekeeping sentinel panels |
| `results/tissue_purity_sentinel_membership.csv` | Expose row-level sentinel memberships |
| `results/top_intensity_restriction.csv` | Test whether low overlap and marker alignment persist among high-intensity rows |
| `results/canonicalization_full_map.csv` | Surface the raw-to-canonical identifier map |
| `results/cross_accession_ambiguities.csv` | List canonicalized sequence groups that appear under more than one accession |
