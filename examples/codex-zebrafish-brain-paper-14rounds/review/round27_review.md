# round27 Review

Reviewed artifact: `paper/main_round26.pdf`

Backend: `paperreview.ai`

Score: `not returned by paperreview.ai`

Verdict: `Accept`

## Summary

This paper reanalyzes the public top-down proteomics data from a 2022 laser-capture microdissection study of adult zebrafish telencephalon versus optic tectum, focusing on proteoform-level overlap and biologically curated markers. It demonstrates that the two regions occupy sharply distinct proteoform regimes (very low Jaccard/Sørensen and abundance-weighted similarities across multiple normalizations), and that curated marker families align strongly with expected regional biology; a putative N-terminal acetylation asymmetry does not remain robust after detectability-aware sensitivity analyses. The work contributes a transparent, provenance-aware audit that converts narrative claims into quantitative, reproducible statements, while carefully delineating the limits of inference imposed by the released tables.

## Strengths

- Technical novelty and innovation
  - Reframes regional specificity at the proteoform level via exact-ID versus canonicalized matching and prevalence-adjusted overlap (centered Jaccard relative to fixed-margin independence).
  - Introduces family-size-preserving randomization for marker-panel concentration and uses duplicate-informed Chao2/jackknife richness bounds to assess unseen overlap.
  - Provides multiple abundance-similarity metrics (weighted Jaccard, Bray–Curtis) under several normalizations and a minimal MNAR-style sensitivity; includes protein-collapsed analyses.
  - Offers a disciplined negative result on PTMs, showing acetylation asymmetry weakens under detectability-aware modeling.
- Experimental rigor and validation
  - Consistent low similarity across article-level, exact-ID, canonicalized, and protein-collapsed views; multiple normalization schemes and run-pair checks.
  - Extensive sensitivity analyses: bootstrap resampling, Chao2/jackknife envelopes, conservative spillover reassignment, exclusion of motor families, independent composition panel.
  - Prevalence-adjusted overlap testing and exact tests with clear confidence intervals and p-values.
- Clarity of presentation
  - Clear articulation of scope and limitations; transparent provenance and rules for marker curation and matching.
  - Careful accounting for representation mismatches between article aggregates and released tables; interpretable effect-size framing (odds ratios, alignment fractions).
  - Distinguishes pre-specified from exploratory PTM analyses and applies Holm correction appropriately.
- Significance of contributions
  - Strengthens the case that region-specific biology is written at the proteoform level in adult zebrafish, beyond protein-level summaries.
  - Provides a reproducible template for extracting quantitative regional-organization insights from public top-down releases.
  - Highlights the importance and feasibility of proteoform-aware validation in spatially resolved neuroproteomics.

## Weaknesses

- Technical limitations or concerns
  - Reliance on a single pilot dataset with only two technical replicates per region; no biological replication, leaving generalization uncertain.
  - No raw reprocessing or feature-level FDR/localization validation; conclusions necessarily rest on post-processed tables.
  - Hypergeometric fixed-margin null and centered Jaccard do not account for discovery-process dependencies; Chao2/jackknife with only two incidence counts are coarse lower bounds.
  - Abundance analyses treat missing values as zeros with minimal MNAR imputation; while reasonable here, censoring may still bias similarities.
  - Possible batch or acquisition-order confounds are not fully ruled out with only duplicate runs per region.
- Experimental gaps or methodological issues
  - Potential contamination (e.g., motor proteins in optic tectum) is stress-tested but not directly measured; no orthogonal purity assays.
  - Lack of replication on an independent dataset to confirm the sharp separation and marker alignment.
  - The independent composition panel is helpful but small; broader panels could further mitigate circularity concerns.
- Clarity or presentation issues
  - Some implementation details need more precision for full reproducibility (e.g., exact canonicalization rules, residue-window criteria, protein-collapsing logic, intensity preprocessing order).
  - Figures are described rather than shown; exact table references and links to code/data would improve accessibility.
- Missing related work or comparisons
  - Deeper engagement with proteoform notation/registry standards (ProForma 2.0, Proteoform Registry) could strengthen the representation-mismatch discussion.
  - Additional contextualization with region-resolved brain proteomics in zebrafish or other vertebrates would help situate the magnitude of the observed separations.
  - Further discussion of statistical methods for set overlap and detection biases in proteomics (beyond the cited works) could round out methodology context.

## Detailed Comments

- Technical soundness evaluation
  - The overlap and similarity metrics are appropriate, and the prevalence-adjusted framework is a sensible way to contextualize low Jaccard values. The exact-ID versus canonicalized matching analysis cogently diagnoses the article-versus-table discrepancy without altering conclusions.
  - The bootstrap, Chao2/jackknife, and MNAR-style imputations provide reasonable sensitivity bounds given the limited duplication; however, with only two runs per region, richness estimates and missingness models remain coarse, and hypergeometric nulls cannot fully model selection dependencies or candidate-identification pipelines.
  - The PTM section is carefully handled: an initially significant acetylation bias is checked against precursor mass, sequence span, and first-residue position (plus logistic modeling), ultimately reframing the claim as hypothesis-generating. This is a methodological strength and models good scientific hygiene.
