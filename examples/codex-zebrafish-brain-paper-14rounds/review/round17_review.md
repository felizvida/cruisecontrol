# Round 17 paperreview.ai Review

Reviewed artifact: `examples/codex-zebrafish-brain-paper-14rounds/paper/main_round16.pdf`

Backend: `paperreview.ai`

Score: `not returned by paperreview.ai`

Verdict: `No calibrated score returned`

## Summary

This paper presents a quantitative, reproducible re-analysis of a 2022 top-down proteomics pilot profiling two adult zebrafish brain regions (telencephalon and optic tectum). Using counts extracted from the paper and machine-readable proteoform tables released to PRIDE, the authors quantify regional separation, perform duplicate-informed missingness sensitivity, formalize a curated marker-panel alignment analysis, and examine PTM bias within matched markers. The central finding is a robustly low proteoform overlap between regions and a strong, auditable alignment of biologically expected marker families to their corresponding regions, with code and traceability artifacts provided.

## Strengths

- Technical novelty and innovation
  - Reframing a narrative interpretation into a quantitative, auditable analysis using exact-ID matching (accession+proteoform), multiple overlap metrics (Jaccard, Sørensen, Bray-Curtis), and intensity-weighted variants.
  - Incorporation of duplicate-informed Chao2-style sensitivity analysis to address undersampling and unseen richness—uncommon in re-analyses of top-down proteomics.
  - Explicit, reproducible curation and rule-based mapping of marker families, with machine-readable traceability and per-row provenance.

- Experimental rigor and validation
  - Systematic cross-checks between article-level counts and released source tables, revealing and transparently reporting a 35 vs. 29 shared-proteoform discrepancy.
  - Robustness checks: leave-one-out family analysis, exclusion of motor-related families (contamination stress test), pessimistic reassignment of matched counts to spillover, protein-level collapse, and intensity weighting.
  - Clear restriction of claims to what the public tables support, avoiding overreach into raw data inferences.

- Clarity of presentation
  - Methodological steps and derived metrics are explained clearly; key formulas (overlaps, bias, tests) are specified and tied to outputs.
  - Results are structured to answer likely reviewer objections, with a well-communicated “auditability” emphasis and claim-to-evidence mapping.

- Significance of contributions
  - Demonstrates that small, published spatial top-down proteomics datasets can yield stronger, verifiable biological inferences when reframed with transparent computations.
  - Encourages community standards for releasing analyzable tables and traceability files to strengthen interpretability of pilot-scale studies.

## Weaknesses

- Technical limitations or concerns
  - Heavy reliance on a curated marker panel that originates from the source article raises selection-bias and circularity concerns, despite the thoughtful stress tests.
  - Chao2 methodology and its assumptions may not fully match MS proteoform detection processes; cross-region duplicate co-detection is not available, limiting interpretability of the sensitivity envelopes.
  - Intensity comparability is assumed through mean duplicate intensities; no explicit normalization across runs/regions is detailed, which may affect abundance-based similarity metrics.

- Experimental gaps or methodological issues
  - No proteome-wide statistical assessment or FDR-controlled differential analysis; conclusions remain at the level of curated markers and aggregate overlap metrics.
  - PTM analysis focuses on N-terminal acetylation within the matched marker subset; it is unclear whether this was pre-specified or selectively reported among possible PTMs, and multiple-hypothesis controls are not discussed.
  - Lack of explicit controls for confounders like regional cell-type composition differences or tissue purity beyond the motor-family exclusion test.

- Clarity or presentation issues
  - The paper would benefit from an explicit summary of normalization choices for intensities and a brief rationale for metric selection (e.g., why Bray-Curtis plus weighted Jaccard, and how they complement the exact-ID Jaccard).
  - The 35 vs. 29 shared-proteoform discrepancy is acknowledged but not traced to plausible causes (data versioning, ID canonicalization, accession mapping differences); a short diagnostic would further increase trust.

- Missing related work or comparisons
  - Limited engagement with broader literature on statistical treatment of species/proteoform incidence in MS contexts (e.g., Good–Turing/iChao extensions, occupancy models) and alternative normalization or similarity measures common in omics (e.g., CSS, TMM, compositional approaches).
  - The spatial foundation-model references are conceptually helpful but remain tangential; a clearer bridge to how this proteoform-level auditability paradigm can inform or augment such models would improve contextualization.

## Detailed Comments

