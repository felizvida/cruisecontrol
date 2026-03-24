# Narrative Report

## Working Title

Function Follows Proteoform: A Computation-Backed Re-analysis of Adult Zebrafish Telencephalon and Optic Tectum Top-Down Proteomics

## Executive Summary

This project re-analyzes a published 2022 top-down proteomics pilot study of adult zebrafish telencephalon and optic tectum. The local computation does not invent new mass-spectrometry measurements; instead, it turns the paper's published counts into an auditable quantitative argument about regional specialization, function-aligned marker concentration, technical sensitivity, and post-translational modification burden.

## Core Claims

1. Adult zebrafish telencephalon and optic tectum are sharply separated at the proteoform level.
2. The published marker proteoforms are concentrated in the regions whose known biological functions they should support.
3. The pilot dataset is small but already rich enough to support a reproducible computational biology note.
4. The PTM layer is large enough that the dataset should be discussed at the proteoform level rather than collapsed to protein identities alone.

## Claim-Evidence Matrix

| Claim | Evidence | Source path |
|-------|----------|-------------|
| Strong regional separation | Jaccard overlap = 0.0434; protein overlap fraction = 0.2151; unique fractions = 0.8867 and 0.9343 | `results/summary_metrics.json`, `results/region_summary.csv` |
| Function-aligned marker concentration | Tel axis = 23 matched vs 2 spillover; Teo axis = 102 matched vs 1 spillover; odds ratio = 1173; one-sided exact p = 5.12e-22 | `results/axis_summary.csv`, `results/functional_test.json`, `results/marker_bias.csv` |
| Robustness of the alignment claim | Leave-one-out alignment remains above 0.969 | `results/leave_one_out_alignment.csv` |
| PTM-rich dataset | 358/807 identified proteoforms carry mass shifts; 211 are N-terminally acetylated | `results/ptm_summary.csv`, `results/summary_metrics.json` |
| Pilot technical sensitivity | Duplicate means 232 and 356 proteoforms; single-run high water mark 418 with about 250 cells worth of injected material | `results/technical_replicate_summary.csv`, `results/summary_metrics.json` |

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

- The computation uses values recoverable from the article text and figure discussion, not a full raw-data reprocessing workflow.
- The function-alignment claim is about a curated marker panel, not the entire proteome.
- The biological interpretation should remain conservative because this is a pilot study with technical replicates rather than a large cohort.

