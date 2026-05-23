# Round 39 Review

Reviewed artifact: `examples/codex-zebrafish-brain-paper-14rounds/paper/main.pdf`

Backend: `paperreview.ai`

Score: `not returned by paperreview.ai`

Verdict: `Weak Accept`

## Summary

This paper reanalyzes a publicly available LCM-CZE-MS/MS top-down proteomics dataset from adult zebrafish to quantify and interpret proteoform-level overlap between telencephalon and optic tectum. The authors show that the regions share very few intact proteoforms (29–35 across ~800 total, Jaccard ≈ 0.03–0.06 across matching schemes), and that region-enriched proteoforms align with expected biology (neuropeptide/synaptic markers in telencephalon; reticulon/cytoskeletal/motor markers in optic tectum). Extensive sensitivity analyses (identifier canonicalization, protein/gene collapse, detectability corrections using duplicates, misidentification bounds, abundance-weighted similarities) preserve the low-overlap conclusion, while an apparent telencephalon bias in N-terminal acetylation weakens after adjusting for detectability.

## Strengths

- Technical novelty and innovation
  - Introduces a clear, accession+proteoform identity unit of analysis and contrasts it with protein/gene collapse to show how biological conclusions change with identifier granularity.
  - Applies prevalence-adjusted overlap baselines, multiple similarity metrics (Jaccard, Sørensen, Bray–Curtis, weighted Jaccard), and duplicate-informed detectability corrections (including Chao2/jackknife estimates) to stress-test conclusions.
  - Uses canonicalization of proteoform strings to dissect representation versus biology and leverages conservative misidentification ceilings tied to reported FDR levels.
- Experimental rigor and validation
  - Convergent evidence for low overlap across strict, relaxed, and protein-collapsed representations, with quantitative bounds showing only modest increases under detectability/error scenarios.
  - Marker-family enrichment assessed with exact tests, Wilson intervals, and family-size-preserving randomization; effects remain robust after excluding motor families and after protein collapse.
  - PTM analysis is handled cautiously; logistic models with covariates explain why the acetylation asymmetry is not stable, preventing overreach.
- Clarity of presentation
  - The paper is transparent about interpretive limits (processed tables rather than raw feature histories) and focuses its strongest claims where the data are most direct.
  - Key metrics and assumptions are articulated in an appendix; robustness checks are clearly enumerated and tied to available spreadsheet fields.
- Significance of contributions
  - Demonstrates that proteoform-resolved analysis yields regional distinctions that protein-level summaries dilute, underscoring the biological value of intact-proteoform measurements.
  - Provides a concrete, reproducible case study that connects regional neurobiology to proteoform states, relevant to spatially resolved proteomics and neurobiology.

## Weaknesses

- Technical limitations or concerns
  - Reliance on processed region spreadsheets precludes feature-level reanalysis, assessment of PTM localization confidence, or recalculation of spectrum-level FDRs and may mask upstream identification/quantification biases.
  - The duplicate-based occupancy/detectability model is first-order and likely understates complex MNAR missingness and ID-dependent detection heterogeneity; independence assumptions in the product-of-probabilities approach may be optimistic.
  - The prevalence-adjusted Jaccard “independence baseline” and centered Jaccard are not fully formalized; uncertainty around these baselines and their variance is not quantified.
- Experimental gaps or methodological issues
  - No new measurements or orthogonal validation (immunostaining, bottom-up quantification, MSI) to corroborate regional assignments or tissue purity.
  - Lack of biological replicates and explicit LCM purity metrics; potential contamination (e.g., muscle-like myosin/troponin proteoforms) complicates interpretation despite sensitivity exclusions.
  - The curated marker panel could reflect confirmation bias; selection criteria and completeness are only briefly described.
- Clarity or presentation issues
  - Some figure placeholders and minor typographical artifacts remain; equations/metrics would benefit from more explicit definitions and uncertainty estimates.
  - Implementation details (e.g., exact canonicalization rules, code availability) are referenced but not linked; reproducibility would benefit from a public repository.
- Missing related work or comparisons
  - While several key references are cited, the paper could further contextualize against broader regional proteomics (bottom-up) and other top-down spatial studies; discussion of bottom-up proteoform inference methods (e.g., HIquant) is relevant to contrast direct top-down evidence versus inference from shared peptides.
  - Additional discussion of single-cell or subregion heterogeneity (and how LCM region-level profiles relate) would strengthen context.

## Detailed Comments

- Technical soundness evaluation
  - The core overlap findings are soundly supported by simple, transparent counts that are robust across multiple matching schemes and identifier granularities. The use of accession+proteoform IDs is appropriate given string reuse across accessions.
  - Detectability correction via duplicate incidence and Chao2/jackknife richness modeling is a reasonable first step with the available flags, but a fuller MNAR-aware model (as advocated in the proteomics statistics literature) would better bound hidden sharing. Explicit confidence intervals for adjusted Jaccard values would make the corrections more interpretable.
  - The conservative misidentification ceilings grounded in reported FDRs are a defensible stress test; however, without access to raw search results and localization probabilities, PTM-level conclusions should remain guarded (as the authors acknowledge).
