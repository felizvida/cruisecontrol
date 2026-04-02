# round35 Review

Reviewed artifact: `paper/main_round34.pdf`

Backend: `paperreview.ai`

Score: `not returned by paperreview.ai`

Verdict: `No calibrated score returned`

## Summary

This paper presents a careful secondary analysis of a public, region-resolved top-down proteomics dataset of adult zebrafish telencephalon and optic tectum (Lubeckyj and Sun, 2022). By examining exact accession+proteoform identities in the deposited PRIDE spreadsheets and performing multiple sensitivity analyses, the authors show that the two regions share very few proteoforms and that the separating proteoforms align with known regional biology (forebrain neuropeptide/synaptic markers vs visuomotor/cytoskeletal markers). They further evaluate a putative N-terminal acetylation asymmetry and conclude that this PTM signal is not stable after accounting for detectability and other confounders.

## Strengths

- Technical novelty and innovation
  - The paper leverages the deposited proteoform-level spreadsheets to quantify overlap structure in a way that the original narrative did not, adopting a stringent exact accession+proteoform unit and probing how canonicalization choices affect overlap.
  - Multiple conservative sensitivity analyses (detectability via duplicates, misidentification ceilings keyed to reported FDRs, Chao2/jackknife richness bounds, family-size-preserving randomization) are thoughtfully designed to match what the deposited data can actually support.
  - The work foregrounds the value of proteoform-aware standards (ProForma) and careful identifier handling for biological inference.
- Experimental rigor and validation
  - Overlap conclusions are tested under strict/relaxed matching, abundance weighting, prevalence-adjusted baselines, and conservative error bounds; results are concordant across metrics.
  - Marker-based biological validation is strong, with near-complete alignment of curated families to the expected region and robustness to leave-one-out removal and exclusion of large motor families.
  - The acetylation claim is treated cautiously and stress-tested, avoiding overinterpretation.
- Clarity of presentation
  - The argument is logically structured (data scope → overlap quantification → biological direction → PTM caution), with transparent discussion of interpretive limits.
  - The methods and assumptions are explicitly tied to what the spreadsheets expose; formulae and sensitivity setups are documented in an appendix.
- Significance of contributions
  - The study demonstrates that proteoform-level resolution reveals a sharp, biologically coherent regional organization that protein-collapsed views dilute, which is important for the proteoform community and for region-resolved neuroproteomics.
  - It provides a reproducible template for reanalyzing public top-down datasets to extract rigorous, proteoform-centric biological insight.

## Weaknesses

- Technical limitations or concerns
  - The detectability correction assumes a homogeneous per-run detection probability derived from duplicate rediscovery, which may not capture proteoform-specific detectability differences (mass/charge/PTM/sequence-dependent effects).
  - The misidentification “ceiling” analysis is symmetric and coarse; it does not model proteoform-level localization ambiguity or accession-sharing explicitly.
  - Protein-family correlations (e.g., many actin/myosin/troponin forms) can inflate non-independence; while motor families are excluded in a sensitivity check, broader correlation structure remains.
- Experimental gaps or methodological issues
  - No raw-feature reprocessing is attempted; thus, feature histories, localization confidence distributions, and cross-run alignment uncertainties cannot be evaluated, limiting conclusions about PTM localization and fine-grained quantitative differences.
  - Presence/absence metrics dominate, with only limited intensity-aware comparisons; the study does not attempt formal differential abundance at the proteoform level (likely underpowered with duplicates), which could complement overlap measures.
  - Regional purity (LCM cross-contamination) is only indirectly assessed via sentinel markers; more formal purity or cell-type composition controls are not possible from the deposit but would strengthen anatomical inference.
- Clarity or presentation issues
  - Some figures are placeholders from PDF extraction; the main text is clear, but direct access to the code/data artifacts referenced (CSV/JSON) is essential to fully verify the workflow.
  - The acetylation detectability adjustment is described at a high level; additional detail on the covariates/model form used for adjustment would aid interpretability.
- Missing related work or comparisons
  - While ProForma 2.0 is cited, the broader landscape of spatial top-down proteomics (e.g., on-tissue top-down MSI) and its implications for regional proteoform mapping could be discussed more explicitly.
  - Methodological connections to quantitative frameworks that model shared/unique molecular forms (e.g., HIquant’s treatment of shared peptides/proteoforms in bottom-up) could contextualize the chosen presence/absence emphasis.

## Detailed Comments

- Technical soundness evaluation
  - The core overlap claim is technically sound and appropriately conservative: strict exact-ID matching, prevalence-adjusted tests, and multiple sensitivity analyses converge on a very low Jaccard overlap that cannot be explained away by reasonable detectability or FDR assumptions.
  - The detectability model derived from duplicate rediscovery is a sensible first-order correction given data constraints, but it is necessarily simplistic; proteoform-specific detectability heterogeneity (ionization, fragmentation, PTM status, sequence length) likely remains.
  - The misidentification ceiling anchored to reported FDRs is appropriately framed as a bound; the paper rightly avoids inferring a true error distribution from limited metadata.
  - The acetylation analysis is careful: after accounting for detectability proxies and sequence geometry, the enrichment weakens; this restraint lends credibility to the overall study.