- Experimental evaluation assessment
  - The central claim—sharp proteoform-level separation between telencephalon and optic tectum—is strongly supported across multiple views, normalizations, and stress tests. The marker-panel alignment is compelling, especially under family-size-preserving randomization, protein collapse, intensity weighting, and conservative spillover perturbations.
  - The contamination concern is treated fairly via exclusion tests and sentinels, but cannot be decisively resolved without orthogonal purity or histology. Likewise, the lack of biological replication and raw-feature access constrains broader inferential claims.
  - Reporting per-run pairwise similarities is valuable, showing stability of the low-overlap conclusion even before duplicate averaging.
- Comparison with related work (using the summaries provided)
  - The work meaningfully extends beyond the original LCM-CZE-MS/MS pilot by turning dispersed qualitative observations into a cohesive, quantified, and sensitivity-tested statement. It aligns with subsequent reports that proteoform-level signals are biologically informative in zebrafish brains and situates itself alongside emerging spatial-omics foundation models by emphasizing proteoform-resolved auditability rather than scale.
  - The discussion acknowledges standards like ProForma and the Proteoform Registry as longer-term solutions to representation issues; stronger integration (e.g., mapping a subset of entries) would further demonstrate the portability of the approach.
- Discussion of broader impact and significance
  - The study offers a useful blueprint for extracting robust, biologically interpretable conclusions from public top-down proteoform tables—emphasizing exact matching, prevalence-adjusted overlap, traceable curation, and clearly bounded claims.
  - Its transparent, sensitivity-driven approach should encourage higher-quality public releases (feature histories, localization confidence) and careful proteoform-aware analyses in neuroproteomics. Risks center on overgeneralization from a single dataset and on relying too heavily on curated markers without broader, orthogonal validation—caveats the paper explicitly and responsibly states.

## Questions

1. Can you provide a public repository link containing the code, traceability JSON/CSV, and exact parameter settings to enable full reproduction of all statistics and figures?
2. Please specify the canonicalization pipeline precisely (e.g., which bracket types, punctuation, residue-window definitions, and edge cases), and share one or two concrete examples where canonicalization merges entries.
3. How were proteins defined for protein-collapsed analyses (e.g., strict accession equality, gene symbol mapping, isoform handling)? Did multi-mapping proteoforms contribute to multiple proteins or one?
4. Do acquisition order, instrument conditions, or batch metadata for the four runs suggest any confounding that could inflate regional separation? If available, please summarize.
5. For the prevalence-adjusted test, what exact margins and universe size were used, and how sensitive are p-values to expanding the universe to include all accessions observed in either region plus plausible “non-detected” candidates?
6. Can you provide a few exemplar spectra and TopPIC identifications (with localization confidence) for high-impact marker proteoforms from each region to further reassure readers about ID quality in the absence of raw-feature reprocessing?
7. Would mapping a subset of proteoforms to ProForma 2.0 or the Proteoform Registry be feasible, to help future-proof the representation-mismatch diagnostic?
8. Could you report alignment and overlap statistics using an expanded, literature-derived panel beyond the current myelin/radial-glia markers (e.g., additional neuronal/glial markers in adult zebrafish) to test robustness to panel composition?
9. How sensitive are the intensity-based similarities to log transforms or small pseudo-counts on shared IDs only (to reduce dominance by high-intensity calls while not over-weighting zeros)?
10. Are there indications in the released tables of proteoforms likely to derive from non-neural tissue (e.g., muscle), and could you provide a more formal assessment (e.g., tissue-enrichment scoring) alongside the current sentinel and exclusion checks?

## Overall Assessment

This is a careful, well-argued, and transparent reanalysis that strengthens and clarifies the biological interpretation of a public top-down zebrafish brain dataset. The central result—that telencephalon and optic tectum occupy sharply distinct proteoform regimes, with curated markers overwhelmingly aligning to expected regional biology—is convincingly supported by multiple overlap/similarity metrics, prevalence-adjusted tests, and a diverse set of robustness checks. The disciplined treatment of PTMs, which rescinds an initially appealing acetylation story after detectability-aware modeling, further reinforces the authors’ methodological rigor. The main limitations are inherent to the public data: only two technical replicates per region, no biological replication, and lack of raw-feature histories precluding deeper FDR/localization audits or contamination resolution. Within these bounds, the work provides a valuable, reusable template for proteoform-aware auditing and carries clear relevance for the proteomics and neurobiology communities. I recommend acceptance, contingent on releasing full code/trace artifacts and tightening a few methodological details to maximize reproducibility and portability.
