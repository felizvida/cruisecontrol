# round19 Review

Reviewed artifact: `examples/codex-zebrafish-brain-paper-14rounds/paper/main_round19.pdf`

Backend: `paperreview.ai`

Score: `not returned by paperreview.ai`

Verdict: `Accept`

## Summary

This paper presents a quantitative, reproducible re-analysis of a 2022 top-down proteomics pilot profiling adult zebrafish telencephalon and optic tectum. Using counts extracted from the source article and the released per-region proteoform tables, the authors quantify regional separation with multiple overlap/similarity metrics, conduct duplicate-informed missingness sensitivity analyses (Chao2 and jackknife), and formalize the biological interpretation as a matched-versus-spillover alignment of curated marker families. They further examine post-translational modification patterns, finding a strong enrichment of N-terminal acetylation among telencephalon-matched marker proteoforms, and provide a code/data package for traceable reproduction.

## Strengths

- Technical novelty and innovation
  - Reframing a qualitative biological narrative into an explicit, auditable quantitative alignment problem is a useful and nontrivial contribution for small spatial proteomics studies.
  - The discrepancy diagnostic between article-level “shared proteoforms” and exact table-derived overlaps (strict vs canonicalized matching) highlights an important provenance and representation issue common in proteomics publishing.
  - Incorporation of duplicate-informed missingness bounds (Chao2, jackknife) and multiple intensity-normalization regimes provides a methodologically aware sensitivity envelope well-suited to the limited public data.
- Experimental rigor and validation
  - Systematic overlap metrics (Jaccard, Sørensen, Bray–Curtis, weighted Jaccard) under multiple normalizations, plus run-pair analyses, robustly support the low-overlap claim.
  - Marker alignment is backed by exact tests, family-size-preserving randomization, leave-one-out analysis, intensity weighting, and protein-collapse robustness.
  - PTM results are constrained to a pre-specified N-terminal acetylation screen with Holm-adjusted p-values, avoiding broad post hoc fishing.
- Clarity of presentation
  - The paper is carefully written, with explicit metrics, formulas, and numerical values that make the audit trail clear.
  - Clear scoping of claims and limitations; the distinction between article-level extraction and table-driven analysis is carefully maintained.
- Significance of contributions
  - Demonstrates how to turn a small, published top-down dataset into a transparent, reusable analysis with strengthened biological interpretation.
  - Provides a template others can follow to improve reproducibility and interpretability in spatial top-down proteomics.

## Weaknesses

- Technical limitations or concerns
  - The work does not include raw-feature reprocessing or proteome-wide FDR recalibration; conclusions rely on PRIDE tables and reported thresholds, which precludes finer-grained controls on identification quality, localization, and detectability biases.
  - Canonicalization used for the discrepancy diagnostic is ad hoc (stripping bracketed PTMs/punctuation) rather than grounded in a standard such as ProForma 2.0; this could affect reproducibility of overlap computations elsewhere.
  - Statistical tests on proteoform counts implicitly treat entries as independent; dependencies within families or proteins may inflate nominal significance.
- Experimental gaps or methodological issues
  - Limited replication (two duplicate runs/region) constrains the ability to model missingness mechanisms or apply more sophisticated normalization/imputation frameworks.
  - Purity/contamination checks are limited to a small sentinel panel; a richer, orthogonal marker set or orthogonal modalities would better address contamination concerns.
  - The PTM enrichment analysis cannot fully discount detection/localization biases (e.g., N-terminus coverage, spectrum quality differences) without raw-level evidence.
- Clarity or presentation issues
  - A few minor typographical artifacts persist (e.g., “inter-pretation,” “Te12”), and exact formulas for some similarity measures (e.g., weighted Jaccard) could be stated more explicitly in the main text.
  - The code/reproducibility section references a local path but does not specify a permanent archival DOI.
- Missing related work or comparisons
  - Limited engagement with proteoform notation/standardization literature (e.g., ProForma 2.0) and with recent FDR calibration approaches relevant to proteomics scoring (e.g., model-based decoy-free calibration paradigms).
  - The discussion could more clearly situate this re-analysis alongside complementary bottom-up approaches for proteoform inference (e.g., HIquant) and their trade-offs, and reflect on how such methods might cross-check top-down conclusions.

## Detailed Comments

- Technical soundness evaluation
  - The overlap and similarity analyses across strict ID, canonicalized sequence, abundance-weighted, and protein-collapsed views are well-motivated and mutually consistent; all place the system in a low-overlap regime.
  - Duplicate-informed Chao2 and jackknife lower-bound estimates are appropriately used to stress-test overlap under plausible unseen richness; the sensitivity envelope (fixed-shared vs scaled-shared scenarios) is transparent and conservative.
  - The marker alignment framing is statistically clear, with exact tests, effect sizes (odds ratios with intervals), and a null preserving family sizes and total label counts; this addresses common circularity critiques in curated marker evaluations.
  - The PTM screen is pre-specified (N-terminal acetylation) and accompanied by a minimal exploratory screen with multiple-testing control; this balance of focus and restraint is appropriate.
