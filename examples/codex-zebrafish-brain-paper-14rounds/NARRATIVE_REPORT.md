# Narrative Report

## Working Title

Distinct Proteoform Profiles Mark Adult Zebrafish Telencephalon and Optic Tectum

## Executive Summary

This project analyzes a published 2022 top-down proteomics pilot study of adult zebrafish telencephalon and optic tectum. The local computation does not invent new mass-spectrometry measurements; instead, it turns the article counts and deposited region spreadsheets into a quantitative argument about regional specialization, function-aligned marker concentration, duplicate-level detectability, representation effects, and post-translational modification burden.

## Core Claims

1. Adult zebrafish telencephalon and optic tectum are sharply separated at the proteoform level.
2. The published marker proteoforms are concentrated in the regions whose known biological functions they should support.
3. The regional split survives conservative checks for unequal list size, duplicate-level detectability, low-intensity identifications, plausible identifier error, and marker-panel composition.
4. The PTM layer is large enough to justify proteoform-level interpretation, but the apparent acetylation contrast remains provisional after covariate and first-residue checks.

## Claim-Evidence Matrix

| Claim | Evidence | Source path |
|-------|----------|-------------|
| Strong regional separation | article Jaccard overlap = 0.0434; strict exact-ID Jaccard overlap = 0.0360; occupancy-adjusted exact-ID Jaccard = 0.0432; protein overlap fraction = 0.2151 | `results/summary_metrics.json`, `results/region_summary.csv`, `results/source_table_overlap_metrics.csv` |
| Function-aligned marker concentration | Tel axis = 23 matched vs 2 spillover; Teo axis = 102 matched vs 1 spillover; odds ratio = 1173; one-sided exact p = 5.12e-22 | `results/axis_summary.csv`, `results/functional_test.json`, `results/marker_bias.csv` |
| Robustness of the alignment claim | Leave-one-out alignment remains at or above 0.9625; motor-family exclusion alignment = 0.9310; top-100 intensity-restricted marker alignment = 1.0000 | `results/leave_one_out_alignment.csv`, `results/top_intensity_restriction.csv`, `results/motor_family_breakdown.csv` |
| Tissue-purity guardrail | Skeletal/cardiac muscle sentinels are tectal-heavy, but the non-motor marker axis remains aligned | `results/tissue_purity_sentinels.csv`, `results/tissue_purity_sentinel_membership.csv` |
| PTM-rich but cautious dataset | 358/807 identified proteoforms carry mass shifts; 211 are N-terminally acetylated; adjusted acetylation model p = 0.140 | `results/ptm_summary.csv`, `results/acetylation_covariate_sensitivity.csv`, `results/summary_metrics.json` |
| Pilot technical sensitivity | Duplicate means 232 and 356 proteoforms; public files expose duplicate technical runs rather than biological replication across animals | `results/technical_replicate_summary.csv`, `results/summary_metrics.json` |

## Figure Plan

1. `fig1_region_overview`
   Two-panel overview of regional totals and unique/shared counts.

2. `fig2_marker_bias`
   Marker-level log-bias chart showing the separation of telencephalon-associated and optic-tectum-associated proteoforms.

3. `fig3_axis_alignment`
   Axis-level concentration plus leave-one-out robustness plot.

4. `fig4_ptm_and_sensitivity`
   PTM inventory and technical sensitivity panel.

## Limitations

- The computation uses the article, supplement, and deposited region spreadsheets, not a full raw-feature reprocessing workflow.
- The function-alignment claim is strongest for curated and independently checked marker panels, not for every proteoform in the dataset.
- The biological interpretation should remain conservative because the public files expose duplicate technical runs rather than a biological-replicate design across animals.
- Tissue-sentinel screens are useful guardrails, but they are not a substitute for direct histological purity measurements.
