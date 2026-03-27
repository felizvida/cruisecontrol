# round20 Review

Reviewed artifact: `examples/codex-zebrafish-brain-paper-14rounds/paper/main_round20.pdf`

Backend: `paperreview.ai`

Score: `not returned by paperreview.ai`

Verdict: `No calibrated score returned`

## Summary

This paper presents a quantitative, fully traceable re-analysis of a 2022 top-down proteomics pilot of adult zebrafish telencephalon and optic tectum. Using both article-extracted counts and the publicly released Tel2/Teo2 proteoform tables, the authors quantify regional separation with multiple overlap and abundance metrics, reconcile a discrepancy between published and table-derived overlaps via canonicalized matching, and formalize the source paper’s qualitative “marker alignment” narrative into explicit matched-versus-spillover statistical tests and robustness checks. The study also examines a focused PTM signal (N-terminal acetylation) within the curated marker panel, and provides a reproducible analysis package emphasizing auditability over new acquisition or raw-data reprocessing.

## Strengths

- Technical novelty and innovation
  - Treats a small, previously qualitative story as a transparent, quantitative, and reproducible analysis, including exact accession+proteoform overlap, intensity-weighted similarities, and duplicate-informed missingness sensitivity (Chao2/jackknife).
  - Introduces a family-size-preserving randomization test and multiple discrepancy diagnostics (strict vs canonicalized matching) that make the provenance issues interpretable rather than opaque.
  - Offers an explicit, auditable pipeline with machine-readable traceability for marker curation and metric computation.
- Experimental rigor and validation
  - Multiple, convergent measures of regional separation (Jaccard, Sørensen, weighted Jaccard, Bray–Curtis) across several normalization schemes and run-pair views; bootstrap sensitivity reported.
  - Robustness checks address common reviewer concerns: contamination (excluding motor families), pessimistic reassignment of counts, protein-level collapse, and intensity weighting.
  - Duplicate-informed richness bounds (Chao2/jackknife) used to probe unseen-proteoform inflation; conclusions remain stable.
- Clarity of presentation
  - Clear articulation of scope limits (no raw reprocessing; curated markers) and what can and cannot be inferred from public tables.
  - Transparent discussion of the 35-versus-29 shared-proteoform discrepancy with plausible representation-based reconciliation.
  - Careful statistical framing of marker alignment (odds ratios, Wilson intervals, exact tests) and limited multiple-testing steps for PTM analysis.
- Significance of contributions
  - Provides a model for turning modest, pilot-scale spatial top-down data into a more trustworthy, auditable analysis, which is valuable for a community struggling with reproducibility and interpretability.
  - Highlights that region-resolved proteoform profiles can show strong separation and function-aligned marker distributions, motivating future, deeper top-down studies.

## Weaknesses

- Technical limitations or concerns
  - Conclusions rest on technical replicates and a single published dataset with no biological replication; regional generalization is therefore limited.
  - Chao2/jackknife incidence-based richness estimation is constrained by only two runs per region; higher-order incidence corrections are not identifiable and estimates may be unstable.
  - The proteoform string handling is ad hoc (canonicalization heuristic) rather than adopting a formal ProForma 2.0 or Proteoform Registry mapping; this may under- or over-match edge cases.
- Experimental gaps or methodological issues
  - Overlap comparisons rely on raw/normalized intensities without modeling MNAR missingness; more formal prevalence-adjusted or MNAR-aware statistics could reduce residual biases.
  - The curated marker panel, while transparently defined, inherits selection from the original paper’s interpretation; despite randomization safeguards, some circularity risk remains.
  - No independent dataset or orthogonal modality is used to corroborate the PTM enrichment observation; detectability confounders (length, mass, N-terminus coverage) are acknowledged but not modeled.
- Clarity or presentation issues
  - Dense numerical reporting could be complemented by a succinct executive-summary table/figure consolidating the strongest evidence and sensitivity envelopes.
  - The repository’s reproducibility could be strengthened with an archival DOI and containerized environment to minimize rebuild/OS drift.
- Missing related work or comparisons
  - While ProForma is cited, the PSI ProForma 2.0 standard and tooling are not discussed as a practical path to formalize the discrepancy diagnostic and matching.
  - Jaccard significance frameworks that adjust for marginal prevalence (e.g., centered Jaccard/Tanimoto testing) are relevant and could complement row-bootstraps for presence/absence overlap.

## Detailed Comments

