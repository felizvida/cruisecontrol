# Codex Zebrafish Brain Paper, 14 Rounds + External Review Loop

This folder is a fresh **Codex-only** build for the prompt:

> how does the proteome of specific, functionally distinct regions of the adult zebrafish brains, such as optic tectum vs telencephalon, differ, and how do these differences relate to their known biological functions?

The manuscript is now framed as a knowledge contribution, not just as a reconstruction of an older paper. Its central claim is that the released top-down proteomics dataset already supports a specific biological conclusion: adult zebrafish telencephalon and optic tectum have distinct proteoform profiles, and that split is organized in ways that match known regional function.

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
-> round27 paperreview.ai rereview returns Accept on paper/main_round26.pdf
-> round28 JPR-facing editorial pass shortens the paper, moves deeper computation into the appendix, and strengthens the biological framing
-> round29 abstract rewrite follows recent JPR abstract patterns and removes excess numerical detail from the opening summary
-> round30 paperreview.ai rereview evaluates paper/main_round29.pdf and returns a favorable assessment without a calibrated score for venue Other
-> round31 revision implements the round30 requests with a duplicate-based detectability model, conservative misidentification bounds, ProForma-oriented canonicalization examples, and clearer figure/sample-size recap
-> round32 language pass replaces awkward phrasing with more natural biology prose and retitles the manuscript around proteoform profiles rather than proteoform regimes
-> round33 sentence-level prose revision replaces vague repository shorthand with concrete language about deposited spreadsheets, PRIDE, and the actual biological claims
-> round34 scientific-prose revision rewrites the abstract and core narrative so the paper reads as a direct biological argument rather than as annotated homework notes
-> round35 paperreview.ai rereview evaluates paper/main_round34.pdf and treats the manuscript as publishable after minor revision
-> round36 revision implements the round35 requests with clearer traceability, overlap-model assumptions, accession handling, prevalence-adjusted statistics, and detectability-model detail
-> round37 paperreview.ai rereview evaluates paper/main_round36.pdf and returns Accept with a last set of minor auditability and robustness requests
-> round38 revision implements the round37 requests with accession-level motor-family breakdown, gene-symbol sensitivity, stratified detectability checks, inverse acetylation modeling, and a minimal reproducibility notebook
-> round39 paperreview.ai rereview returns Weak Accept with requests for stronger fixed-margin formalization, count-normalized checks, and clearer processed-table limits
-> round40 revision implements the round39 requests with Jaccard null intervals, identification-count rarefaction, and clearer executable provenance
-> round41 updated-skill rewrite applies the latest local paper-write and classic-biology-prose guidance while preserving the computation-backed claim set
-> round42 paperreview.ai rereview evaluates paper/main_round41.pdf and returns Accept with minor revision requests on purity sentinels, canonicalization transparency, top-intensity checks, and notation cleanup
-> round43 response revision implements the round42 requests with tissue sentinels, top-intensity restrictions, full canonicalization maps, replicate-scope clarification, and notation cleanup
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
- `paper/main_round28.pdf`
- `paper/main_round29.pdf`
- `paper/main_round31.pdf`
- `paper/main_round32.pdf`
- `paper/main_round33.pdf`
- `paper/main_round34.pdf`
- `paper/main_round36.pdf`
- `paper/main_round38.pdf`
- `paper/main_round40.pdf`
- `paper/main_round41.pdf`
- `paper/main_round43.pdf`
- `review/round43_revision_summary.md`
- `review/round41_revision_summary.md`
- `review/round42_review.md`
- `review/round39_review.md`
- `review/round37_review.md`
- `review/round37_scorecard.json`
- `review/round35_review.md`
- `review/round35_scorecard.json`
- `review/round30_review.md`
- `review/round30_scorecard.json`
- `review/round27_review.md`
- `review/round27_scorecard.json`
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
- latest externally reviewed artifact: `paper/main_round41.pdf`
- latest completed external review: `round42` from `paperreview.ai`
- latest explicit external accept: `round42`
- latest unre-reviewed revision after external feedback: `paper/main_round43.pdf`
- external-review score: `not returned` for venue `Other`
- round21 submission status: blocked by `paperreview.ai` rate limit before a token was issued
- round26 submission status: blocked again by `paperreview.ai` rate limit before a token was issued
- last calibrated internal score: `9.4 / 10` on `paper/main_round14.pdf`
- validation: `12` pages, embedded fonts, and no `Overfull`, `Underfull`, `undefined`, warning, error, or `[VERIFY]` matches in the round43 build checks

Key final results:

