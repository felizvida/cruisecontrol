# Round 18 paperreview.ai Review

Reviewed artifact: `examples/codex-zebrafish-brain-paper-14rounds/paper/main_round17.pdf`

Backend: `paperreview.ai`

Score: `not returned by paperreview.ai`

Verdict: `Accept`

## Summary

This paper presents a quantitative, reproducible re-analysis of a 2022 top-down proteomics pilot profiling adult zebrafish telencephalon and optic tectum. Using counts extracted from the article and proteoform tables from PRIDE, the authors quantify regional separation (low proteoform-level Jaccard and abundance-based similarities), formalize the source paper’s biological narrative as a matched-versus-spillover marker-alignment problem with exact/randomization tests, and provide duplicate-informed missingness sensitivity and PTM-layer follow-up. The work emphasizes auditability over new acquisition or raw-data reprocessing, and demonstrates that a modest published study can support a stronger and more transparent region-function argument.

## Strengths

- Technical novelty and innovation
  - A careful reframing of a narrative biological interpretation into explicit, auditable quantitative metrics (exact-ID vs canonicalized overlaps; marker matched/spillover analysis).
  - Introduction of duplicate-informed Chao2/jackknife sensitivity envelopes tailored to the information content of the released tables.
  - Transparent traceability: rule-based, machine-readable curation of marker families and accession+proteoform matching logic; reproducibility package with file-level provenance.
- Experimental rigor and validation
  - Multiple, complementary similarity measures (Jaccard, Sørensen, weighted Jaccard, Bray–Curtis) under several normalization regimes, with consistent “low overlap” conclusions.
  - Robustness of marker alignment demonstrated via exact directional tests, effect-size intervals, family-size-preserving randomization, leave-one-out analyses, protein collapse, and intensity weighting.
  - Sensitivity analyses addressing reviewer-style concerns (pessimistic reassignment of matched counts, exclusion of potential contamination-prone families, sentinel purity checks).
- Clarity of presentation
  - Clear statement of scope and limits: no new wet-lab data or raw-feature reprocessing; strongest claims restricted to a curated, interpretable marker panel.
  - Crisp accounting of the 35 vs 29 shared-proteoform discrepancy and a well-motivated canonicalization diagnostic that bounds the plausible range.
  - Straightforward, interpretable effect sizes (e.g., alignment fractions, odds ratios) that connect statistics to biological expectations.
- Significance of contributions
  - Strengthens the evidential basis of a prior study and models good practice for turning small spatial proteomics pilots into reproducible, auditable analyses.
  - Highlights the biological informativeness of proteoform-level resolution and shows region-linked PTM structure (N-terminal acetylation).
  - Provides a generally useful template for quantitative re-analysis in proteomics where raw pipelines may be inaccessible.

## Weaknesses

- Technical limitations or concerns
  - Reliance on a curated marker panel (~15% of counts) leaves the broader proteome untested; correlations among proteoforms within families may violate independence assumptions in some tests.
  - Ecological richness estimators (Chao2, jackknife) are applied under constraints (only duplicate incidence available), with potential violations of assumptions (heterogeneous detectability, misidentification).
  - Canonicalization that strips PTM annotations can merge biologically distinct proteoforms; matching rule choices may affect overlap estimates in nontrivial ways.
- Experimental gaps or methodological issues
  - No raw-feature reprocessing or global FDR/localization assessment; conclusions depend on the fidelity of released tables and article-side thresholds.
  - Abundance normalization limited to global scalings; more model-based approaches (e.g., EigenMS, censoring-aware methods) are not explored and may affect similarity metrics in presence of nonrandom missingness.
  - PTM bias analysis tests acetylation robustly but does not address detectability biases that could differ by region (e.g., N-termini coverage, proteoform size/charge).
- Clarity or presentation issues
  - While thorough, inclusion of future-leaning spatial-omics foundation-model references is tangential and might distract from the focused re-analysis narrative.
  - Some statistical details (e.g., how zeros/missing intensities were treated across runs for Bray–Curtis or weighted Jaccard) could be spelled out more precisely for full reproducibility.
- Missing related work or comparisons
  - Statistical normalization/missingness literature in proteomics (e.g., censoring-aware models; SVD/EigenMS) could be more directly connected to the chosen normalization strategies and their assumptions.
  - Richness estimation under misclassification (extensions adjusting Q1/Q2 for identification error) could be acknowledged as a possible refinement in the presence of proteoform misidentification.

## Detailed Comments

- Technical soundness evaluation
  - The overlap and abundance-similarity metrics are standard and appropriate; the convergence of multiple measures toward “low overlap” strengthens validity.
  - The duplicate-informed sensitivity analyses are carefully bounded given available incidence counts; the fixed-shared and scaled-shared scenarios are a reasonable envelope under incomplete cross-region co-detection information.
  - The marker alignment framing is statistically well-posed; the use of directional exact tests is justified by directional biological hypotheses. Family-size-preserving randomization is a strong, assumption-light check against circularity.
  - Caveat: ecological estimators (Chao2/jackknife) assume homogeneous detection or at least interpretable incidence structures; in proteomics, detectability and misidentification can be structured. Stating these assumptions and potential biases is appreciated, but confidence in exact numeric lower bounds should remain cautious.
