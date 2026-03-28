# round30 Review

Reviewed artifact: `paper/main_round29.pdf`

Backend: `paperreview.ai`

Score: `not returned by paperreview.ai`

Verdict: `No calibrated score returned`

## Summary

This paper reanalyzes publicly released region-specific top-down proteomics tables from Lubeckyj and Sun (2022) to quantify proteoform-level differences between adult zebrafish telencephalon and optic tectum. It shows that the two regions have sharply distinct proteoform profiles with very low overlap and that the proteoforms driving the separation align with known regional biology; in contrast, an apparent N-terminal acetylation asymmetry does not remain robust after detectability-aware adjustments. The work emphasizes transparent, provenance-tracked analyses with multiple robustness checks, turning a previously qualitative interpretation into an explicit, quantitative statement about regional proteoform organization.

## Strengths

- Technical novelty and innovation
  - Recasts regional differences as an explicit overlap/alignment problem at the proteoform level with exact-ID matching, protein-collapsed summaries, and prevalence-adjusted testing.
  - Introduces a clear matched-versus-spillover framing for marker families and supports it with family-size-preserving randomization and sensitivity analyses.
  - Provides a detectability-aware perspective on PTM asymmetry, avoiding overinterpretation of preliminary PTM signals.
- Experimental rigor and validation
  - Multiple complementary overlap metrics (Jaccard, Sørensen, Bray-Curtis; abundance-weighted and prevalence-adjusted) consistently show strong separation.
  - Robustness checks include alternative normalizations, duplicate-informed richness bounds (Chao2, jackknife), MNAR-style fills, protein collapse, spillover reassignment, leave-one-out marker analyses, and an independently curated composition panel.
  - Exact and interval-based inference for contingency analyses (odds ratios, Wilson intervals, one-sided exact tests) with extensive randomization to validate alignment.
- Clarity of presentation
  - The argument is tightly scoped to what the public release can support, with clear articulation of limits.
  - Strong emphasis on traceability: explicit rules for canonicalization and marker matching, and a claim-to-evidence/file map.
  - The narrative is concise and the key effect sizes are easy to follow; sensitivity analyses are summarized accessibly.
- Significance of contributions
  - Converts a dispersed, qualitative biological interpretation into a crisp, quantitative conclusion about regional proteoform regimes in the adult zebrafish brain.
  - Highlights the added value of proteoform-resolved analysis beyond protein-level summaries for region-resolved neurobiology.
  - Provides a template for rigorous reanalysis of public top-down datasets with interpretable outputs and testable claims.

## Weaknesses

- Technical limitations or concerns
  - Reliance on processed TopPIC/TopDiff-derived region tables rather than raw-feature reprocessing limits control over identification, localization confidence, and detectability biases.
  - Differences in sampling depth and detection sensitivity between regions could inflate uniqueness and reduce overlap; while addressed partially, a fuller occupancy or hierarchical detectability model is not implemented.
  - No explicit misidentification correction is applied (e.g., adjusted Chao2/jackknife under misclassification), leaving a residual concern that part of the low overlap could stem from ID variance.
- Experimental gaps or methodological issues
  - Absence of orthogonal validation (e.g., targeted MS, immunodetection, or bottom-up cross-checks) for key region-distinguishing proteoforms.
  - Lack of raw data rescoring or PTM localization quality thresholds impedes a deeper PTM-specific interpretation (beyond the cautious acetylation note).
  - Statistical calibration of extremely small p-values under fixed-margin tests is not linked to biological effect sizes beyond Jaccard differences; model-based uncertainty quantification (e.g., occupancy or Bayesian models) could better apportion technical versus biological variance.
- Clarity or presentation issues
  - Some figure references are presented as schematic placeholders; tighter integration of final plots and a minimal in-text figure caption recap of sample sizes and units would help.
  - The canonicalization step could benefit from aligning with ProForma 2.0 conventions to resolve representation discrepancies in a community-standard way.
- Missing related work or comparisons
  - Limited discussion of standardization efforts (e.g., ProForma 2.0) that directly pertain to proteoform identity representation and could reduce strict/relaxed matching discrepancies.
  - The work could better position its detectability-aware analysis relative to occupancy/missingness frameworks from proteomics and bias-correction ideas (e.g., misidentification adjustments in incidence data).
  - Brief comparison to bottom-up proteoform inference (e.g., HIquant) could contextualize when intact-proteoform separation offers unique advantages over peptide-based approaches.

## Detailed Comments

