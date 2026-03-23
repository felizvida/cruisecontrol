# Narrative Report

**Direction**: Battery-gated forward-only adaptation for battery-constrained quadruped robots  
**Chosen Idea**: Battery-gated forward-only adaptation with explicit compute-energy accounting  
**Venue Target**: ICLR-style demo paper  
**Status**: draft-with-known-gaps  
**Date**: 2026-03-23  
**Benchmark note**: This continuation uses the synthetic benchmark in `results/demo_benchmark.json` to exercise the full repo workflow. It is a sample artifact, not a claim of real robot performance.

## Executive Summary

The core research question is whether a quadruped should adapt continuously when battery is limited, or whether adaptation itself should be treated as a resource-budgeted action. The benchmark instantiated in this sample compares four policies: a static controller, periodic adaptation, always-on adaptation, and a battery-gated forward-only adaptation rule.

The synthetic results show a clean regime split. In low-battery terrain shift, the battery-gated policy raises mission return from `0.67` to `0.75` relative to always-on adaptation while reducing adaptation-compute energy from `0.56 Wh` to `0.13 Wh`. In low-battery payload shift, the same pattern holds: mission return rises from `0.69` to `0.77` while compute energy drops from `0.49 Wh` to `0.14 Wh`. In high-battery regimes, always-on adaptation remains competitive or slightly better in raw return, which supports a scheduling claim rather than a universal dominance claim.

The right paper story is therefore not "we invented a new TTA method." The stronger story is that once adaptation cost is priced explicitly, the preferred deployment strategy changes across battery regimes, and a lightweight gated rule can dominate always-on adaptation when the budget is tight.

## Core Claims

1. On the synthetic low-battery regimes in this sample, battery-gated forward-only adaptation outperforms always-on adaptation in mission return while consuming much less adaptation-compute energy.
2. High-battery regimes do not support a universal "gating always wins" claim; instead, they motivate a regime-aware scheduler.
3. The artifact set is sufficient to drive the repo’s paper-writing workflow end to end, including a compiled PDF.

## Claims-Evidence Matrix

| Claim | Evidence | Status | Notes |
|-------|----------|--------|-------|
| Low-battery gating improves the tradeoff | Terrain low battery: `0.75` vs `0.67`, payload low battery: `0.77` vs `0.69`; compute energy `0.13-0.14 Wh` vs `0.49-0.56 Wh` | Supported in synthetic benchmark | Needs real robot validation in a future project |
| High-battery regime changes the preferred policy | Terrain high battery: always-on `0.83`, gated `0.81`; payload high battery: always-on `0.84`, gated `0.83` | Supported in synthetic benchmark | Shows scheduling rather than one-size-fits-all adaptation |
| Cost accounting changes the crossover | Cost sweep: always-on `0.82 -> 0.49`, gated `0.80 -> 0.68` as cost scale rises from `0.25` to `2.0` | Supported in synthetic benchmark | This is the cleanest deployment-law style result in the sample |

## Experimental Setup

- **Benchmark type**: synthetic mission-level benchmark designed to exercise the full repo workflow
- **Shift families**: terrain shift and payload shift
- **Battery regimes**: `25%` and `80%`
- **Methods**: static, periodic adaptation, always-on adaptation, battery-gated forward-only adaptation
- **Metrics**: mission return, distance traveled, cost of transport, falls per `100m`, adaptation invocations, adaptation-compute energy
- **Data source**: `results/demo_benchmark.json`
- **Compute budget**: no GPU jobs; numbers are synthetic but structured to reflect the hypothesis produced by the earlier research stages

## Main Results

- **Terrain, low battery**: gated improves mission return by `+0.08` over always-on (`0.75` vs `0.67`) and cuts compute energy by `0.43 Wh`.
- **Payload, low battery**: gated improves mission return by `+0.08` over always-on (`0.77` vs `0.69`) and cuts compute energy by `0.35 Wh`.
- **Terrain, high battery**: always-on is slightly ahead in raw return (`0.83` vs `0.81`), but gated has lower cost of transport (`1.05` vs `1.07`) and much lower compute energy.
- **Cost sweep**: as adaptation-cost scale increases from `0.25` to `2.0`, always-on return drops by `0.33`, while gated drops by only `0.12`.

## Reviewer Pressure

- **Strongest objection**: the result could be dismissed as a composition of existing ideas unless the paper shows a clear regime split.
- **What was fixed**: the sample now centers the regime split, adds a main-results table and cost sweep, and explicitly labels the benchmark as synthetic.
- **What remains a limitation**: no real locomotion codebase or robot data is included in this repo.

## Figure Inventory

- **Fig 1**: controller schematic placeholder showing state, battery signal, gating rule, and forward-only adaptation branch
- **Fig 2**: regime-map placeholder summarizing when static, periodic, always-on, and gated policies dominate
- **Table 1**: mission results across the four benchmark regimes
- **Table 2**: adaptation-cost sweep
- **Table 3**: low-battery ablation of the gating rule

## Paper Framing

- **Working title**: Battery-Gated Adaptation for Battery-Constrained Quadruped Robots: A Synthetic End-to-End Workflow Demonstration
- **Target venue**: ICLR-style anonymous paper template using plain LaTeX
- **Paper type**: empirical systems/demo paper
- **Related-work buckets**:
  - rapid quadruped adaptation
  - energy-efficient locomotion
  - efficient test-time adaptation
- **Sections likely needed**:
  - Introduction
  - Related Work
  - Method
  - Synthetic Benchmark
  - Results
  - Discussion and Limitations
  - Conclusion

## Citations To Verify

- RMA / Kumar et al. 2021
- Fu et al. 2021 on energy and gait emergence
- Aboufazeli et al. 2023 on online stiffness and stride adaptation
- Hong et al. 2023 on MECTA
- Jia et al. 2024 on TinyTTA
- Xiao et al. 2026 on backprop-free embedding alignment

## Remaining Gaps

- Replace the synthetic benchmark with a real locomotion stack and measured energy instrumentation
- Validate the same crossover on at least two real disturbance families
- Replace placeholder figures with actual plots or diagrams from a real experiment run
