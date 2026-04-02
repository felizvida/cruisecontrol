# round37 Review

Reviewed artifact: `paper/main_round36.pdf`

Backend: `paperreview.ai`

Score: `not returned by paperreview.ai`

Verdict: `Accept`

## Summary

This paper presents a careful reanalysis of a public, region-resolved top-down proteomics dataset of adult zebrafish telencephalon and optic tectum (Lubeckyj and Sun, 2022). Using accession+proteoform–level matching, prevalence-adjusted overlap statistics, detectability-aware sensitivity analyses, and curated marker panels, the authors show a strikingly low overlap of proteoforms between regions and a biologically coherent axis separating telencephalon (neuropeptide/synaptic) and optic tectum (reticulon/cytoskeletal/motor). They also revisit a reported N-terminal acetylation asymmetry and conclude it is not robust once simple detectability covariates are modeled, positioning the PTM result as a lead for future work rather than a settled claim.

## Strengths

- Technical novelty and innovation
  - The study leverages proteoform-resolved IDs from deposited spreadsheets to quantify regional overlap stringently at the accession+proteoform level, not merely by proteins.
  - Multiple, conservative sensitivity analyses (duplicate-informed occupancy, Chao2/jackknife richness, canonicalization diagnostics, misidentification ceilings) are thoughtfully designed for what the public tables can support.
  - Clear, auditable traceability (marker membership CSV, evidence JSON, code/manifests) enhances reproducibility and transparency.
- Experimental rigor and validation
  - Robustness is tested across exact vs canonicalized IDs, protein collapse, abundance weighting, and family-size–preserving randomization.
  - Prevalence-adjusted overlap tests and fixed-margin hypergeometric baselines avoid naive interpretations of Jaccard overlap.
  - A detectability-aware logistic model for acetylation with simple covariates avoids overclaiming on PTMs.
- Clarity of presentation
  - The main biological claims are clearly separated from sensitivity analyses and limitations; appendices carry computation details.
  - The framing is biologically grounded, connecting markers to known regional functions and providing independent literature-derived panels.
- Significance of contributions
  - Demonstrates that proteoform-level organization reveals sharper regional distinctions than protein-collapsed summaries, reinforcing the value of top-down, proteoform-aware analysis.
  - Provides a practical “how-to” for analyzing overlap structure and auditing claims from public top-down datasets, with implications for broader spatial proteomics.

## Weaknesses

- Technical limitations or concerns
  - No raw-file reprocessing; reliance on processed spreadsheets limits control over identification, localization confidence, and feature histories.
  - The occupancy/detectability corrections assume homogeneous detection probabilities within regions and may understate complex missingness or run effects.
  - Extremely small p-values derive from feature-level counts without biological replication structure; dependence among proteoforms may inflate nominal significance.
- Experimental gaps or methodological issues
  - The curated marker panel, while transparent and biologically motivated, may still encode selection bias; enrichment analyses (e.g., GO, pathway-level tests) are not reported.
  - The heavy enrichment for myosin/troponin in optic tectum invites scrutiny for potential dissection contamination or isoform annotation ambiguities; additional sentinel analyses could be expanded.
  - Limited exploration of alternative similarity metrics that consider shared proteoforms’ differential intensities beyond simple weighted Jaccard (e.g., Bray–Curtis results are mentioned but not detailed).
- Clarity or presentation issues
  - Some statistical machinery (e.g., Chao2/jackknife scaling variants) is summarized tersely in the main text; clearer intuition or a single consolidated figure could help non-specialists.
  - The logistic model for acetylation treats region as outcome; readers may expect acetylation as outcome with region as predictor for interpretability.
- Missing related work or comparisons
  - While the paper cites ProForma and spatial top-down MSI, it could better connect to broader calls for standardization and reproducibility in proteomics computational pipelines (e.g., single-cell proteomics lessons on missingness and batch handling).
  - Additional context on proteoform-aware population variation and isoform disambiguation would situate the accession+proteoform choices within current proteoform inference debates.

## Detailed Comments

- Technical soundness evaluation
  - The overlap analysis is well thought out: strict accession+proteoform units, canonicalization diagnostics, and protein-collapsed sensitivity cover key representation pitfalls. Prevalence-adjusted overlap tests with fixed margins are appropriate for the 2×2-like overlap setting. The duplicate-informed occupancy adjustment is reasonable but simplistic; heterogeneity of detectability across proteoforms/runs could be material, especially for large tectal totals.
  - The misidentification ceiling anchored to reported FDRs is a transparent way to bound overlap inflation; however, without access to site-localization confidence, PTM-level distinctions may be noisier than assumed.
  - The acetylation follow-up is cautious and appropriate; modeling detectability proxies (mass, span length, N-terminus proximity) is a sensible first step and the tempered conclusion is scientifically responsible.