- article-level proteoform Jaccard overlap: `0.0434`
- exact-ID proteoform Jaccard overlap: `0.0360`
- occupancy-adjusted shared exact IDs: `43.1859`
- occupancy-adjusted exact-ID Jaccard overlap: `0.0432`
- mass-tertile detectability-adjusted Jaccard overlap: `0.0451`
- intensity-tertile detectability-adjusted Jaccard overlap: `0.0445`
- exact-ID centered Jaccard relative to independence: `-0.2792`
- exact-ID lower-tail overlap significance: `5.56e-183`
- canonicalized proteoform Jaccard overlap: `0.0615`
- gene-symbol Jaccard overlap: `0.2302`
- gene-symbol centered Jaccard relative to independence: `-0.2034`
- 5% misidentification-adjusted exact-ID Jaccard ceiling: `0.0540`
- 10% misidentification-adjusted exact-ID Jaccard ceiling: `0.0725`
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
- motor-family skeletal/cardiac-like annotation fraction: `0.8625`
- marker-panel gene-collapsed alignment fraction: `0.9200`
- independent panel alignment fraction: `0.9143`
- independent panel one-sided exact `p`: `6.68e-04`
- MNAR-style weighted Jaccard range: `0.0456` to `0.0483`
- acetylation adjusted odds ratio: `2.94` with `p = 0.140`
- inverse acetylation-region odds ratio: `0.26` with `p = 0.180`
- first-residue<=2 acetylation recheck: odds ratio `0.88`, `p = 0.714`
- top-100 intensity-restricted exact-ID Jaccard overlap: `0.0526`
- top-100 intensity-restricted marker alignment: `1.0000`
- skeletal/cardiac muscle sentinel rows: `2` telencephalon, `89` optic tectum
- skeletal/cardiac muscle sentinel intensity share of each region: `0.042%` telencephalon, `11.0%` optic tectum
- canonicalization full-map rows: `842`
- cross-accession canonicalized sequence groups: `17`

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
- `paper/main_round28.pdf`
- `paper/main_round29.pdf`
- `paper/main_round31.pdf`
- `paper/main_round32.pdf`
- `paper/main_round33.pdf`
- `paper/main_round34.pdf`
- `paper/main_round36.pdf`
- `paper/main_round38.pdf`
- `paper/main_round40.pdf`
- `paper/main_round41.pdf`
- `paper/main_round43.pdf`
- `paper/PAPER_IMPROVEMENT_LOG.md`
- `review/round00_review.md` through `review/round13_review.md`
- `review/round15_review.md`
- `review/round16_review.md`
- `review/round17_review.md`
- `review/round18_review.md`
- `review/round19_review.md`
- `review/round20_review.md`
- `review/round35_review.md`
- `review/round37_review.md`
- `review/round30_review.md`
- `review/round27_review.md`
- `review/round39_review.md`
- `review/round39_revision_summary.md`
- `review/round41_revision_summary.md`
- `review/round43_revision_summary.md`
- `review/round42_paperreview_submission.json`
- `review/round42_paperreview_response.json`
- `review/round42_review.md`
- `review/round42_scorecard.json`
- `review/round21_submission_blocked.md`
- `review/round26_submission_blocked.md`
- `review/ROUND_REVIEWS_LIVE.md`
- `review/REVIEW_OPINION.md`
- `review/review_scorecard.json`
- `review/round15_paperreview_submission.json`
- `review/round16_paperreview_submission.json`
- `review/round17_paperreview_submission.json`
- `review/round18_paperreview_submission.json`
- `review/round35_paperreview_submission.json`
- `review/round35_paperreview_response.json`
- `review/round37_paperreview_submission.json`
- `review/round37_paperreview_response.json`
- `review/round30_paperreview_submission.json`
- `review/round30_paperreview_response.json`
- `review/round27_paperreview_submission.json`
- `review/round27_paperreview_response.json`
- `code/`
- `data/`
- `results/`
- `figure_assets/`

This example stays honest about scope. The biological claim rests on the deposited proteoform spreadsheets rather than on a new wet-lab run, but it is not just a packaging exercise. The paper now shows that the regional split remains visible after duplicate-based detectability correction, conservative misidentification bounds, gene-symbol and protein collapse, marker-panel stress tests, count-normalized rarefaction, fixed-margin overlap tests, top-intensity restriction, tissue-sentinel guardrails, and a standards-aware canonicalization pass. The package includes the internal 14-round loop, multiple live `paperreview.ai` rounds, the blocked round-21 rereview attempt, a round-22 reframing pass that turned the manuscript into a direct knowledge-claim paper, a round-23 cleanup pass that removed the remaining diminishing re-analysis/audit language, a round-24 prose pass that made the academic writing more natural, a round-25 style pass informed by classic molecular-biology prose, a round-26 final pass that tightened cadence and compression, the successful `round27` external rereview that returned `Accept` on `paper/main_round26.pdf`, a later `round28` editorial pass that shortened the paper and made the JPR-facing version more biology-first, a `round29` abstract pass, a `round30` external review and its `round31` response, the `round32` and `round33` language revisions, the `round34` scientific-prose rewrite, the `round35` external review and `round36` response revision, the later `round37` external `Accept`, the `round39` external `Weak Accept`, the `round40` response revision, the `round41` updated-skill rewrite, the `round42` external `Accept` on `paper/main_round41.pdf`, and the current `round43` response revision. The saved submission metadata redacts the email address and external-review handles before publication.

Submission support:

- `submission/COVER_LETTER_JPR.md`
- `submission/README.md`
- `submission/JPR_20_PAPER_STYLE_MAP.md`
- `submission/JPR_SUBMISSION_CHECKLIST.md`
- `review/JPR_COMPARISON_2026-03-24.md`
