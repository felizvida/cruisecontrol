# Round 16 paperreview.ai Review

Reviewed artifact: `examples/codex-zebrafish-brain-paper-14rounds/paper/main_round15.pdf`

Backend: `paperreview.ai`

Score: `not returned by paperreview.ai`

Verdict: `Borderline`

## Summary

This paper presents a quantitative, fully reproducible re-analysis of a 2022 top-down proteomics pilot that profiled adult zebrafish telencephalon and optic tectum using LCM-CZE-MS/MS. By extracting counts reported in the original paper and reframing them into explicit region-separation and marker-alignment statistics, the authors demonstrate very low proteoform-level overlap between regions (Jaccard = 0.0434) and strong alignment of curated functional markers with their biologically expected regions (overall alignment 0.9766; one-sided exact-test p = 5.12×10^-22), supported by stress tests. The work does not generate new acquisitions or reprocess raw data; instead, it contributes a compact and auditable computational summary, code, and sensitivity analyses that sharpen and substantiate the original study’s qualitative claims.

## Strengths

- Technical novelty and innovation
  - Reframes a narrative interpretation into a clear matched-versus-spillover and region-separation problem with explicit metrics (Jaccard, Wilson CIs, exact tests, odds ratios).
  - Provides a reproducible, inspectable analysis package (manifests, scripts, evidence files), increasing auditability and reuse of published proteomics results.
  - Introduces thoughtful stress tests (pessimistic reassignment; motor-family exclusion) to probe robustness to curation and contamination concerns.

- Experimental rigor and validation
  - Mathematical checks are internally consistent (e.g., union cardinality, odds ratio from the 2×2 table).
  - Statistical choices (Wilson intervals, Fisher’s exact one-sided test) are appropriate for sparse off-diagonals and directional hypotheses.
  - Sensitivity analyses are clearly described and leave main conclusions intact.

- Clarity of presentation
  - Clear articulation of scope and limits (no raw-data reprocessing; curated marker focus).
  - Straightforward exposition of metrics, counts, and logic of the baseline prevalence control.
  - Good separation of claims by strength, with a “claim-to-evidence” mapping and explicit rebuild instructions.

- Significance of contributions
  - Demonstrates how a modest, published spatial proteomics pilot can be converted into an auditable quantitative argument, likely improving trust and reusability of similar small-scale studies.
  - Highlights the importance of proteoform-level resolution in regional comparisons and explicitly quantifies the PTM layer reported in the source study.

## Weaknesses

- Technical limitations or concerns
  - Heavy reliance on curated, named marker families from the original paper risks selection bias and may inflate perceived alignment compared to an objective proteome-wide test.
  - No abundance weighting, feature-level FDR integration, or replicate-level incidence modeling; hence, cannot correct for missing detections or quantify uncertainty at the proteoform ID level.
  - The PTM quantification is purely descriptive and not tied back to functional alignment (e.g., whether modified species drive regional differences).

- Experimental gaps or methodological issues
  - Absence of raw TopPIC outputs or a per-feature supplementary table prevents validation of identification confidence, localization probabilities, and replicate detection spectra.
  - Jaccard and overlap estimates are based on aggregate counts rather than explicit proteoform-ID lists; this constrains the depth of statistical inference and may obscure ID redundancy.
  - No orthogonal validation (e.g., transcriptomic markers, imaging) to arbitrate contamination versus true biological enrichment for high-abundance motor/cytoskeletal families.

- Clarity or presentation issues
  - A few figure descriptions are approximate (e.g., shared proteoforms “~50” in a schematic despite text reporting 35), which could confuse readers; the paper acknowledges rendering artifacts but should ensure numeric consistency in all visual summaries.
  - The baseline calculation is correct but could be motivated more explicitly to avoid misinterpretation as restatement of region totals.

- Missing related work or comparisons
  - Limited discussion connecting MS-based spatial proteomics with broader spatial-omics methods and recent foundation models for spatial proteomics/transcriptomics and imaging (e.g., KRONOS, HEIST), which could contextualize the work’s role in the ecosystem of analysis and reproducibility tools.
  - Minimal comparison to alternative similarity metrics (e.g., Sørensen-Dice) or incidence-corrected estimators beyond citing Chao et al.; a brief rationale for metric choice would strengthen methodological framing.

## Detailed Comments

- Technical soundness evaluation
  - The set-based metrics and exact tests are appropriate for the reported counts and directional hypotheses. The OR = 1173 derived from the 2×2 table is correctly computed; the wide CI due to sparse off-diagonals is expected and appropriately framed.
  - The prevalence-adjusted baseline for alignment (weighted by regional totals) appropriately guards against triviality from unbalanced region sizes. The reported lift is thus meaningful.
  - The stress-test design is sensible given data constraints. The Haldane correction is appropriate for zero cells after excluding motor families.