- Experimental evaluation assessment
  - Given the constraints (public spreadsheets; no feature histories), the study pushes the available evidence about as far as is reasonable. Sensitivity checks are conservative and span multiple representations. That said, the absence of raw reprocessing, replicate-level random effects, and site-localization metadata remains a hard ceiling on inferential depth, particularly for PTMs.
  - The biological replication structure is unclear (technical duplicates per region); thus, statistical inferences at the proteoform level should be interpreted as descriptive of feature overlap rather than population-level sampling variability.
- Comparison with related work (using the summaries provided)
  - The paper’s emphasis on proteoform-resolved analysis and standards resonates with ProForma 2.0 efforts and proteoform-aware tools like ProHap Explorer, which advocate precise sequence/PTM/haplotype context. This work’s strict accession+proteoform matching is consistent with that direction.
  - The reproducibility and processing-choices theme aligns with Vanderaa and Gatto’s survey of single-cell proteomics pipelines, underscoring that analysis choices materially affect conclusions; the authors’ transparent, auditable pipeline and sensitivity analyses are in the spirit of those recommendations.
  - Imaging-based top-down work (e.g., Yang et al., 2022; Kiss et al., 2014) is positioned as complementary; future cross-validation against proteoform MSI would strengthen spatial claims.
  - The acetylation caution echoes broader concerns that PTM detection and quantification are sensitive to pipeline choices (paralleling issues raised in SCP and QSM pipeline studies), and complements computational PTM frameworks (e.g., PTM-Psi) and prediction tools (e.g., Deep-Ace) by grounding claims in observed detectability limits rather than model predictions.
- Discussion of broader impact and significance
  - The central finding—brain-region proteoform complements can be sharply distinct and biologically interpretable—advocates strongly for proteoform-aware spatial studies in neuroscience. It suggests that collapsing to proteins risks erasing meaningful regional texture.
  - Methodologically, the paper models a reproducible template for auditing public top-down datasets: emphasize strict identifiers, quantify overlap relative to prevalence baselines, probe detectability, and avoid overclaiming PTM biology without stronger evidence.
  - The work invites follow-on efforts: raw reprocessing with richer missingness models, expansion to additional brain regions, orthogonal spatial validation (MSI), and community-standardized deposition of feature histories and ProForma-rich annotations.

## Questions

1. Can you provide a detailed breakdown of the “myosin” and “troponin” accessions (non-muscle vs muscle isoforms) and any evidence (e.g., spectra-level uniqueness, gene annotations) that mitigates concerns about potential dissection contamination?
2. How sensitive are the overlap and marker-alignment conclusions to alternative canonicalization rules (e.g., partial localization retention, ProForma token parsing) or to grouping by gene symbols rather than accessions?
3. Could you report Bray–Curtis similarities (already computed) and any complementary abundance-aware metrics to further demonstrate that low overlap is not an artifact of binary presence/absence?
4. The detectability adjustment assumes homogeneous per-run detection probabilities. Did you explore simple heterogeneity stratifications (e.g., by mass bins or intensity quantiles) and, if so, did they materially change the Jaccard bounds?
5. For the acetylation model, would inverting the regression (acetylation as outcome, region as predictor) or restricting to proteoforms with unambiguous N-termini materially alter the effect estimates?
6. Can you share the exact code/environment bundle (or DOI) and a minimal computational notebook that reproduces Tables 1–5 and the figures to facilitate reuse by the community?

## Overall Assessment

This is a careful, well-argued reanalysis that extracts stronger, clearer biological conclusions from a published top-down dataset by emphasizing proteoform-resolved overlap, conservative sensitivity analyses, and auditable marker curation. The central conclusion—that adult zebrafish telencephalon and optic tectum are sharply distinct at the proteoform level along a biologically coherent axis—is convincingly supported within the study’s interpretive scope. The authors appropriately temper PTM-specific claims and are transparent about limitations stemming from reliance on processed spreadsheets. While the methodological novelty is incremental and the absence of raw reprocessing limits depth, the work is valuable to the community: it models best practices for proteoform-level overlap analysis, highlights the importance of standards and traceability, and makes a substantive biological point likely to generalize to other spatial neuroproteomics settings. I recommend acceptance after minor revisions focused on clarifying the isoform/contamination question for motor/cytoskeletal families, expanding abundance-aware similarity reporting, and tightening the acetylation modeling presentation.
