# Breakthrough Plan

## Proposed Title Direction

**Serialized Structural Learning: Revisiting Space-Filling Curve Encodings with an Executable Context-Budget Probe**

## Upgraded Central Claim

The 2018 space-filling-curve mapping idea should no longer be framed as a workaround that lets 2D CNNs stand in for 3D CNNs. A stronger 2026 framing is that serialization is a general representation interface that can connect irregular 3D structures to efficient sequence-native architectures, especially when token efficiency and rich multi-channel semantics matter. The smallest honest way to strengthen that framing is to add a deterministic probe showing how orderings expose local structure under bounded sequence budgets.

## What Is Genuinely New Relative To The Source

1. A cross-era reinterpretation of the original method in light of 2021-2026 serialized 3D models
2. An executable context-budget probe comparing Hilbert, Morton, raster, and random orderings
3. A taxonomy of serialization strategies across voxel, point, and biomolecular settings
4. A design checklist for future biomolecular AI systems:
   - locality preservation
   - token efficiency
   - channel semantics
   - reversibility / interpretability

## Evidence Required

This paper is no longer purely conceptual. The evidence burden is:

- accurate reading of the source paper
- credible review of modern primary literature
- a coherent unifying framework
- a real executable probe with reproducible code and generated results
- explicit limits on what is and is not empirically established

## What Must Be Deleted From The Original Claim Set

- Any implication that the 2018 volumetric comparison is itself enough for a modern methods paper
- Any suggestion that the new paper contains a real biomolecular benchmark
- Any framing that treats 2D/1D CNN substitution as the main scientific story

## Figure / Table Plan

- **Table 1**: source paper vs upgraded paper
- **Table 2**: executable probe summary
- **Table 3**: taxonomy of serialization strategies
- **Table 4**: publication agenda for biomolecular serialization
- **Figure 1**: serialization-first view of structural learning
- **Figure 2**: locality and context-budget curves from the executable probe

## Risk Register

- **Risk**: the paper could still read like a retrospective blog post rather than a paper
  **Mitigation**: make the taxonomy and design framework precise, and anchor them with computation

- **Risk**: the probe could be mistaken for a real biomolecular benchmark
  **Mitigation**: keep the synthetic scope explicit in the paper, code, and review

- **Risk**: reviewers may expect a larger learned model
  **Mitigation**: position the paper as an interface paper with a deterministic probe, not as a full benchmark paper

## Why This Is Not Just A Facelift

### New contribution

A unifying serialization framework for modern 3D and biomolecular learning, strengthened by an executable context-budget study

### New evidence / theory

Cross-era synthesis from the 2018 source paper through 2024-2025 serialization and protein-structure papers, plus deterministic probe results generated in this repository

### What changed in the acceptance story

The paper stops trying to win on a dated benchmark comparison and instead argues for a broader, timely interface position with concrete design rules and a real computational vignette.
