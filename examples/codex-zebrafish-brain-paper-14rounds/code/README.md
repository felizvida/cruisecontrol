# Code Package

This example uses a small local computation stack:

- `../results/analyze_region_proteome.py`
  Computes article-level overlap, exact-ID and canonicalized source-table overlap, prevalence-adjusted overlap significance, duplicate-informed Chao2 and jackknife missingness sensitivity, MNAR-style low-intensity sensitivity, normalization-sensitive abundance similarities, marker-bias, axis-alignment, family-size-preserving permutation tests, an independent literature-derived marker panel, intensity-weighted and protein-collapsed robustness, PTM follow-up, covariate-adjusted acetylation sensitivity, composition guardrails, and technical-replicate summaries.

- `../results/render_figures.R`
  Generates publication-ready PDF, SVG, and 600 DPI PNG figure assets.

- `build_inputs.sh`
  Rebuilds the analysis outputs and figures.

- `build_paper.sh`
  Rebuilds the analysis outputs and recompiles the paper.

- `validate_artifacts.sh`
  Checks the final paper package, saved review chain, figure assets, and PDF metadata.

The analysis stage now also emits:

- `../results/source_table_metrics.json`
- `../results/abundance_normalization_sensitivity.csv`
- `../results/presence_overlap_significance.csv`
- `../results/discrepancy_diagnostic.csv`
- `../results/source_table_shared_ids.csv`
- `../results/source_table_proteoforms.csv`
- `../results/marker_family_membership.csv`
- `../results/marker_permutation_test.csv`
- `../results/independent_panel_marker_bias.csv`
- `../results/independent_panel_axis_summary.csv`
- `../results/independent_panel_sensitivity.csv`
- `../results/composition_guardrails.csv`
- `../results/ptm_scope_screen.csv`
- `../results/ptm_detectability_proxies.csv`
- `../results/acetylation_covariate_sensitivity.csv`
- `../results/mnar_similarity_sensitivity.csv`
- `../data/evidence_traceability.json`
