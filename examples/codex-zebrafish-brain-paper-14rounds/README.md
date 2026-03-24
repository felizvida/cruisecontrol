# Codex Zebrafish Brain Paper, 14 Rounds

This folder is a fresh **Codex-only** build for the prompt:

> how does the proteome of specific, functionally distinct regions of the adult zebrafish brains, such as optic tectum vs telencephalon, differ, and how do these differences relate to their known biological functions?

The artifact chain is:

```text
source curation -> local computation -> NARRATIVE_REPORT.md -> PAPER_PLAN.md
-> baseline paper -> 14 serialized review-driven rounds -> final paper package
```

Open these first:

- `paper/main.pdf`
- `submission/COVER_LETTER_JPR.md`
- `review/REVIEW_OPINION.md`
- `review/ROUND_REVIEWS_LIVE.md`
- `paper/PAPER_IMPROVEMENT_LOG.md`

Final status:

- route: `pure Codex`
- final paper: `paper/main.pdf`
- score: `9.4 / 10`
- verdict: `Accept for a reproducible re-analysis or data-note venue`
- validation: `10` pages, embedded fonts, and no `Overfull`, `Underfull`, or `undefined` matches in `paper/main.log`

Key final results:

- proteoform-level Jaccard overlap: `0.0434`
- protein-level overlap fraction: `0.2151`
- marker alignment fraction: `0.9766`
- expected alignment under regional prevalence: `0.5811`
- alignment excess over prevalence: `0.3955`
- family-level sign check: `9 / 9` families in the expected direction, one-sided `p = 0.001953`
- leave-one-out range: `0.9625` to `0.9911`

The final package includes:

- `paper/main.pdf`
- `paper/main_round0_original.pdf`
- `paper/main_round1.pdf` through `paper/main_round14.pdf`
- `paper/PAPER_IMPROVEMENT_LOG.md`
- `review/round00_review.md` through `review/round13_review.md`
- `review/ROUND_REVIEWS_LIVE.md`
- `review/REVIEW_OPINION.md`
- `review/review_scorecard.json`
- `code/`
- `data/`
- `results/`
- `figure_assets/`

This example stays honest about scope. It does not claim a new wet-lab experiment or a raw-data reprocessing pipeline. The paper is a computation-backed audit of a published regional proteomics pilot, with the full review trail preserved round by round.

Submission support:

- `submission/COVER_LETTER_JPR.md`
- `review/JPR_COMPARISON_2026-03-24.md`