- Technical soundness evaluation
  - The exact-ID overlap approach is appropriate and clearly stricter than string-only matching; reporting both article-level and table-level overlaps is good practice.
  - The use of Jaccard/Sørensen for incidence and Bray-Curtis/weighted Jaccard for abundance is standard; however, intensity comparability assumptions should be justified (e.g., per-run normalization, scaling).
  - The Chao2 lower-bound estimation is a reasonable first step for unseen richness, but its assumptions (incidence sampling, independence) may be strained in MS proteoform detection. The sensitivity “envelope” that scales shared overlap by region-specific inflation factors is pragmatic but could be supplemented by parametric or bootstrap nulls.
  - The marker alignment analysis is statistically convincing on its own terms (e.g., Fisher’s exact test, confidence intervals) and is strengthened by multiple robustness checks (leave-one-out, family exclusions, protein collapse). The potential for selection bias remains a caveat.

- Experimental evaluation assessment
  - The re-analysis is meticulous within the constraints of public tables and does not overclaim. Stress tests are thoughtful and directly address reviewer-salient concerns (contamination, undersampling).
  - Reporting recovery fractions, duplicate statistics (q1, q2), and a single-run high-water mark contextualizes detection sensitivity well for a pilot.
  - Adding uncertainty estimates or resampling-based intervals for overlap metrics would further improve the quantitative rigor.

- Comparison with related work (using the summaries provided)
  - The paper positions itself relative to TopPIC-based pipelines (Choi and Liu, 2022) and to the Lubeckyj and Sun (2022) study it re-analyzes. It also cites a follow-on zebrafish brain top-down study (Askarani et al., 2025), indicating ongoing relevance of proteoform-level signals.
  - The inclusion of spatial-omics foundation models (KRONOS/HEIST) provides macro context but not methodological integration; a tighter link would clarify complementary roles (e.g., using proteoform-level auditability to validate or interpret embeddings learned by foundation models).

- Discussion of broader impact and significance
  - The study models a reproducible, auditable path from small-scale proteomics reports to stronger biological claims, which is valuable for community standards and meta-analysis culture.
  - The focus on proteoform-level distinctions and PTM-aware interpretations underscores why top-down workflows can reveal biology that protein-level summaries might dilute.
  - While the scientific novelty is incremental, the reproducibility and auditability contribution is timely and of practical importance, especially for pilot studies or under-resourced labs.

## Questions

1. Marker panel: Were the included PTMs and marker families pre-specified prior to analysis, and how was the risk of selection bias addressed? Could you provide results of permutation tests that preserve family sizes but randomize region labels to quantify expected alignment under null?
2. Intensity handling: How were the duplicate intensity values normalized across runs and regions before computing weighted Jaccard and Bray-Curtis? Would alternative normalization (e.g., quantile, median-ratio, or compositional transforms) change the abundance-based similarities materially?
3. Chao2 assumptions: Why was Chao2 chosen over iChao or other incidence/abundance estimators for unseen richness in MS contexts? Can you provide sensitivity to alternative unseen-species models or to different assumptions about cross-region co-detection?
4. Shared-proteoform discrepancy: Can you diagnose the 35 (article) vs. 29 (exact-ID tables) difference—e.g., differences in accession canonicalization, isoform mapping, table filtering, or software versions?
5. Contamination and cell-type composition: Beyond excluding motor-related families, can you quantify tissue purity or approximate cell-type composition differences between regions (e.g., via known housekeeping or glial markers) to guard against confounds?
6. Multiple testing: For the PTM analysis (N-terminal acetylation), did you examine additional PTM classes? If yes, how did you control for multiple comparisons; if not, can you pre-register acetylation as a primary hypothesis and provide rationale?
7. Generalizability: Do you plan to extend the framework to raw TopPIC exports or to additional brain regions/datasets? What is needed to turn this into a proteome-wide, FDR-aware analysis while keeping the same level of auditability?

## Overall Assessment

This is a careful, well-executed re-analysis that strengthens and audits the biological interpretation of a small but influential zebrafish brain top-down proteomics pilot. The authors are transparent about scope, provide clear metrics, and conduct thoughtful sensitivity and robustness checks. The work’s primary contribution lies in reproducibility and interpretability rather than new methodological advances or new data. For a top-tier venue, the scientific novelty is moderate, and the impact is bounded by the curated marker focus and lack of raw-feature reprocessing. Nonetheless, the paper models good practices for quantitative auditing of small spatial proteomics datasets, and the clear connection between proteoform-level distinctions and regional function is of genuine interest. With added clarity on intensity normalization, unseen-richness modeling, and the shared-ID discrepancy—as well as a brief treatment of multiple testing for PTMs—this would be a solid contribution. I view it as a valuable, if niche, addition to the literature on proteoform-aware spatial proteomics and reproducible analysis.