- Experimental evaluation assessment
  - The normalization variants (per-run total intensity, upper quartile, median ratio) are reasonable baselines and show stability of conclusions; with only two technical runs per region, more sophisticated approaches may not be identifiable but could be acknowledged as future work if richer replication becomes available.
  - Sensitivity stress tests (matched-to-spillover reassignment; family exclusions) are convincing and materially strengthen claims of robustness.
  - PTM analysis is conservative: acetylation was pre-specified, “other mass shifts” collapsed as exploratory with Holm adjustment. Still, potential region-dependent detectability biases for N-termini warrant discussion or a sensitivity check (e.g., size/charge distributions or fragmentation quality proxies).
- Comparison with related work (using the summaries provided)
  - The emphasis on auditability and data reuse aligns with concerns about MS data disappearance and the opportunity for re-analysis highlighted in 2407.00117; this paper is a concrete demonstration in that spirit.
  - Treatment of normalization and missingness connects to Karpievitch et al. (1101.1154); the authors’ choice of global scalings is practical for small-n settings, but the discussion could more explicitly reference censoring-aware frameworks and SVD-based bias removal as aspirational alternatives when replication permits.
  - The CE-MS and top-down context is broadly consistent with 1910.13819 and 1309.0988; noting the CZE-MS/MS modality’s role in enabling proteoform-level identification supports the paper’s focus on proteoform-resolved signals.
  - The paper’s missingness-sensitivity framing resonates with broader ML perspectives on missingness robustness (2406.16484) and with single-cell proteomics challenges around sensitivity and missing values (2502.11982). While not directly applied here, acknowledging these connections strengthens the generality of the approach.
  - Richness estimation under misclassification (2012.07485) suggests a potential refinement path: adjusting Q1/Q2 for misidentification if validation subsets or decoy-based error estimates can be integrated.
  - The foundation-model context (2601.12381) is not central to the present contribution but positions the work as complementary: transparent proteoform-specific accounting versus large-scale representation learning.
- Discussion of broader impact and significance
  - The paper provides a practical template for transforming small proteomics studies into reusable, auditable analyses—valuable for communities prioritizing reproducibility and transparent biological interpretation.
  - By keeping proteoforms explicit, it underscores the importance of PTM-resolved biology in spatial contexts and motivates better sharing of feature-level histories and FDR/localization metadata.
  - The approach could generalize to other regions or organisms and serve as a bridge until richer raw exports or atlases are available, potentially informing future standards for data deposition and post hoc analysis.

## Questions

1. Please specify the exact canonicalization rules with illustrative before/after examples. In particular, how do you prevent merging biologically distinct proteoforms when stripping bracketed PTMs and punctuation?
2. How are missing intensities handled when computing weighted Jaccard and Bray–Curtis (e.g., absent in one run vs true zero)? Were any imputation or pseudo-count strategies applied?
3. Can you clarify whether the PRIDE tables and the article’s 35-shared count were filtered with identical FDR/localization thresholds? If not, could threshold differences explain part of the 35 vs 29 discrepancy?
4. For the PTM analysis, did you assess region-dependent detectability biases (e.g., N-terminus coverage, precursor mass/charge, fragmentation quality) that could inflate apparent acetylation differences?
5. Could you report uncertainty for overlap metrics (e.g., bootstrapped Jaccard intervals under sampling of identified proteoforms or runs) to complement point estimates?
6. How were the sentinel purity markers selected, and can you provide a full list and counts by region to allow readers to judge coverage and potential bias?
7. If additional replicate-level information becomes available, would you consider richer normalization (e.g., EigenMS) or censoring-aware models to test whether the abundance-similarity conclusions persist?
8. Do your traceability files include software versions, environment details, and a permanent repository link/DOI to ensure long-term reproducibility?

## Overall Assessment

This is a careful and useful re-analysis that converts a qualitative regional-function narrative into a quantitative, auditable argument using publicly released tables and transparent local computations. The central findings—very low proteoform-level overlap between telencephalon and optic tectum, strong alignment of curated marker families with expected regions, and a regionally structured PTM signal—are well supported by multiple metrics, robustness checks, and sensitivity analyses that directly anticipate reviewer concerns. The scope is intentionally limited: no new acquisitions or raw-feature reprocessing, and strongest claims restricted to a curated panel. Within these boundaries, the contribution is solid, clearly presented, and valuable to a community seeking reproducibility and proteoform-resolved biological insight from modest datasets. I recommend acceptance, contingent on minor clarifications regarding canonicalization rules, intensity handling, and PTM detectability considerations.