- Technical soundness evaluation
  - The overlap and similarity metrics are well chosen and interpreted; reporting multiple normalizations and run-pair views is appropriate for a two-duplicate design.
  - Treating presence/absence using exact accession+proteoform IDs is defensible; the canonicalization diagnostic is a good sanity check, though a standards-based mapping (e.g., ProForma 2.0) would be more rigorous.
  - Chao2/jackknife on two-duplicate incidence is reasonable as a lower-bound sensitivity probe; the authors correctly state identifiability limits for higher-order corrections and present sensitivity envelopes rather than point certainties.
  - The marker alignment analysis is statistically cogent (exact tests, odds ratio intervals, family-size-preserving randomization). The leave-one-out, family exclusion, and intensity-weighted checks all bolster robustness.
  - The PTM analysis is appropriately conservative: a pre-specified acetylation contrast plus one exploratory “other mass shift” bucket with Holm correction; detectability caveats are acknowledged.
- Experimental evaluation assessment
  - The absence of raw reprocessing and biological replicates is candidly stated; within these constraints, the work extracts maximal value from public tables and demonstrates run-pair stability checks and bootstrap sensitivity.
  - Using zero for missing intensities and avoiding imputation is defensible here; still, a brief comparison to a simple MNAR-aware sensitivity (e.g., censoring-threshold perturbations) could further reassure readers.
  - The sentinel purity markers and motor-family exclusions are useful qualitative guardrails; a more quantitative tissue-composition model would be a strong future extension.
- Comparison with related work
  - The discussion of normalization and missingness appropriately references Karpievitch et al., aligning with the decision not to overfit complex models on tiny designs.
  - The paper cites ProForma, but PSI ProForma 2.0 (PSI/HUPO) provides standard, machine-actionable notation and could directly reduce representation mismatches; acknowledging concrete tools/implementations would strengthen the path forward.
  - On binary overlap testing, centered Jaccard/Tanimoto significance (Chung et al.) could complement the descriptive Jaccard and bootstrap sensitivity by accounting for prevalence, which is pertinent given sparse overlaps.
  - The broader context of spatial proteomics and top-down advances (e.g., imaging and microfluidic top-down) is reasonably touched, emphasizing the complementary mission of auditability rather than acquisition innovation.
- Discussion of broader impact and significance
  - The paper’s main impact is cultural and methodological: it shows how to turn a small, qualitative top-down study into an auditable, quantitative analysis that is easy to critique and extend.
  - By demonstrating strong telencephalon/tectum separation and function-aligned marker concentration that withstands sensitivity checks, it motivates further top-down brain-region studies with expanded scope and replication.
  - The reproducibility apparatus (traceability files, source-table parsing, documented rules) is a valuable template; hardening it with standards (ProForma 2.0 IDs) and a citable, containerized release would amplify community value.

## Questions

1. Can you provide a ProForma 2.0–based remapping of the proteoform strings and report overlaps under that standard, to solidify the representation-based reconciliation of the 35 vs 29 vs 44 shared counts?
2. Would you consider adding a centered Jaccard/Tanimoto significance analysis for presence/absence overlap (with appropriate caution for small m), complementing your bootstrap intervals and strengthening the claim of “very low overlap” beyond descriptive indices?
3. For the acetylation enrichment within matched markers, can you report a simple sensitivity analysis controlling for length/mass/N-terminus distance (e.g., stratification or a coarse logistic regression) to further probe detectability confounding?
4. Could you deposit the analysis code and artifacts under an archival DOI and/or provide a container (e.g., Docker) to ensure long-term reproducibility beyond the environment_versions.json?
5. To reduce concerns about marker-selection circularity, can you include a small, independently curated marker set (e.g., literature-derived but not mentioned in the source paper) and report the same alignment and robustness metrics?
6. Is it feasible to add a minimal MNAR-aware sensitivity (e.g., threshold-based censoring perturbation) for intensity similarities to complement the current zero-as-absence approach?

## Overall Assessment

This is a careful, well-scoped, and genuinely useful quantitative re-analysis that turns a modest, pilot-scale top-down dataset into a transparent, statistically legible argument about regional separation and function-aligned markers. The authors are appropriately conservative about scope, deploy multiple overlapping metrics and robustness checks, and provide an audit-ready code/data trail. While the work does not introduce new acquisition or raw-data reprocessing and is limited by the lack of biological replication, it makes a meaningful contribution to reproducibility and interpretability in spatial top-down proteomics. Strengthening the standards-based proteoform matching (ProForma 2.0), adding a prevalence-adjusted overlap significance test, and hardening the reproducibility packaging would further elevate the contribution. Overall, I view this as a solid and valuable paper for the community, particularly as a model of how to responsibly and rigorously re-analyze public top-down datasets.
