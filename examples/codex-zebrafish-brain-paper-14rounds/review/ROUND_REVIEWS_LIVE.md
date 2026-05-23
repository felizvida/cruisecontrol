# Round Reviews Live

This file summarizes the serialized review-driven path from the baseline paper through the completed `paperreview.ai` rounds, including the later successful rereview of `paper/main_round26.pdf`, the later external review of `paper/main_round29.pdf`, and the current `paper/main_round41.pdf` revision sequence.

| Round reviewed | Score | Verdict | Main issue pushed into next round |
| --- | ---: | --- | --- |
| `round00` | 6.6 | Borderline | missing explicit contributions, clearer methods, technical table, tighter abstract scope |
| `round01` | 7.1 | Weak Borderline | no prevalence baseline for alignment; robustness not quantified enough |
| `round02` | 7.5 | Weak Accept | count-weighted alignment could still be dominated by large families |
| `round03` | 7.9 | Weak Accept | technical sensitivity needed normalization to regional totals |
| `round04` | 8.1 | Accept with Minor Revision | literature-to-function bridge should be explicit in one place |
| `round05` | 8.3 | Accept with Minor Revision | reproducibility commands and output map were still implicit |
| `round06` | 8.4 | Accept with Minor Revision | marker-panel curation rule was not stated plainly enough |
| `round07` | 8.5 | Accept with Minor Revision | leave-one-out table needed to be visible inside the paper package |
| `round08` | 8.6 | Accept with Minor Revision | narrow marker-panel scope needed a quantitative, not only verbal, bound |
| `round09` | 8.8 | Accept | limitations needed a clearly labeled subsection |
| `round10` | 9.0 | Accept | main claims, evidence, and limits needed a single audit table |
| `round11` | 9.1 | Accept | title and summary language lagged behind the paper’s audit-note identity |
| `round12` | 9.2 | Accept | readers still needed a quick map from claims to exact local files |
| `round13` | 9.3 | Accept | final package still needed cleaner appendix formatting and a broader closing sentence |
| `round14` via `paperreview.ai` | -- | No calibrated score returned | add odds-ratio CI, explicit curation/misclassification stress tests, contamination stress test, clearer family-level scope, and stronger missingness/TopPIC discussion |
| `round15` via `paperreview.ai` | -- | Borderline | next issues are source-location mapping, metric-choice rationale beyond Jaccard, unseen-overlap bracketing, PTM-to-function linkage, and broader spatial-omics context |
| `round16` via `paperreview.ai` | -- | No calibrated score returned | add marker-panel circularity control, alternative normalization rationale, discrepancy diagnostic, purity guardrail, and multiple-testing discipline for PTMs |
| `round17` via `paperreview.ai` | -- | Accept | remaining work is minor clarification only: canonicalization examples, missing-intensity handling, PTM detectability caveat, sentinel-list explicitness, and reproducibility metadata |
| `round19` via `paperreview.ai` | -- | Accept | next issues are standards-based overlap significance, reviewer-visible formula clarity, detectability proxies, and stronger reproducibility packaging |
| `round20` via `paperreview.ai` | -- | No calibrated score returned | add prevalence-adjusted overlap significance, MNAR-style intensity sensitivity, an independent literature-derived marker panel, and a stronger confounding check that may weaken the acetylation claim |
| `round21` submission attempt | -- | Blocked by rate limit | revised paper frozen as `paper/main_round21.pdf`, but `paperreview.ai` returned `Rate limit exceeded` before issuing a token |
| `round26` submission attempt | -- | Blocked by rate limit | style-refined manuscript frozen as `paper/main_round26.pdf`, but two live submission attempts both failed before token issuance |
| `round27` via `paperreview.ai` | -- | Accept | release fuller reproducibility details, make canonicalization and protein-collapse rules fully explicit, surface code/data links, and expand standards/context discussion |
| `round30` via `paperreview.ai` | -- | No calibrated score returned | next issues are occupancy-style detectability modeling, misidentification-sensitive uniqueness bounds, ProForma-aligned canonicalization, clearer figure/sample-size recap, and stronger standards-context positioning |
| `round31` author revision | -- | Pending rereview | implements the round30 requests with a duplicate-based occupancy model, conservative misidentification ceilings, standards-oriented canonicalization examples, and clearer figure/sample-size recap |
| `round32` author revision | -- | Pending rereview | replaces the last few awkward phrases with plainer biology prose and retitles the manuscript around proteoform profiles |
| `round33` author revision | -- | Pending rereview | replaces vague repository shorthand with concrete language about deposited spreadsheets, PRIDE, and the biological meaning of each result |
| `round34` author revision | -- | Pending rereview | rewrites the abstract and core narrative into a more authoritative scientific voice with less procedural self-explanation and a stronger biological lead |
| `round35` via `paperreview.ai` | -- | No calibrated score returned | publishability is no longer the main issue; the next round needed clearer reproducibility surfacing, a plainer detectability/acetylation-model description, explicit accession-conflict handling, stronger prevalence-adjusted overlap reporting, and broader spatial top-down context |
| `round36` author revision | -- | Pending rereview | implements the round35 requests with clearer traceability files, explicit overlap-model assumptions and statistics, fuller acetylation-model detail, stronger accession-handling language, and a broader spatial-top-down comparison |
| `round37` via `paperreview.ai` | -- | Accept | accepted after minor revision; the next round needed accession-level motor-family breakdown, gene-symbol collapse sensitivity, explicit Bray--Curtis reporting, stratified detectability checks, inverse acetylation modeling, and a minimal reproducibility notebook |
| `round38` author revision | -- | Pending rereview | implements the round37 requests with accession-level motor-family accounting, gene-symbol overlap and marker-collapse sensitivity, mass/intensity-stratified detectability bounds, inverse acetylation modeling, notebook-based reproducibility surfacing, and tighter standards-context prose |
| `round39` via `paperreview.ai` | -- | Weak Accept | next issues are fixed-margin formalization, count-normalized checks, clearer code and canonicalization surfacing, and sharper limits around processed-table analysis and tissue purity |
| `round40` author revision | -- | Pending rereview | implements the round39 requests with Jaccard null intervals, identification-count rarefaction, clearer executable provenance, and stronger processed-table and contamination guardrails |
| `round41` author revision | -- | Pending rereview | applies the updated local paper-writing and classic-biology-prose guidance while preserving the computation-backed claim set |
| `round42` via `paperreview.ai` | -- | Accept | accepted after minor revision; next issues are tissue-purity sentinel quantification, canonicalization and marker-membership transparency, top-intensity restrictions, and notation cleanup |
| `round43` author revision | -- | Pending rereview | implements the round42 requests with tissue-purity sentinel tables, top-intensity restrictions, full canonicalization maps, replicate-scope clarification, and cleaned p-value notation |

