# Round 15 paperreview.ai Review

Reviewed artifact: `examples/codex-zebrafish-brain-paper-14rounds/paper/main_round14.pdf`

Backend: `paperreview.ai`

Score: `not returned by paperreview.ai`

Verdict: `No calibrated score returned`

## Summary

This paper presents a quantitative and reproducible re-analysis of a 2022 top-down proteomics pilot that profiled adult zebrafish telencephalon and optic tectum. Using counts extracted from the original publication (without new MS acquisition or raw-data reprocessing), the authors formalize region separation and a curated marker alignment analysis, reporting a very low proteoform-level Jaccard overlap (0.0434) and an extremely strong directional association of marker families with their biologically expected regions (odds ratio 1173; one-sided Fisher exact p = 5.12×10⁻²²). The contribution is a compact, auditable reframing of the source study’s qualitative claims into explicit, testable, and reproducible quantitative evidence.

## Strengths

- Technical novelty and innovation
  - Converts a scattered qualitative narrative into a clear quantitative framework (Jaccard overlap, specialization fractions, marker alignment fractions, Wilson intervals, and exact testing).
  - Provides a small, reproducible analysis package with code, data manifests, and an explicit claim-to-file map, improving auditability.
- Experimental rigor and validation
  - Uses conservative, pre-specified marker curation tied directly to the source paper’s stated biology, minimizing post hoc selection bias.
  - Multiple cross-checks: axis-level analysis, family-level sign-style test, and leave-one-out robustness all point in the same direction.
- Clarity of presentation
  - The scope is explicitly delimited; claims are carefully framed around what can be supported by published counts.
  - Metrics and effect sizes are stated plainly and accompanied by interpretable baselines (regional-prevalence “naive” baseline vs. observed alignment).
- Significance of contributions
  - Demonstrates how small pilot spatial proteomics datasets can be made more interpretable and reusable with minimal assumptions and transparent computation.
  - Emphasizes the proteoform layer (substantial PTM content), supporting the broader push in the community beyond protein-level summaries.

## Weaknesses

- Technical limitations or concerns
  - Heavy reliance on presence/absence counts and a curated marker panel that represents only ~15% of total counts; results may not generalize to the full proteome.
  - Potential dependence among proteoforms within families is not fully accounted for; the exact test treats counts as independent draws.
  - The extreme region separation (low Jaccard) could be inflated by undersampling and detection heterogeneity across regions; no correction for incomplete detection.
- Experimental gaps or methodological issues
  - No raw-data reprocessing or independent validation; conclusions rest entirely on count summaries taken from the original paper.
  - No intensity- or abundance-weighted analysis; proteoform detection counts may reflect instrument/identification biases rather than biology alone.
  - Baselines and nulls do not consider proteoform-specific detectability or protein length/chemistry, which can systematically bias presence/absence.
- Clarity or presentation issues
  - While reproducibility is emphasized, the paper relies on secondary extraction from the source text/figures; explicit lists of proteoform IDs and their mapping rules could be highlighted further in the main text (not only the appendix).
  - Some figure descriptions are textual (likely due to extraction), which makes visual assessment harder.
- Missing related work or comparisons
  - Limited discussion of alternative similarity/dissimilarity measures and undersampling-corrected indices (e.g., Chao-type estimators) for presence–absence data.
  - Sparse placement within broader spatial proteomics/top-down proteomics methodology literature and zebrafish neuroproteomics studies beyond the primary source.

## Detailed Comments

- Technical soundness evaluation
  - The statistical framing for curated markers is sound and conservative. Fisher’s exact test is appropriate for a 2×2 matched/spillover table, and Wilson intervals are a reasonable choice for proportions with small denominators.
  - The family-level sign-style check and leave-one-out analysis are welcome robustness steps, though they cannot fully resolve within-family correlation of counts or selection effects.
  - The Jaccard and specialization fractions are interpretable but sensitive to missingness. Without replicate-level detection probabilities or raw features, it is difficult to separate biology from detectability.
  - The strong PTM coverage supports the rationale for proteoform-level interpretation; however, PTM ambiguity and proteoform assignment uncertainties in top-down pipelines (e.g., localization confidence, FDR) are not re-examined here.