- Technical soundness evaluation
  - The overlap and alignment analyses are thoughtfully constructed: exact-ID matching on accession+proteoform is conservative and appropriate; abundance-weighted similarities (weighted Jaccard, Bray-Curtis) guard against binary incidence-only conclusions; prevalence-adjusted tests (fixed-margin hypergeometric) correctly contextualize overlap given margins.
  - The marker alignment strategy is statistically well-supported (odds ratios with CIs, exact tests, randomization preserving family sizes), and stress tests (leave-one-out, protein collapse, spillover handling, intensity weighting) bolster robustness.
  - The PTM analysis is cautious and appropriately detectability-aware; the authors avoid overclaiming in the face of plausible biases in precursor mass, span, and N-terminus position.
  - Remaining technical caveats largely stem from the data’s scope: without raw-feature reprocessing, detailed localization confidence and false localization rates cannot be probed; occupancy models or explicit misidentification corrections are not applied and could further refine conclusions.
- Experimental evaluation assessment
  - For a reanalysis paper, the suite of sensitivity checks is strong and credible. The duplicate-informed richness estimates and MNAR-style fills are sensible probes for undersampling effects.
  - Still, region-specific depth differences (total identifications, recovery fractions) can induce asymmetric detectability; modeling detections via a hierarchical occupancy or zero-inflated framework could quantify how much of the observed uniqueness is explained by depth alone.
  - Orthogonal validation for a small subset of discriminating proteoforms (even from independent literature or bottom-up overlays) would further anchor the biological claims.
- Comparison with related work (using the summaries provided)
  - Standardization: ProForma 2.0 (PSI/CTDP) is directly relevant to resolving representation discrepancies; adopting or mapping to ProForma would strengthen the canonicalization diagnostics and portability of IDs across tools and studies.
  - Methodological context: bottom-up inference methods like HIquant address proteoform ratios under peptide-level biases; this work complements them by showing that intact proteoform analysis can surface robust regional distinctions even at pilot scale.
  - Spatial/multimodal context: recent frameworks for integrating multimodal spatial omics highlight the need for clear, interpretable molecular axes; the paper’s matched-versus-spillover framing could be extended into spatial contexts and linked to integration methods from the spatial omics literature.
  - Broader proteomics advances (AI-enabled workflows, single-cell proteomics) emphasize detectability, missingness, and standardization; the paper’s transparency/traceability emphasis is aligned, but could better connect to these trends explicitly (data/ID standards, uncertainty modeling).
- Discussion of broader impact and significance
  - The work provides a pragmatic blueprint for extracting biologically coherent, proteoform-specific insights from limited public top-down data, highlighting the added value of intact proteoform views over protein-level summaries.
  - Its careful treatment of PTMs and detectability prevents overinterpretation and models best practices in conservative inference.
  - The clear, reproducible pipeline and evidence mapping should be useful to the community as a pattern for reanalyzing public top-down datasets and for designing future region-resolved experiments.

## Questions

1. Can you quantify how much of the low proteoform overlap could be explained by region-specific detection depth via an occupancy or hierarchical detection model (e.g., logistic/Beta-Binomial with region-specific effort parameters)?
2. Would you consider implementing an incidence misidentification adjustment (e.g., adapted Chao2/jackknife under misclassification) using an assumed or literature-based PrSM mis-ID rate to bound how much ID error could inflate uniqueness?
3. How sensitive are the alignment results to alternative marker curation schemes (e.g., gene-family expansions, stricter synonym handling) and to adopting ProForma 2.0 canonicalization for proteoform strings?
4. Could you provide a small orthogonal validation for a subset of key discriminating proteoforms (e.g., targeted MS or corroboration via bottom-up unique peptides), even if only for a handful of markers?
5. Do the intensity distributions of matched vs unique proteoforms differ systematically by region (e.g., unique entries being near detection limits), and if so, how does that affect your interpretation of functional separation?
6. Have you examined PTM localization scores or ambiguity flags in the source to stratify the PTM analysis by localization confidence, and do conclusions about acetylation persist under high-confidence subsets?
7. Could you formalize the prevalence-adjusted overlap effect size (e.g., centered Jaccard with CI or permutation-based intervals) to accompany the extremely small p-values and aid biological interpretation?
8. Are the code and artifacts archived with a permanent DOI, and do you provide a mapping to community standards (ProForma, PSI formats) to maximize reuse?

## Overall Assessment

This paper presents a careful, well-evidenced reanalysis that turns a qualitative narrative into a quantitative, proteoform-resolved statement: adult zebrafish telencephalon and optic tectum occupy distinct proteoform regimes, and the discriminating proteoforms align with known regional biology. The analyses are methodically constructed, robustness is convincingly demonstrated, and claims are appropriately scoped—particularly the cautious treatment of PTM asymmetry given detectability considerations. The main limitations stem from dependence on processed tables rather than raw-feature reanalysis and the absence of orthogonal validation or more comprehensive detectability/misidentification modeling. Nonetheless, the core claim is compelling and well-supported, and the transparency and reusability of the pipeline offer clear value to the community. I view this as a solid, carefully bounded contribution suitable for publication after addressing clarifications and, where feasible, adding modest methodological refinements (ProForma-aligned canonicalization, effect-size CIs, and an occupancy-style detectability check).