Current external-review state:

- latest externally reviewed artifact: `paper/main_round41.pdf`
- latest completed external verdict: `Accept`
- latest completed external review: `review/round42_review.md`
- latest saved external response payload: `review/round42_paperreview_response.json`
- latest explicit external `Accept`: `round42`
- latest unre-reviewed author response artifact: `paper/main_round43.pdf`
- current manuscript includes the later authorial framing passes recorded as `paper/main_round22.pdf`, `paper/main_round23.pdf`, `paper/main_round24.pdf`, `paper/main_round25.pdf`, the externally accepted `paper/main_round26.pdf`, the later JPR-facing editorial revision `paper/main_round28.pdf`, the abstract-refined and externally rereviewed `paper/main_round29.pdf`, the `paper/main_round31.pdf` revision implementing the round30 reviewer requests, the `paper/main_round32.pdf` language pass, the `paper/main_round33.pdf` sentence-level prose revision, the `paper/main_round34.pdf` scientific-prose revision, the `paper/main_round36.pdf` revision implementing the round35 external review, the `paper/main_round38.pdf` revision implementing the round37 external review, the `paper/main_round40.pdf` revision implementing the round39 external review, the `paper/main_round41.pdf` updated-skill rewrite, and the current `paper/main_round43.pdf` response to the round42 external review
- documented external submission blocks retained for provenance: `review/round21_submission_blocked.md` and `review/round26_submission_blocked.md`
- last calibrated internal score before the external loop: `9.4 / 10` on `paper/main_round14.pdf`
