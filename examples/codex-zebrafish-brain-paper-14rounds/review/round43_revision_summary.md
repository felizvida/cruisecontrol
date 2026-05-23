# Round 43 Revision Summary

Date: 2026-05-23

Reviewed artifact: `paper/main_round41.pdf`

External review: `review/round42_review.md`

Revised artifact: `paper/main_round43.pdf`

Backend that supplied the review: `paperreview.ai`

## Reviewer Requests Addressed

1. Tissue-purity sentinel quantification was added through `results/tissue_purity_sentinels.csv` and `results/tissue_purity_sentinel_membership.csv`. The manuscript now states the skeletal/cardiac muscle sentinel burden directly and separates that signal from neuronal/synaptic and glial/myelin sentinel panels.
2. Canonicalization transparency was expanded through `results/canonicalization_full_map.csv`, `results/cross_accession_ambiguities.csv`, and appendix text spelling out the strict accession-plus-proteoform unit and the relaxed diagnostic rules.
3. Top-intensity robustness was added in `results/top_intensity_restriction.csv`. The paper now reports that restricting each region to its top 100 mean-intensity rows still leaves sparse exact-ID overlap and preserves marker-axis alignment.
4. Replicate structure was clarified in the Methods and Limits sections: the public files expose duplicate technical runs per region, not a biological-replicate design across animals.
5. P-value notation was normalized to standard scientific notation in the Results and sensitivity table.

## New Computed Outputs

- `results/tissue_purity_sentinels.csv`
- `results/tissue_purity_sentinel_membership.csv`
- `results/top_intensity_restriction.csv`
- `results/canonicalization_full_map.csv`
- `results/cross_accession_ambiguities.csv`

## Validation

The revised manuscript was rebuilt from the regenerated analysis outputs with `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`.

Checks passed:

- `paper/main.pdf` builds successfully.
- `paper/main_round43.pdf` was saved from the rebuilt PDF.
- PDF page count: `12`.
- Fonts are embedded.
- The LaTeX log has no `Overfull`, `Underfull`, `undefined`, `Warning`, or `Error` matches in the final check.
- The PDF text check found no unresolved `[VERIFY]`, `TODO`, `FIXME`, or `??` markers.

## External Review State

This is an author response revision to an external `Accept` review. It has not yet been externally rereviewed after the `round42` feedback.