- Experimental evaluation assessment
  - The re-analysis is explicit about not being a raw-data study. Given this, the experimental assessment is necessarily limited to what can be inferred from published aggregate counts.
  - The exact-test result is compelling for the curated panel, but the broader regional separation claim would benefit from sensitivity analyses that simulate undersampling or employ bias-aware baselines.
  - The technical replicate numbers (means, CVs) are informative, yet aggregating to presence/absence limits their interpretability for overlap statistics. Access to per-replicate identifications would enable more principled uncertainty quantification.
- Comparison with related work (using the summaries provided)
  - The framing aligns with ongoing community efforts to improve reproducibility and auditability in omics by turning narrative claims into code-backed summaries. However, the paper would be strengthened by explicitly referencing methods for dissimilarity with imperfect detection and by contrasting top-down vs. bottom-up spatial proteomics comparability for zebrafish brain.
  - Additional context on prior zebrafish telencephalon/tectum proteomics or multi-omics spatial studies would help readers situate the contribution within a growing body of work.
- Discussion of broader impact and significance
  - The paper’s main value is methodological reframing and reproducibility rather than new biology. This is still impactful: it models a transparent path for small-scale spatial proteomics to support sharper, auditable claims.
  - The clarity with which the authors bound their claims and connect them to code, manifests, and rebuild instructions sets a good standard for secondary data analyses.
  - If extended to raw files and scaled to additional regions, the approach could facilitate a reusable benchmarking asset for spatial top-down proteomics.

## Questions

1. Can you provide (or more prominently surface) the exact list of proteoform IDs used per region and per marker family, along with any de-duplication and mapping rules from the source study to your curated evidence file?
2. How sensitive are the overlap and alignment metrics to plausible misclassification or small curation changes (e.g., reassigning one or two border-line proteoforms, adding/removing a small marker family)?
3. Did you consider undersampling-corrected similarity estimators (e.g., Chao-type Jaccard/Sørensen) to mitigate missingness bias in presence/absence? If so, how do the conclusions change?
4. Could some of the optic-tectum marker counts (e.g., myosin, troponin, actin) reflect contamination from adjacent muscle or non-neuronal tissues? Can you incorporate a contamination check or discuss tissue purity controls?
5. Would an abundance-weighted variant of the alignment analysis (e.g., using spectral counts or intensities if recoverable) change the effect sizes or conclusions relative to presence/absence?
6. Can you report confidence intervals for key effect sizes beyond Wilson intervals (e.g., odds ratio CI; bootstrap CIs for Jaccard/specialization), acknowledging the limitations of aggregate-level data?
7. How would you extend the analysis if you had the raw TopPIC outputs (e.g., per-feature FDRs, proteoform localization confidence)? Are there specific metrics you would prioritize to move from a pilot-scale to atlas-quality inference?

## Overall Assessment

This is a careful, well-scoped, and useful re-analysis that translates a previously qualitative spatial proteomics result into a compact, quantitative, and auditable argument. The work is not methodologically groundbreaking nor does it introduce new experimental data, but it convincingly demonstrates strong region separation and marker alignment using simple, transparent statistics that are appropriate for the curated scope. The authors are commendably explicit about limitations and avoid over-claiming beyond what the published counts can support. To reach the bar of a top-tier venue, I would encourage modest but important extensions: (i) incorporate bias-aware similarity metrics for presence/absence data to address undersampling; (ii) strengthen the null/baseline choices and uncertainty quantification; (iii) more thoroughly situate the work within related spatial proteomics methodology and zebrafish neurobiology literature; and (iv) consider a limited raw-data reprocessing supplement for at least one key analysis to demonstrate end-to-end reproducibility. Even without these, the paper provides tangible value to the community by modeling good analytical hygiene and sharpening the interpretation of a small yet informative pilot dataset.
