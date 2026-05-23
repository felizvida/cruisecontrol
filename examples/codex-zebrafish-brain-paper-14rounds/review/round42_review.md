# Round 42 Review

Reviewed artifact: `paper/main_round41.pdf`

Backend: `paperreview.ai`

Score: `not returned by paperreview.ai`

Verdict: `Accept`

## Summary

This paper reanalyzes a published adult zebrafish brain top-down proteomics dataset (LCM–CZE–MS/MS) to test whether telencephalon and optic tectum are distinguished at the intact-proteoform level. Using strict accession-plus-proteoform identities, multiple overlap metrics, detectability and representation sensitivity checks, and curated biological marker panels, the authors report a very small shared proteoform repertoire and a strong, directionally consistent enrichment of telencephalon-associated neuropeptide/synaptic entries versus optic-tectum-associated reticulon/cytoskeletal/motor entries. The analysis further shows that coarser identifier collapse (protein/gene) increases apparent overlap but does not erase regional separation, and that an initially observed N-terminal acetylation bias weakens under covariate checks.

## Strengths

- Technical novelty and innovation
  - The work provides a careful, identifier-aware reanalysis that foregrounds proteoform resolution (accession-plus-proteoform) and quantifies how conclusions change with canonicalization and identifier collapse.
  - Application of ecological richness/occupancy adjustments and representation diagnostics to top-down proteoform overlap is creative and helps bracket detectability-driven uncertainties.

- Experimental rigor and validation
  - Multiple, complementary overlap metrics (Jaccard, Bray–Curtis; count- and intensity-weighted) and fixed-margin hypergeometric baselines with centered Jaccard strengthen the separation claim.
  - Robustness checks include duplicate-informed detectability corrections, rarefaction to equalize list sizes, canonicalization sensitivity, protein/gene collapse, and conservative misidentification bounds tied to reported FDRs.
  - Marker-direction claims are validated by both an a priori curated panel aligned with the source paper’s biology and an independent literature-derived panel, with family-size-preserving randomization tests.

- Clarity of presentation
  - Clear articulation of analysis units (accession-plus-proteoform vs protein vs gene symbol) and why identifier granularity matters.
  - Transparent scoping: strong claims are limited to overlap/marker direction; PTM inference is appropriately cautious.

- Significance of contributions
  - Demonstrates that intact-proteoform granularity preserves biologically meaningful regional structure that protein-level summaries dilute, advancing the case for proteoform-aware spatial proteomics.
  - Offers a reproducible framework (as described) for rigorous reanalysis of public top-down datasets, relevant to communities working at the interface of spatial omics and proteoform biology.

## Weaknesses

- Technical limitations or concerns
  - Reliance on processed PRIDE spreadsheets and published FDRs without access to raw feature histories limits the ability to model localization certainty, feature-to-proteoform propagation, and region-structured error.
  - The dataset appears to comprise duplicate technical runs per region without clear biological replication across animals, constraining generalization beyond this preparation.

- Experimental gaps or methodological issues
  - Potential tissue purity/contamination confounds remain under-characterized; extensive myosin/troponin content in the optic-tectum set raises the possibility of muscle carryover. While stress tests exclude motor families, direct sentinel panels for muscle and non-neural tissues and quantitative purity estimates would strengthen the anatomical interpretation.
  - The independence baseline and hypergeometric testing assume exchangeability under fixed margins; detectability heterogeneity beyond duplicate occupancy (e.g., proteoform-dependent ionization or fragmentation differences) may still bias overlap expectations.

- Clarity or presentation issues
  - Several exponent notations for p-values appear corrupted (e.g., 10−14³, 10−18³), which should be corrected to avoid ambiguity.
  - Details of the canonicalization rules, marker mapping heuristics, and exact accessions composing each family are said to be in a local file; explicit, in-text methodological detail or supplemental tables would help readers audit decisions without running the code.

- Missing related work or comparisons
  - The paper could better situate its approach alongside spatial proteomics/IMS integration and multimodal spatial omics reviews, and more deeply discuss known practical constraints of top-down spatial workflows and data integration (e.g., as surveyed in multimodal spatial omics frameworks).
  - There is limited discussion of proteoform family modeling and cross-accession ambiguity resolution strategies beyond ProForma references; additional connections to proteoform family inference literature would help.

## Detailed Comments

- Technical soundness evaluation
  - Overlap analysis at strict accession-plus-proteoform level is an appropriate and conservative choice; showing that the inference persists through canonicalization and identifier collapse is compelling.
  - The use of fixed-margin hypergeometric baselines and centered Jaccard is principled for contingency-style overlap assessment; the authors also account for detectability via duplicate occupancy and rarefaction, which addresses key concerns about uneven recovery.
  - Application of Chao2/jackknife richness and occupancy adjustments from ecology is reasonable in spirit; still, it would be helpful to articulate assumptions (closed population, detection independence) and any violations specific to top-down MS (feature coalescence, PTM localization uncertainty).
  - The PTM analysis is appropriately de-emphasized; logistic models with mass/span/first-residue covariates are a sensible first pass given small N. Reporting wide CIs and loss of significance is appropriately cautious.

