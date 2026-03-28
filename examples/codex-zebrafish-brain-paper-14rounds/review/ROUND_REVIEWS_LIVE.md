# Round Reviews Live

This file summarizes the serialized review-driven path from the baseline paper through the completed `paperreview.ai` rounds, including the later successful rereview of `paper/main_round26.pdf`, the newer external review of `paper/main_round29.pdf`, and the current `paper/main_round31.pdf` revision that answers the latest external critique.

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

Current external-review state:

- latest externally reviewed artifact: `paper/main_round29.pdf`
- latest completed external verdict: `No calibrated score returned`
- latest completed external review: `review/round30_review.md`
- latest saved external response payload: `review/round30_paperreview_response.json`
- last explicit external `Accept`: `round27`
- current manuscript includes the later authorial framing passes recorded as `paper/main_round22.pdf`, `paper/main_round23.pdf`, `paper/main_round24.pdf`, `paper/main_round25.pdf`, the externally accepted `paper/main_round26.pdf`, the later JPR-facing editorial revision `paper/main_round28.pdf`, the abstract-refined and externally rereviewed `paper/main_round29.pdf`, and the current `paper/main_round31.pdf` revision implementing the round30 reviewer requests
- documented external submission blocks retained for provenance: `review/round21_submission_blocked.md` and `review/round26_submission_blocked.md`
- last calibrated internal score before the external loop: `9.4 / 10` on `paper/main_round14.pdf`