- Experimental evaluation assessment
  - Despite limited replication, the authors report multiple normalization schemes and run-pair similarities, which is an appropriate level of care for the data available.
  - Treating blank intensity cells as zeros (no imputation) is a defensible conservative choice; still, the authors rightly acknowledge that richer missingness modeling requires more replication.
  - The small sentinel-marker purity check is informative but limited; nonetheless, stress tests excluding motor-associated families and shifting matched-to-spillover counts demonstrate the robustness of the core alignment result.
- Comparison with related work (using the summaries provided)
  - The emphasis on proteoform-level accounting and PTM structure complements bottom-up deconvolution approaches like HIquant, which infer proteoform stoichiometries from peptides; the authors could highlight how these perspectives might cross-validate each other on future datasets.
  - Canonicalization choices would benefit from alignment with ProForma 2.0, which provides a community standard to encode peptidoforms/proteoforms and mitigate representation mismatches when computing overlaps or registering proteoforms.
  - Recent calibration paradigms for FDR estimation (e.g., Winnow’s discriminative, decoy-free approach for DNS) underscore the importance of well-calibrated confidence in identification workflows; while not directly applied here, acknowledging analogous top-down calibration opportunities would add context.
  - PTM prediction frameworks (e.g., UniPTMs, Deep-Ace) are orthogonal; this paper focuses on observed PTMs rather than prediction. Still, linking observed PTM distributions to model-predicted propensities in future work could enrich mechanistic interpretation.
  - Broader spatial-omics integration work (multimodal reviews) frames where such proteoform-specific, auditable notes can interoperate with large-scale spatial models; the authors appropriately position their contribution as complementary.
- Discussion of broader impact and significance
  - The paper provides a replicable scaffold for turning narrative interpretations from small spatial proteomics studies into explicit, testable, and auditable claims—valuable for the community’s reproducibility culture.
  - The findings reinforce that proteoform-level resolution can reveal stronger regional separation than protein-level aggregates and can expose meaningful PTM structure within functionally interpretable markers.
  - Limitations are carefully scoped. The work is best viewed as a methodological and reproducibility note rather than a discovery paper, but it nonetheless sets strong expectations for data release, traceability, and statistical clarity.

## Questions

1. Can you provide an archival DOI (e.g., Zenodo) for the analysis code, traceability files, and generated outputs referenced in the reproducibility appendix?
2. Please specify the exact formula you used for the weighted Jaccard similarity on intensities (e.g., whether weights are averaged across duplicates first, how zeros are handled, and whether any log transform was considered).
3. How sensitive are the canonicalized-overlap results to the specific stripping rules? Have you considered implementing ProForma 2.0 parsing/canonicalization or mapping to Proteoform Registry identifiers to standardize overlap computations?
4. For the N-terminal acetylation enrichment, did you examine basic detectability proxies (e.g., precursor charge distributions, fragmentation quality surrogates, sequence length) to check for systematic differences between regions that could bias acetylation detection?
5. In the family-size-preserving randomization, did you also explore permutations that preserve protein identity (i.e., collapsing to unique proteins before shuffling) to mitigate within-protein dependence among multiple proteoforms?
6. Could you report confidence intervals for the Bray–Curtis and weighted Jaccard similarities (e.g., via bootstrap over rows) alongside point estimates, for symmetry with the overlap-interval reporting?
7. Do the released TopPIC/TopDiff outputs (or the supplement) allow recovering per-PSM/PrSM quality metrics for at least a subset of identifications to partially validate localization confidence and support a finer PTM analysis?

## Overall Assessment

This is a careful, well-scoped re-analysis that strengthens the interpretability and auditability of a small but influential top-down spatial proteomics pilot. The core claims—very low proteoform overlap between telencephalon and optic tectum, strong alignment of curated markers to expected regions, and a focused N-terminal acetylation enrichment in telencephalon-matched markers—are consistently supported across multiple views, stress tests, and sensitivity analyses. The limitations are candidly discussed and largely derive from the constraints of the public data (lack of raw-feature-level exports and richer replication), not from analytical shortcuts. While the contribution is not a novel algorithm or a new dataset, it raises the standard for transparent, quantitative interpretation of small spatial proteomics studies and offers a useful template others can follow. For a venue that values reproducibility notes, rigorous re-analyses, and methodological clarity in proteomics and spatial omics, I view this as a solid contribution. I recommend acceptance in an “Analysis/Resource/Note” track, contingent on minor revisions to standardize canonicalization (ideally with ProForma 2.0), clarify similarity formulas, and archive the code/data package.