- Experimental evaluation assessment
  - The study’s strength is triangulation rather than new experimentation. Within that scope, the sensitivity analyses are unusually thorough and appropriately cautious.
  - The acetylation analysis demonstrates good statistical hygiene: conditioning on matched markers, adjusting for mass/length/N-terminal proximity, and reversing the model to test robustness. The conclusion (signal not yet stable) is appropriately conservative.
  - The strong marker alignment, even after excluding motor families and after protein collapse, supports a meaningful biological axis; however, direct purity controls or orthogonal assays would mitigate concerns that some tectal “motor” signals reflect contamination rather than genuine regional biology.
- Comparison with related work (using the summaries provided)
  - The work complements top-down MSI efforts (e.g., LAESI-FT-ICR; broader MSI instrumentation advances) by trading spatial pixels for proteoform depth, consistent with the authors’ discussion. Unlike MSI, this analysis achieves higher proteoform diversity but loses intra-section localization.
  - The handling of missingness and detection bias is directionally aligned with statistical recommendations (e.g., Karpievitch et al. emphasizing intensity-dependent missingness and the risks of naïve imputation). The present occupancy model could evolve toward censored-likelihood or joint models if raw data become available.
  - Bottom-up proteoform inference (e.g., HIquant) targets related conceptual goals from peptide mixtures; this paper usefully highlights that direct top-down observation at intact level delivers orthogonal evidence for regional specialization that protein- or peptidoform-collapsed views may obscure.
  - Broader perspectives emphasize the importance of reanalyzing MS data and adopting standards and automation; this paper’s emphasis on ProForma and on representation-vs-biology effects resonates with that agenda.
- Discussion of broader impact and significance
  - The study reinforces that intact proteoforms encode region-specific biology beyond protein presence/absence and provides a concrete, analyzable benchmark for future spatially resolved top-down datasets.
  - It motivates better reporting standards (ProForma 2.0 compliance, exposure of feature histories, replicate structure) and richer statistical handling of missingness and localization—practical steps that will benefit the field.
  - The cautious stance on PTM asymmetries is a positive example for rigorous interpretation in small, heterogeneous datasets.
  - If extended to additional brain regions and supported by raw data and orthogonal assays, this line of work could underpin proteoform atlases that integrate with single-cell and imaging modalities.

## Questions

1. Can you release the exact code and canonicalization rules used for accession+proteoform matching, prevalence-adjusted baselines, and detectability corrections to facilitate full reproducibility?
2. How were the curated marker families specified a priori (gene symbols, description keywords)? Could you provide a preregistered or literature-sourced list to mitigate selection bias, and how sensitive are conclusions to alternative marker definitions?
3. The prevalence-adjusted “independence baseline” for the Jaccard index is central to your centered Jaccard statistic. Please provide the exact formula, distributional assumptions, and (ideally) uncertainty estimates for these baselines.
4. The duplicate-based occupancy model assumes independent detection across runs and across regions. Did you evaluate correlations in detectability (e.g., intensity-dependent or proteoform-specific) and, if so, how would that affect adjusted overlap estimates?
5. Can you quantify the potential impact of LCM purity (e.g., myelin or muscle-like contamination) using available accession annotations or external tissue markers, and could you share a sensitivity analysis that downweights or excludes likely off-target tissue classes?
6. For the acetylation analysis, did you assess spectrum- and site-localization confidence (e.g., ambiguity in N-terminal assignments) and how might localization uncertainty propagate to the logistic models?
7. Would your conclusions change if you normalized for total identification counts per region (e.g., using rarefaction or subsampling to the smaller region total), and can you provide the corresponding overlap and marker-alignment metrics?
8. Are raw TopPIC search outputs and feature histories accessible or could they be deposited to enable feature-level reanalysis and more advanced MNAR models?

## Overall Assessment

This is a careful and well-reasoned reanalysis that extracts a clear, biologically coherent result from a modest but information-rich top-down dataset: adult zebrafish telencephalon and optic tectum occupy sharply distinct proteoform states, and those distinctions align with expected neurobiological roles. The authors convincingly separate representational artifacts from biology, quantify overlap under multiple views, and appropriately temper PTM-level claims. The main limitations are the absence of raw-data reprocessing, reliance on processed tables, limited replicates/purity information, and the lack of orthogonal validation. As a contribution to the proteoform and spatial proteomics community, the work is valuable for its methodological transparency and as a reference point illustrating how identifier granularity changes biological interpretation. Its originality lies more in the synthesis and robustness of the analysis than in new algorithms or experiments. I view it as a strong case study and a constructive nudge toward better standards and statistical practice; suitability for a top-tier venue depends on its appetite for rigorous reanalyses without new data. I lean toward a weak accept, contingent on releasing code and clarifying key methodological details (baselines, canonicalization, occupancy model), as these steps would maximize reproducibility and community value.
