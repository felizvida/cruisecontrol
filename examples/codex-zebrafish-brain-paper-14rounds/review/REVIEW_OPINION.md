# Latest Review Opinion

Reviewed artifact: `paper/main_round36.pdf`

Current final artifact: `paper/main_round38.pdf`

Backend: `paperreview.ai`

Score: `not returned by paperreview.ai`

Verdict: `Accept`

## Summary

The latest completed external review is `round37` on `paper/main_round36.pdf`. `paperreview.ai` again did not return a calibrated numeric score for venue `Other`, but the verdict was explicitly `Accept`. The reviewer still asked for a tighter final pass before submission, and those requests have now been implemented in `paper/main_round38.pdf`. The round37 requests were:

1. give a direct accession-by-accession breakdown of the myosin and troponin families so the contamination question can be assessed in concrete terms
2. report how much the regional split changes after collapsing to gene symbols, not only after protein collapse
3. surface Bray--Curtis and related abundance-aware similarities more explicitly in the main results
4. test the duplicate-based detectability correction under simple heterogeneity stratifications rather than only a single homogeneous model
5. show that the acetylation conclusion is unchanged when the logistic model is written in the inverse orientation
6. add a compact notebook alongside the code and environment bundle so an outside reader can walk through the main tables and figures quickly

## What The Latest Revision Added

`paper/main_round38.pdf` responds directly to the latest external review by adding:

1. `results/motor_family_breakdown.csv`, which expands the myosin and troponin families to the accession level and shows that most of those observations are skeletal- or cardiac-muscle-like annotations
2. `results/gene_symbol_sensitivity.csv`, which shows that the regional split remains strong even after the full dataset is collapsed to gene symbols
3. explicit Bray--Curtis ranges and a gene-collapse paragraph in the main Results section, so the biology is no longer framed only through binary exact-ID overlap
4. `results/detectability_stratified_sensitivity.csv`, which repeats the duplicate-based overlap correction after mass-tertile and intensity-tertile stratification and shows only small changes relative to the homogeneous model
5. an inverse acetylation model in `results/acetylation_covariate_sensitivity.csv`, which reaches the same cautious conclusion as the original orientation
6. a minimal reproducibility notebook at `code/reproduce_tables_and_figures.ipynb`

## What The Accepted Review Recognized

The latest external review specifically credited the paper for:

1. exact-ID, canonicalized, prevalence-adjusted, and protein-collapsed views that all support the same low-overlap conclusion
2. marker-panel alignment that remains strong under family-preserving randomization, conservative spillover perturbations, and an independent literature-derived panel
3. disciplined treatment of PTMs, especially the decision to weaken rather than force the acetylation claim after detectability-aware sensitivity work
4. transparent provenance and a bounded statement of what the deposited spreadsheets can and cannot support
5. a concise narrative that foregrounds biological separation rather than workflow mechanics

## Current Recommendation

The paper remains in a strong submission state. In particular:

- the low-overlap conclusion is now backed by both descriptive and prevalence-adjusted significance views
- the biological alignment story now survives both the source-paper marker panel and an independent literature-derived composition panel
- the motor-family concern is now bounded more explicitly, and the regional axis still holds after those families are removed
- the PTM section is more trustworthy because it became more conservative instead of forcing a positive result
- the latest reviewer's requests have now been addressed in the current manuscript, so the next useful step is rereview rather than another speculative rewrite

The earlier `round21` and `round26` submission blocks remain part of the package history, but they are no longer the current state. A later retry succeeded, returned a token, and produced the accepted `round27` review on `paper/main_round26.pdf`. That was followed by `round30` on `paper/main_round29.pdf`, `round35` on `paper/main_round34.pdf`, and the current accepted external review `round37` on `paper/main_round36.pdf`. None of those later `Other` submissions returned a calibrated numeric score, but `round37` is now the latest explicit external `Accept`.
The manuscript has since moved through `paper/main_round36.pdf`, received the `round37` external `Accept`, and has now been revised again as `paper/main_round38.pdf`. The current manuscript has implemented the round37 requests, but it has not yet gone back out for external rereview.

## Remaining Honest Limits

1. The strongest biological claim still rests on released summary tables rather than a raw-feature or raw-file reprocessing workflow.
2. The marker-alignment results are strong, but they still summarize curated subsets rather than the full latent proteome.
3. The acetylation contrast should now be read as hypothesis-generating only.
4. The package still lacks an archival DOI, even though the repository URL and traceability files are now surfaced more clearly.
5. The current manuscript has not yet been externally rereviewed after the round37-response revision in `paper/main_round38.pdf`.