- Experimental evaluation assessment
  - The breadth of sensitivity analyses (abundance weighting, stratified occupancy, rarefaction, mis-ID ceilings, canonicalization variants) adds robustness to the central claim of low overlap.
  - Biological validation via curated marker families and a separate literature panel, plus family-size-preserving randomization, addresses concerns about circularity in marker selection and dependence structure across proteoforms within families.
  - The strongest remaining empirical gap is quantitative tissue purity assessment and external validation across biological replicates/animals. Adding explicit muscle and non-neural sentinel panels and reporting their intensities would materially strengthen the anatomical interpretation.

- Comparison with related work (using the summaries provided)
  - Relative to the multimodal spatial omics landscape, the study exemplifies a serial-section, microdissection-based depth-over-pixels trade-off, consistent with reviews that emphasize limited proteome depth and spatial anchoring challenges for top-down IMS. The paper’s emphasis on identifier granularity aligns with the recognized difficulty of linking top-down proteoforms to gene/transcript anchors in spatial integration tasks.
  - The work’s message—that proteoform resolution reveals regional biology that protein-level aggregation blurs—adds a useful empirical case study complementing reviews highlighting the promise and practical limits of proteoform-aware spatial methods.
  - The analysis would benefit from explicit linkage to computational integration strategies (e.g., factor models, OT/FGW alignment) that might reconcile proteoform-level findings with imaging or transcriptomic atlases in future work.

- Discussion of broader impact and significance
  - The study strengthens the argument for proteoform-aware identifiers in spatial proteomics workflows and benchmark analyses. It also offers a compact template for reusing public top-down datasets to probe biologically anchored questions, potentially motivating standardized releases that include feature histories and ProForma-ready annotations.
  - Highlighting how conclusions shift with identifier relaxation provides a practical lesson for the community and will inform downstream integration and interpretation in multimodal spatial pipelines.

## Questions

1. Can you provide a quantitative purity assessment using targeted sentinel panels for skeletal/cardiac muscle (e.g., MYH isoforms, desmin, titin) and other non-neural tissues, alongside neuronal/glial/myelin markers, to bound possible tissue carryover—especially for the optic-tectum samples?
2. How exactly was canonicalization performed (regex patterns, handling of ambiguous/localized PTMs, charge states, truncations), and can you share a definitive mapping table of raw strings to canonical IDs to enable independent replication?
3. Were any cross-accession ambiguities observed for the same proteoform-like string, and how were conflicts adjudicated (e.g., by proteoform family grouping or best-scoring accession)? Would family-level grouping alter the overlap picture?
4. The duplicate occupancy model treats per-run detection as region-specific but proteoform-invariant within strata. Did you explore more granular detectability models (e.g., per-proteoform hierarchical detection probabilities) or sensitivity to the assumption of independence across runs?
5. Do your conclusions hold when restricting to the top-N most intense proteoforms per region (e.g., top 100 by mean duplicate intensity), to reduce susceptibility to low-level identifications and missingness?
6. How many unique animals and tissue blocks underlie the Tel2/Teo2 spreadsheets, and can you clarify the biological versus technical replicate structure? Would you consider validating the marker-axis result in a second, independent dissection/animal?
7. Could you provide the full marker membership tables (accession plus proteoform), including the independent literature-derived panel, as a supplement? This would facilitate auditing potential mapping errors or synonym conflation.
8. Some reported p-values have formatting artifacts (e.g., 10−14³). Can you revise to unambiguous scientific notation and, where applicable, provide exact hypergeometric tail probabilities?

## Overall Assessment

This is a careful, well-scoped reanalysis of a valuable top-down proteomics dataset that convincingly demonstrates strong proteoform-level separation between adult zebrafish telencephalon and optic tectum and shows that this separation aligns with known regional biology. The methodological choices—strict accession-plus-proteoform identifiers, multiple complementary overlap measures, occupancy/rarefaction sensitivity, and curated marker validation—are appropriate and thoughtfully executed. The authors responsibly temper PTM-level claims and make clear the limits of inference imposed by working from processed tables without raw feature histories or robust biological replication. The main reservations concern potential tissue purity confounds (notably motor protein abundance in optic tectum), lack of quantitative contamination sentinels, and generalization beyond the specific preparation. Despite these, the central claims are well supported, the insights about identifier granularity are timely and instructive, and the work is likely to be valuable to the spatial proteomics and proteoform communities. I recommend acceptance after minor revisions that address purity assessment, canonicalization transparency, and notation fixes; if new validation is infeasible within the current cycle, a clear statement of these limitations and expanded sentinel analyses would suffice.