- Experimental evaluation assessment
  - Although no new experiments are performed, the analysis is well-anchored in the public deposit, uses duplicate labels constructively (richness, detectability), and acknowledges the impossibility of feature-level error modeling without raw search intermediates.
  - Robustness checks are comprehensive within scope: strict/relaxed matching, intensity weighting, protein collapse, leave-one-out for markers, family exclusion, and conservative spillover reassignment all preserve the primary conclusion.
  - Additional quantitative comparisons (e.g., Bray-Curtis, which is mentioned but not extensively discussed) could be expanded to complement Jaccard with continuous measures, but the present evidence suffices for the central claim.
- Comparison with related work (using the summaries provided)
  - The discussion around ProForma 2.0 (PSI/HUPO standard) is apt and could be deepened by articulating how partial localization metadata in public deposits limits fully standard-compliant serialization and, consequently, cross-study exact-ID matching (2109.11352).
  - The study’s emphasis on spatial organization at the proteoform level resonates with progress in on-tissue top-down MSI (Kiss et al., 2014; 1309.0988), which trades depth for direct spatial fidelity; contrasting LCM-CZE-MS/MS with MSI would situate the current findings within spatial proteoform mapping modalities.
  - Broader proteomics perspectives (2108.07660) underline the importance of multi-dimensional proteoform characterization; this work contributes a concrete example where proteoform resolution preserves biologically meaningful regional texture that protein-level views dilute.
  - While not directly applicable, methods like HIquant (1708.01772) highlight how modeling shared molecular species can recover quantitative structure; acknowledging why such approaches are impractical here (top-down, duplicates only) helps justify the presence/absence focus.
- Discussion of broader impact and significance
  - The paper demonstrates that proteoform-level analysis can reveal strong, biologically interpretable regional organization even in small, pilot-scale datasets, arguing for routine release and analysis of proteoform-resolved identifications.
  - It provides a practical template for community re-use of public top-down deposits, including identifier handling, sensitivity analysis aligned with metadata, and restrained claims where detectability confounds remain.
  - Findings encourage adoption of standardized proteoform representations and richer deposits (feature histories, localization confidence), which would materially improve reproducibility and cross-study synthesis.

## Questions

1. Can you provide a public repository link (with a stable tag/DOI) to the CSV/JSON artifacts and scripts referenced in the appendix, so readers can reproduce the overlap and marker analyses exactly?
2. How precisely is the detectability-adjusted acetylation analysis implemented (model form, covariates, fitting procedure)? For example, is it a logistic regression with precursor mass, sequence span, N-terminal position, and region recovery fractions as predictors?
3. In the detectability correction for overlap, do you assume a single homogeneous detection probability per region across all proteoforms? If so, can you explore stratified detection probabilities (e.g., by mass bin or PTM presence) to assess robustness?
4. Regarding non-independence within marker families, beyond excluding motor families, did you consider down-weighting multiple proteoforms from the same protein/gene or clustering correlated entries to reduce effective multiplicity?
5. How were accession conflicts handled when the same proteoform string appeared under multiple accessions? Would a gene-centric or isoform-centric collapse change any of the conclusions materially?
6. Can you comment on potential batch or run-order effects in the duplicates (e.g., telencephalon vs tectum processing order), and whether any normalization beyond intensity scaling was required?
7. For the “prevalence-adjusted” overlap tests, could you report the exact p-values and effect sizes (e.g., centered Jaccard) alongside the baselines for stricter/relaxed matching cases?
8. Do you have access to metadata indicating whether duplicates correspond to distinct animals or technical repeats from the same tissue capture? If biological replication is limited, how might that affect generalization?
9. Would integrating additional orthogonal markers (e.g., scRNA-seq-defined region-specific gene sets from Pandey et al., 2023) change the strength or direction of the axis-alignment result?
10. Could you release a compact mapping file that links each curated marker-family member to its exact spreadsheet row(s) and matching rule hits, to facilitate external audit?

## Overall Assessment

This is a careful and well-argued secondary analysis that extracts clear, biologically meaningful conclusions from a publicly deposited top-down proteomics dataset. The central claim—that adult zebrafish telencephalon and optic tectum are sharply separated at the proteoform level and that distinguishing proteoforms align with known regional biology—is strongly supported through stringent overlap definitions, multiple conservative sensitivity analyses, and a robust marker-based validation that resists several perturbations. The authors are appropriately cautious about the PTM layer, showing that apparent acetylation asymmetry is not stable once detectability is considered. While the work is necessarily constrained by its reliance on spreadsheets (no raw-feature reprocessing), homogeneous detectability assumptions, and limited replication, it still provides a valuable, reproducible template for proteoform-centric reanalysis and underscores the importance of standardized identifiers and richer public deposits. I view this as a solid contribution of moderate originality but high clarity and methodological care, suitable for publication after minor revisions focused on code/data availability, expanded methodological detail on detectability/PTM modeling, and a slightly broader contextualization within spatial top-down proteomics.
