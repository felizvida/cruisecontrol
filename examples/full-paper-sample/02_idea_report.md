# Research Idea Report

**Direction**: Test-time adaptation for battery-constrained quadruped robots  
**Generated**: 2026-03-23  
**Workflow stage**: `idea-creator`  
**Ideas evaluated**: 5 generated -> 3 survived filtering -> 0 piloted -> 1 recommended

## Landscape Summary

Recent quadruped work shows that online adaptation is practical and useful under terrain shift, payload change, and disturbances. Recent efficient TTA work shows that adaptation itself can be made much cheaper through parameter-efficient or backprop-free updates. The opening is the missing deployment-level objective: adaptation should be judged by whether it improves mission success per unit battery, not just by whether it improves control performance in isolation.

## Recommended Ideas

### Idea 1: Battery-Gated Forward-Only Adaptation for Quadruped Locomotion

- **Hypothesis**: A quadruped can match or beat always-on adaptation under strict battery limits by using a lightweight forward-only adaptation module and only activating it when predicted robustness gains exceed its compute and energy cost.
- **Minimum experiment**: In simulation, compare four policies on terrain and payload shifts: static policy, always-on adaptation, periodic adaptation, and battery-gated forward-only adaptation.
- **Expected outcome**: Gated adaptation keeps most of the robustness gain while lowering total mission energy and late-episode failure rate.
- **Novelty**: 7/10
- **Closest work**: RMA for rapid locomotor adaptation, online leg stiffness/stride tuning for energy efficiency, and backprop-free embedding-alignment TTA for efficient online adaptation.
- **Feasibility**: Moderate. Needs a simulated battery model, an adaptation trigger, and a low-overhead adaptation layer or latent-context update. No new hardware is required for the first paper.
- **Risk**: MEDIUM
- **Contribution type**: empirical finding + deployment method
- **Pilot result**: SKIPPED. This repo does not include a target locomotion codebase or GPU experiment environment.
- **Reviewer's likely objection**: "This is a composition of existing ideas unless the battery-aware trigger reveals a new operating regime or produces a clear deployment law."
- **Why we should do this**: The idea creates a falsifiable deployment question and directly addresses the gap between robust locomotion papers and efficient TTA papers.

### Idea 2: Dual-Timescale Adaptation With Battery-Aware Mode Switching

- **Hypothesis**: Splitting adaptation into a fast cheap latent update and a slower higher-quality update can improve performance early in an episode while preserving battery later.
- **Minimum experiment**: Compare a two-timescale controller against always-fast and always-slow adaptation schedules.
- **Expected outcome**: Better battery-adjusted robustness curves, especially under mixed terrain sequences.
- **Novelty**: 6/10
- **Closest work**: RMA-style latent adaptation plus efficient TTA scheduling papers.
- **Feasibility**: Moderate to high.
- **Risk**: MEDIUM
- **Contribution type**: deployment method
- **Pilot result**: SKIPPED
- **Reviewer's likely objection**: "This may look like engineering unless the scheduling law is principled."
- **Why this is a backup**: It is probably easier to implement than Idea 1, but also easier for reviewers to dismiss as systems tuning.

### Idea 3: Energy-Calibrated Adaptation Trigger From Cost-of-Transport Forecasts

- **Hypothesis**: Short-horizon predictions of cost of transport and slip risk can predict whether adaptation is worth the compute cost before a failure happens.
- **Minimum experiment**: Learn or estimate a simple trigger function from recent proprioceptive history and compare trigger quality against heuristic schedules.
- **Expected outcome**: The learned trigger outperforms fixed adaptation intervals.
- **Novelty**: 5.5/10
- **Closest work**: Online energy-efficiency tuning papers for quadrupeds.
- **Feasibility**: High.
- **Risk**: LOW to MEDIUM
- **Contribution type**: diagnostic / systems paper
- **Pilot result**: SKIPPED
- **Reviewer's likely objection**: "The trigger alone may be too narrow for a full paper."
- **Why this is not the lead**: Better as a component of Idea 1 than as the headline contribution.

## Eliminated Ideas

| Idea | Reason eliminated |
|---|---|
| Continuous backprop-based TTA on the locomotion policy | Too expensive for the claimed battery-constrained setting; review would immediately ask why a cheaper adaptation path is not used |
| Purely energy-minimizing gait adaptation with no TTA framing | Too close to existing online energy-efficiency tuning work |
| Apply TinyTTA directly to quadruped perception stack | Risks becoming a narrow transfer paper unless tightly coupled to a locomotion question |

## Pilot Experiment Results

| Idea | GPU | Time | Key Metric | Signal |
|---|---|---:|---|---|
| Battery-Gated Forward-Only Adaptation | N/A | N/A | N/A | SKIPPED: this repo has no locomotion codebase or experiment harness |
| Dual-Timescale Adaptation | N/A | N/A | N/A | SKIPPED |
| Energy-Calibrated Trigger | N/A | N/A | N/A | SKIPPED |

## Suggested Execution Order

1. Start with **Idea 1**. It has the cleanest paper story and the strongest gap against current literature.
2. Implement **Idea 3** as a subcomponent of Idea 1, not as its own paper.
3. Keep **Idea 2** as a fallback if the full battery-gated mechanism is too hard to stabilize.

## Next Steps

- [ ] Build a minimal simulated battery model that accounts for actuation energy and adaptation compute cost
- [ ] Choose the lightweight adaptation mechanism: latent-context update, normalization-stat alignment, or forward-only embedding alignment
- [ ] Benchmark static, periodic, always-on, and gated schedules
- [ ] Run a focused novelty check on Idea 1 before implementation
- [ ] If novelty holds, move into a real target project with a filled `AGENTS.md` and then use `/run-experiment`
