# Round 39 External Review Revision Summary

External backend: `paperreview.ai`

Reviewer disposition: `Weak Accept` for the current mass-spec manuscript, with requests for stronger formalization and clearer limits rather than a change in the central claim.

Revision actions:

- Added fixed-margin hypergeometric Jaccard null intervals to `results/presence_overlap_significance.csv`; the exact-ID observed Jaccard of 0.0360 remains far below the 95% null interval of 0.2890--0.3430.
- Added `results/identification_count_rarefaction.csv` to test whether unequal regional identification totals create the separation; subsampling optic tectum to the telencephalon count preserves low overlap and high marker-axis alignment.
- Surfaced executable provenance in the manuscript: `results/analyze_region_proteome.py`, `code/reproduce_tables_and_figures.ipynb`, canonicalization examples, marker-membership tables, and `data/evidence_traceability.json`.
- Revised the methods, results, discussion, and appendix to explain the fixed-margin baseline, count-normalized sampling, processed-table limits, PTM localization limits, and tissue-purity guardrails in direct paper prose.
- Preserved the central conclusion: adult zebrafish telencephalon and optic tectum have sharply distinct proteoform profiles whose marker direction follows known regional biology.
