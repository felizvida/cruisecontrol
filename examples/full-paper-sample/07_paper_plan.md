# Paper Plan

**Title**: Battery-Gated Adaptation for Battery-Constrained Quadruped Robots: A Synthetic End-to-End Workflow Demonstration  
**Venue**: ICLR-style sample paper  
**Type**: empirical systems/demo paper  
**Date**: 2026-03-23  
**Page budget**: 9 pages main body  
**Section count**: 7 + appendix

## Claims-Evidence Matrix

| Claim | Evidence | Status | Section |
|-------|----------|--------|---------|
| Low-battery gating improves mission utility relative to always-on adaptation in this synthetic benchmark | Table 1 low-battery terrain/payload rows | Supported | §5 |
| High-battery regimes change the preferred adaptation policy | Table 1 high-battery rows | Supported | §5 |
| Explicit adaptation-cost accounting creates a crossover result | Table 2 cost sweep | Supported | §5 |
| The repo can produce a full paper artifact set end to end | Compiled PDF + paper artifact tree | Supported | §6/§7 |

## Structure

### §0 Abstract

- Problem: adaptation helps quadrupeds, but adaptation also costs battery
- Approach: battery-gated forward-only adaptation on a synthetic benchmark
- Key result: gating wins in low-battery regimes and remains competitive elsewhere
- Scope note: this is a workflow demonstration, not a real robot study

### §1 Introduction

- Motivate battery-constrained legged deployment
- State the gap between locomotion adaptation and efficient TTA
- Introduce the sample benchmark and the four-way comparison
- List contributions:
  - a battery-aware scheduling hypothesis
  - a synthetic regime benchmark
  - a fully traced artifact path from idea to paper

### §2 Related Work

- Rapid locomotor adaptation
- Energy-aware gait tuning
- Efficient and backprop-free TTA
- Position this sample as a synthesis and workflow demonstration

### §3 Method

- Define the forward-only adaptation primitive
- Define the gating score using predicted robustness gain, compute-energy cost, and battery state
- Explain why the claim is about scheduling rather than a new TTA algorithm

### §4 Synthetic Benchmark

- Define regimes: terrain/payload × low/high battery
- Define metrics
- Explain that benchmark values are stored in `results/demo_benchmark.json`
- Explain the role of the benchmark in the repo sample

### §5 Results

- Table 1: main regime results
- Table 2: adaptation-cost sweep
- Table 3: low-battery ablation
- Figure 1: controller schematic placeholder
- Figure 2: regime-map placeholder

### §6 Discussion and Limitations

- What the crossover means
- Why high-battery regimes do not justify a universal claim
- Limits of the synthetic benchmark
- What a real follow-on project must validate

### §7 Conclusion

- Re-state the scheduling hypothesis
- Re-state that the sample proves artifact completeness, not robotics novelty

### Appendix

- File inventory
- Synthetic benchmark schema

## Figure Plan

| ID | Type | Description | Data Source | Priority |
|----|------|-------------|-------------|----------|
| Fig 1 | Placeholder schematic | Battery-gated adaptation controller block diagram | manual placeholder | HIGH |
| Fig 2 | Placeholder regime map | Which policy wins by battery/shift regime | manual placeholder | MEDIUM |
| Table 1 | Comparison table | Main results across four regimes | `results/demo_benchmark.json` | HIGH |
| Table 2 | Comparison table | Adaptation-cost sweep | `results/demo_benchmark.json` | HIGH |
| Table 3 | Comparison table | Low-battery ablation | `results/demo_benchmark.json` | MEDIUM |

## Citation Plan

- §1 Intro: Kumar et al. 2021, Fu et al. 2021, Xiao et al. 2026
- §2 Related: Kumar et al. 2021, Aboufazeli et al. 2023, Hong et al. 2023, Jia et al. 2024, Xiao et al. 2026
- §3 Method: Xiao et al. 2026, Hong et al. 2023, Jia et al. 2024
- §4 Benchmark: no new citations beyond method framing

## Reviewer Feedback Applied

- Added an explicit synthetic-benchmark note
- Centered the paper around the regime split rather than a universal superiority claim
- Added tables that make the crossover visible without relying on external figures

## Next Steps

- [ ] Render the tables from `results/demo_benchmark.json`
- [ ] Draft LaTeX into `paper/`
- [ ] Compile `paper/main.pdf`
- [ ] Preserve the improvement log alongside the final PDF
