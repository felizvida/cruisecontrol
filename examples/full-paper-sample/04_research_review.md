# Research Review Memo

**Topic**: Battery-gated forward-only adaptation for battery-constrained quadruped robots  
**Date**: 2026-03-23  
**Workflow stage**: `research-review`

## Executive Assessment

- **Score**: 5.8/10
- **Verdict**: **Almost**, but not yet submission-ready
- **Reviewer stance**: Promising systems-and-ML paper if the experiment package is disciplined. Weak if it becomes a loose combination of existing ideas.

## What Works

1. The problem is real. Battery budget is a genuine deployment constraint for quadrupeds, and the literature does not yet appear to treat adaptation itself as a costed action.
2. The story connects two active areas that are usually separate: adaptive locomotion and efficient TTA.
3. The idea is falsifiable. If always-on adaptation still wins after battery accounting, the paper has learned something useful.

## Main Weaknesses

1. **Composition risk**  
   The current pitch sounds like "RMA plus efficient TTA plus energy cost." A reviewer can dismiss that unless the paper isolates a concrete new phenomenon.

2. **Evaluation ambiguity**  
   "Battery-aware" can become hand-wavy unless the paper specifies exactly how compute cost is measured or approximated.

3. **Control-layer uncertainty**  
   It is not yet clear whether the adaptation acts on latent context, normalization statistics, an embedding transform, or a small calibration head. That ambiguity weakens the method section.

4. **Missing failure story**  
   The paper needs to say when gating should *not* be used. Without that, the method risks looking overfit to one favorable regime.

## Minimum Fixes Before This Becomes Strong

1. **Commit to a precise adaptation primitive**
   - Best option for a first paper: a forward-only latent or embedding alignment mechanism
   - Avoid a full backprop-based adaptation loop unless the paper's entire point becomes "battery cost breaks standard TTA"

2. **Define a battery accounting model upfront**
   - Actuation energy proxy
   - Adaptation compute proxy
   - Inference latency or duty-cycle overhead
   - Remaining battery state

3. **Run a four-way ablation**
   - Static policy
   - Always-on adaptation
   - Fixed periodic adaptation
   - Battery-gated adaptation

4. **Use at least two shift families**
   - Terrain shift
   - Payload or morphology shift

5. **Report the regime diagram**
   - High battery / low shift
   - High battery / high shift
   - Low battery / low shift
   - Low battery / high shift

The paper gets much stronger if it shows the preferred strategy changes across these regimes.

## Minimum Viable Experiment Package

### Experiment 1: Mission-level battery tradeoff

- **Question**: Does gated adaptation improve task success or mission length under a fixed energy budget?
- **Metrics**: mission duration, falls, distance traveled, cost of transport, adaptation invocations, compute-energy proxy
- **Outcome needed**: gated beats always-on in at least one realistic low-battery regime

### Experiment 2: Sensitivity to shift type

- **Question**: Is the result specific to one terrain benchmark?
- **Metrics**: same as above, split by shift family
- **Outcome needed**: trend holds for both terrain and payload shift, even if effect size differs

### Experiment 3: Adaptation-cost sweep

- **Question**: Does the method still help when adaptation cost is scaled up or down?
- **Outcome needed**: clear threshold behavior, not just one tuned setting

### Experiment 4: Trigger analysis

- **Question**: What features drive the gating decision, and when does it fail?
- **Outcome needed**: interpretable trigger behavior rather than opaque switching

## Claims Matrix

| If results show... | Then claim... | Avoid claiming... |
|---|---|---|
| Gated adaptation consistently beats always-on under tight battery | Battery-aware scheduling changes the optimal deployment policy | A new general-purpose TTA algorithm |
| Gated adaptation matches always-on with lower cost | Lightweight scheduling preserves robustness more efficiently | Universal superiority across all regimes |
| Gains appear only in one regime | Battery-aware gating is useful in clearly specified mission conditions | Broad claims about legged adaptation in general |
| No gains after realistic cost accounting | Continuous adaptation may already be near-optimal for this controller class | Any novelty claim around deployment benefit |

## Recommendation

This is worth pursuing, but only with discipline. The paper should aim to discover a deployment law, not to present a grab-bag architecture. If the first round of experiments cannot show a clean regime shift where battery-aware gating matters, the idea should be narrowed into a smaller systems note or abandoned.
