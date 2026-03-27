# Latest Review Opinion

Reviewed artifact: `paper/main_round20.pdf`

Current final artifact: `paper/main_round26.pdf`

Backend: `paperreview.ai`

Score: `not returned by paperreview.ai`

Verdict: `No calibrated score returned`

## Summary

The latest completed external review was `round20` on `paper/main_round20.pdf`. It remained broadly positive about the paper's value, but it asked for another substantive revision pass before the package should be treated as fully settled. The strongest reviewer asks were:

1. a prevalence-adjusted overlap significance analysis instead of descriptive Jaccard alone
2. a minimal MNAR-aware sensitivity for the intensity similarities
3. a simple confounding check for the acetylation result using public detectability proxies
4. a small independently curated marker panel not inherited from the source paper

## What Changed In `main_round22.pdf`

The current frozen artifact `paper/main_round26.pdf` preserves those scientific revisions and adds later authorial passes that reframe the manuscript as a direct knowledge contribution rather than as a reconstruction exercise.

1. Added a prevalence-adjusted overlap-significance analysis using a fixed-margin lower-tail hypergeometric test and centered Jaccard reporting in `results/presence_overlap_significance.csv`.
2. Added a minimal MNAR-style low-intensity sensitivity in `results/mnar_similarity_sensitivity.csv`.
3. Added a coarse covariate-adjusted acetylation sensitivity and a first-residue-restricted recheck in `results/acetylation_covariate_sensitivity.csv`.
4. Added an independent literature-derived panel built from adult zebrafish CNS myelin markers and adult optic-tectum radial-glia markers in `results/independent_panel_*.csv`.
5. Revised the manuscript so the acetylation claim is now explicitly weaker and more honest: suggestive in the raw counts, but not robust after covariate-sensitive follow-up.

## Current Recommendation

The regional-separation and marker-alignment core of the paper is now stronger than it was at `round20`. In particular:

- the low-overlap conclusion is now backed by both descriptive and prevalence-adjusted significance views
- the biological alignment story now survives both the source-paper marker panel and an independent literature-derived composition panel
- the PTM section is more trustworthy because it became more conservative instead of forcing a positive result

The main unresolved external-review issue is not scientific at this moment. It is operational: `paperreview.ai` rate-limited the attempted `round21` submission before returning a token, and it did the same thing again for `round26` after the later style and framing passes. Later authorial revisions produced `paper/main_round22.pdf`, `paper/main_round23.pdf`, `paper/main_round24.pdf`, `paper/main_round25.pdf`, and `paper/main_round26.pdf`, but those artifacts remain externally unreviewed because the service did not issue a token for either blocked submission.

## Remaining Honest Limits

1. The strongest biological claim still rests on released summary tables rather than a raw-feature or raw-file reprocessing workflow.
2. The marker-alignment results are strong, but they still summarize curated subsets rather than the full latent proteome.
3. The acetylation contrast should now be read as hypothesis-generating only.
4. The package still lacks an archival DOI, and the planned next external rereview is currently blocked by the external service rather than by the paper itself.