- Experimental evaluation assessment
  - The analysis is constrained by the absence of raw feature tables and replicate-level detection histories. As acknowledged, this prevents abundance weighting, ID-level FDR integration, and unseen-overlap corrections.
  - The curated marker approach improves interpretability but introduces a risk of confirmation bias. The authors partially mitigate this via a sign test and leave-one-out analysis demonstrating family-level consistency.
  - PTM summaries confirm that proteoform-level detail is biologically substantive in this dataset, but the work stops short of relating PTM categories to region-level alignment or function.

- Comparison with related work (using the summaries provided)
  - Recent work (KRONOS) advances representation learning for spatial proteomics imaging data, and HEIST provides hierarchical representations for spatial transcriptomics/proteomics primarily at the single-cell/molecular count level. In contrast, this paper addresses top-down MS proteoforms and focuses on auditability and explicit statistical framing rather than representation learning or predictive modeling.
  - NovoBench targets de novo peptide sequencing, orthogonal to the proteoform-level re-analysis here. The benchmark mindset, however, resonates with this paper’s emphasis on comparability, explicit metrics, and robust evaluation—even if the present study does not introduce a benchmark per se.
  - The paper would benefit from explicitly situating MS-based spatial proteomics alongside these broader spatial-omics and imaging paradigms to highlight complementary roles: this work trades scale and modeling sophistication for proteoform specificity and reproducible, auditable statistical summaries.

- Discussion of broader impact and significance
  - The core contribution—turning scattered counts into a compact, testable argument with code—addresses a persistent pain point in small-scale spatial proteomics: reproducibility and clarity of biological interpretation.
  - While limited in scope (no raw reprocessing or proteome-wide inference), the approach is generalizable to other small published studies and could seed a culture of standardized summaries and stress tests.
  - The work could help bridge communities: experimentalists seeking interpretable evidence for regional specialization and computational groups advocating for transparent, reusable analysis pipelines.

## Questions

1. Can you share a machine-readable mapping from every numeric value used in your evidence file back to its source location in the 2022 paper (e.g., figure/panel, paragraph), to fully close the audit trail?
2. Could you provide an explicit comparison of alternative set-similarity metrics (e.g., Sørensen-Dice) and briefly justify choosing Jaccard for the main text? Do any conclusions change materially?
3. How robust are the alignment and separation metrics to plausible ID redundancy within marker families (e.g., near-duplicate proteoforms or charge-state artifacts) given the lack of raw TopPIC feature tables?
4. Would it be feasible to perform a limited unseen-overlap sensitivity analysis by bracketing detection-probability scenarios informed by the duplicate means/SDs (e.g., a simple beta-binomial or bootstrap over replicate recoveries) to quantify potential bias in Jaccard?
5. Can you extend the PTM analysis to test whether specific PTM categories (e.g., N-terminal acetylation) show regionally biased incidence within the curated marker panel, thereby connecting the PTM layer to the alignment result?
6. For the motor/cytoskeletal families enriched in optic tectum, can you incorporate orthogonal support (e.g., literature on tectal axonal tracts, or scRNA-seq markers from Pandey et al.) to help distinguish biological enrichment from contamination?
7. Would you consider adding a brief discussion contrasting MS-based spatial proteomics with imaging-based spatial proteomics (e.g., KRONOS) and spatial multi-omics models (e.g., HEIST), clarifying the niche of top-down proteoform re-analyses within this landscape?

## Overall Assessment

This is a careful and useful quantitative re-analysis that enhances the interpretability and auditability of an existing spatial top-down proteomics pilot. The central claims—strong proteoform-level regional separation and high alignment of curated markers with expected regional function—are well supported by transparent computations and sensible stress tests. The scope is deliberately narrow, which keeps the contribution crisp but also limits broader impact: the study does not reprocess raw data, cannot leverage abundance/FDR/incidence information, and relies on a curated marker set that risks selection bias despite reasonable mitigation. For a top-tier venue, the novelty is primarily in framing and reproducibility rather than new biological discovery or methodological development; nonetheless, the work has clear value to the spatial proteomics community as a model for making small studies quantitatively auditable. I view this as a strong workshop/short-paper contribution or a solid resource note; for a full research track at a top-tier venue, it is borderline due to limited originality and scope. Strengthening contextualization with broader spatial-omics work, adding orthogonal validation for potential contamination, and providing additional sensitivity analyses around unseen overlap would improve its reach and robustness.
