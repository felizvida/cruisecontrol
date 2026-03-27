# Codex Zebrafish Brain Paper, 14 Rounds + External Review Loop

This folder is a fresh **Codex-only** build for the prompt:

> how does the proteome of specific, functionally distinct regions of the adult zebrafish brains, such as optic tectum vs telencephalon, differ, and how do these differences relate to their known biological functions?

The manuscript is now framed as a knowledge contribution, not just as a reconstruction of an older paper. It argues that the public top-down proteomics record already supports a specific new claim: adult zebrafish telencephalon and optic tectum occupy sharply distinct proteoform regimes, and that split is biologically organized in ways that match known regional function.

The artifact chain is:

```text
source curation -> local computation -> NARRATIVE_REPORT.md -> PAPER_PLAN.md
-> baseline paper -> 14 serialized internal review rounds
-> paperreview.ai review -> round15 revision
-> paperreview.ai review -> round17 revision
-> paperreview.ai accept -> round18 clarification pass
-> paperreview.ai review -> round19 revision
-> paperreview.ai review -> round20 revision
-> round21 frozen revision implementing round20 requests
-> round21 paperreview.ai retry blocked by service rate limit
-> round22 authorial reframing pass positioning the paper as a direct knowledge contribution
-> round23 language pass removing the remaining diminishing re-analysis/audit framing
-> round24 prose pass rewriting the high-level framing into more natural academic language
-> round25 style pass informed by Monod, Jacob, Brenner, Stent, and Crick
-> round26 final style pass tightening cadence and compression
-> round26 paperreview.ai retry blocked by service rate limit
```

Open these first:

- `paper/main.pdf`
- `paper/main_round20.pdf`
- `paper/main_round21.pdf`
- `paper/main_round22.pdf`
- `paper/main_round23.pdf`
- `paper/main_round24.pdf`
- `paper/main_round25.pdf`
- `paper/main_round26.pdf`
- `review/round19_review.md`
- `review/round20_review.md`
- `review/round21_submission_blocked.md`
- `review/round26_submission_blocked.md`
- `review/REVIEW_OPINION.md`
- `review/ROUND_REVIEWS_LIVE.md`
- `paper/PAPER_IMPROVEMENT_LOG.md`

Final status:

- route: `pure Codex`
- final paper: `paper/main.pdf`
- latest externally reviewed artifact: `paper/main_round20.pdf`
- latest completed external review: `round20` from `paperreview.ai` with no calibrated numeric score for venue `Other`
- latest explicit external accept: `round19`
- latest frozen artifact awaiting external rereview: `paper/main_round26.pdf`
- round21 submission status: blocked by `paperreview.ai` rate limit before a token was issued
- round26 submission status: blocked again by `paperreview.ai` rate limit before a token was issued
- last calibrated internal score: `9.4 / 10` on `paper/main_round14.pdf`
- validation: `18` pages, embedded fonts, and no `Overfull`, `Underfull`, or `undefined` matches in `paper/main.log`

Key final results:

- article-level proteoform Jaccard overlap: `0.0434`
- exact-ID proteoform Jaccard overlap: `0.0360`
- exact-ID centered Jaccard relative to independence: `-0.2792`
- exact-ID lower-tail overlap significance: `5.56e-183`
- canonicalized proteoform Jaccard overlap: `0.0615`
- protein-level overlap fraction: `0.2151`
- marker alignment fraction: `0.9766`
- expected alignment under regional prevalence: `0.6904`
- alignment excess over prevalence: `0.2861`
- odds ratio with approximate 95% CI: `1173.0` (`102.0` to `13495.1`)
- family-size-preserving permutation upper bound: `p < 5e-06`
- family-level sign check: `9 / 9` families in the expected direction, one-sided `p = 0.001953`
- leave-one-out range: `0.9625` to `0.9911`
- review-driven sensitivity floor: `0.9297`
- motor-family exclusion alignment: `0.9310`
- independent panel alignment fraction: `0.9143`
- independent panel one-sided exact `p`: `6.68e-04`
- MNAR-style weighted Jaccard range: `0.0456` to `0.0483`
- acetylation adjusted odds ratio: `2.94` with `p = 0.140`
- first-residue<=2 acetylation recheck: odds ratio `0.88`, `p = 0.714`

The final package includes:

- `paper/main.pdf`
- `paper/main_round0_original.pdf`
- `paper/main_round1.pdf` through `paper/main_round14.pdf`
- `paper/main_round15.pdf`
- `paper/main_round16.pdf`
- `paper/main_round17.pdf`
- `paper/main_round18.pdf`
- `paper/main_round19.pdf`
- `paper/main_round20.pdf`
- `paper/main_round21.pdf`
- `paper/main_round22.pdf`
- `paper/main_round23.pdf`
- `paper/main_round24.pdf`
- `paper/main_round25.pdf`
- `paper/main_round26.pdf`
- `paper/PAPER_IMPROVEMENT_LOG.md`
- `review/round00_review.md` through `review/round13_review.md`
- `review/round15_review.md`
- `review/round16_review.md`
- `review/round17_review.md`
- `review/round18_review.md`
- `review/round19_review.md`
- `review/round20_review.md`
- `review/round21_submission_blocked.md`
- `review/round26_submission_blocked.md`
- `review/ROUND_REVIEWS_LIVE.md`
- `review/REVIEW_OPINION.md`
- `review/review_scorecard.json`
- `review/round15_paperreview_submission.json`
- `review/round16_paperreview_submission.json`
- `review/round17_paperreview_submission.json`
- `review/round18_paperreview_submission.json`
- `code/`
- `data/`
- `results/`
- `figure_assets/`

This example stays honest about scope. It does not claim a new wet-lab experiment or a raw-data reprocessing pipeline. Its claim is narrower and more defensible: a public proteoform dataset can yield a real new regional-organization statement once the overlap structure, marker architecture, missingness sensitivity, and confounding checks are made explicit. The package includes the internal 14-round loop, multiple live `paperreview.ai` rounds, the blocked round-21 rereview attempt, a round-22 reframing pass that turned the manuscript into a direct knowledge-claim paper, a round-23 cleanup pass that removed the remaining diminishing re-analysis/audit language, a round-24 prose pass that made the academic writing more natural, a round-25 style pass informed by classic molecular-biology prose, a round-26 final pass that tightened cadence and compression, and a second blocked `paperreview.ai` rereview attempt on `paper/main_round26.pdf`. The saved submission metadata redacts the email address and keeps the returned review token local to this working copy.

Submission support:

- `submission/COVER_LETTER_JPR.md`
- `review/JPR_COMPARISON_2026-03-24.md`
