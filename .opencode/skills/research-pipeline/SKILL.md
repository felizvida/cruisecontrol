---
name: research-pipeline
description: "Full research pipeline: Workflow 1 (idea discovery) → implementation → Workflow 2 (auto review loop) → Workflow 3 (paper writing). Goes from a broad research direction to a review-improved paper package in one command. Default route is pure Codex; pure OpenCode is opt-in. Use when user says \"全流程\", \"full pipeline\", \"从找idea到投稿\", \"end-to-end research\", or wants the complete autonomous research lifecycle."
argument-hint: [research-direction]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent, Skill
---

# Full Research Pipeline: Idea → Experiments → Paper

End-to-end autonomous research workflow for: **$ARGUMENTS**

## Overview

This skill chains the entire research lifecycle into a single pipeline:

```
/idea-discovery → implement → /run-experiment → /auto-review-loop → NARRATIVE_REPORT.md → /paper-writing → paper/main.pdf
├── Workflow 1 ──┤            ├────────── Workflow 2 ──────────────┤  ├──────────── Workflow 3 ────────────┤
```

It orchestrates the full research lifecycle, including the narrative handoff into paper generation.

**Route selection:** default to the pure **Codex** route unless the user explicitly requests the pure **OpenCode** route. When this skill invokes sub-skills, pass that route through consistently.

All outputs for this pipeline stay in the current local repository. Do not invent external GitHub repositories, GitHub URLs, or remote destinations for checkpoints, reports, or intermediate artifacts.

## Constants

- **AUTO_PROCEED = true** — Default unattended mode. After presenting a checkpoint, continue with the best supported option unless the user explicitly asked to approve each step.
- **TARGET_VENUE = `ICLR`** — Default paper venue. Override inline, e.g. `/research-pipeline "topic" — venue: NeurIPS`.
- **WORKFLOW_ROUTE = `codex`** — Default route. Override inline with `route: opencode`.
- **REVIEWER_MODE = route-dependent fresh review pass** — Use Codex when `WORKFLOW_ROUTE=codex`; use the configured OpenCode model when `WORKFLOW_ROUTE=opencode`.
- **MAX_RESEARCH_REVIEW_ROUNDS = 4** — Maximum rounds in `/auto-review-loop`.
- **FULLY_AUTOMATIC_PAPER = true** — Continue into `/paper-writing` automatically, allowing placeholder figures when needed instead of stalling.

> Override inline: `/research-pipeline "topic" — wait for my approval at checkpoints, venue: ICML`

## Pipeline

### Stage 1: Idea Discovery (Workflow 1)

Invoke the idea discovery pipeline:

```
/idea-discovery "$ARGUMENTS"
```

This internally runs: `/research-lit` → `/idea-creator` → `/novelty-check` → `/research-review`

**Output:** `IDEA_REPORT.md` with ranked, validated, pilot-tested ideas.

**🚦 Gate 1 — Idea Selection Checkpoint:**

After `IDEA_REPORT.md` is generated, present the top ideas:

```
📋 Idea Discovery complete. Top ideas:

1. [Idea 1 title] — Pilot: POSITIVE (+X%), Novelty: CONFIRMED
2. [Idea 2 title] — Pilot: WEAK POSITIVE (+Y%), Novelty: CONFIRMED
3. [Idea 3 title] — Pilot: NEGATIVE, eliminated

Recommended: Idea 1. Shall I proceed with implementation?
```

The user may:
- **Approve an idea** → proceed to Stage 2.
- **Pick a different idea** → proceed with their choice.
- **Request changes** (e.g., "combine Idea 1 and 3", "focus more on X") → update the idea prompt with user feedback, re-run `/idea-discovery` with refined constraints, and present again.
- **Reject all ideas** → collect feedback on what's missing, re-run Stage 1 with adjusted research direction. Repeat until the user commits to an idea.
- **Stop here** → save current state to `IDEA_REPORT.md` for future reference.

If the user explicitly asked for unattended execution or does not respond and `AUTO_PROCEED=true`, proceed with the top-ranked supported idea after documenting the choice in `IDEA_REPORT.md`. Only block here when the user requested manual approvals.

### Stage 2: Implementation

Once an idea is selected:

1. **Read the idea details** from `IDEA_REPORT.md` (hypothesis, experimental design, pilot code)

2. **Implement the full experiment**:
   - Extend pilot code to full scale (multi-seed, full dataset, proper baselines)
   - Add proper evaluation metrics and logging (wandb if configured)
   - Write clean, reproducible experiment scripts
   - Follow existing codebase conventions

3. **Code review**: Before deploying, do a self-review:
   - Are all hyperparameters configurable via argparse?
   - Is the random seed fixed and controllable?
   - Are results saved to JSON/CSV for later analysis?
   - Is there proper logging for debugging?

### Stage 3: Deploy Experiments (Workflow 2 — Part 1)

Deploy the full-scale experiments:

```
/run-experiment [experiment command]
```

**What this does:**
- Check GPU availability on configured servers
- Sync code to remote server
- Launch experiments in screen sessions with proper CUDA_VISIBLE_DEVICES
- Verify experiments started successfully

**Monitor progress:**

```
/monitor-experiment [server]
```

Wait for experiments to complete. Collect results.

### Stage 4: Auto Review Loop (Workflow 2 — Part 2)

Once initial results are in, start the autonomous improvement loop:

```
/auto-review-loop "$ARGUMENTS — [chosen idea title]"
```

**What this does (up to 4 rounds):**
1. A fresh reviewer-agent pass reviews the work (score, weaknesses, minimum fixes)
2. Claude Code implements fixes (code changes, new experiments, reframing)
3. Deploy fixes, collect new results
4. Re-review → repeat until score ≥ 6/10 or 4 rounds reached

**Output:** `AUTO_REVIEW.md` with full review history and final assessment.

### Stage 5: Narrative Consolidation

After the research loop completes, synthesize a paper-ready narrative handoff.

Write `NARRATIVE_REPORT.md` in the project root using:
- `IDEA_REPORT.md`
- `AUTO_REVIEW.md`
- experiment logs, JSON/CSV outputs, and plots
- final code paths and commands used for the accepted experiments

The report must be honest and structured enough for `/paper-writing` to run without asking for missing story context.

```markdown
# Narrative Report

**Direction**: $ARGUMENTS
**Chosen Idea**: [title]
**Venue Target**: [TARGET_VENUE]
**Status**: submission-ready / draft-with-known-gaps
**Date**: [start] → [end]

## Executive Summary
[2-3 paragraphs describing the problem, method, and current evidence]

## Core Claims
1. [claim]
2. [claim]
3. [claim]

## Claims-Evidence Matrix
| Claim | Evidence | Status | Notes |
|-------|----------|--------|-------|
| ... | ... | supported / partial / weak | ... |

## Experimental Setup
- Datasets:
- Baselines:
- Metrics:
- Compute budget:
- Reproducibility details:

## Main Results
- [quantitative result with exact numbers]
- [quantitative result with exact numbers]

## Reviewer Pressure
- Strongest objection from `AUTO_REVIEW.md`
- What was fixed
- What remains a limitation

## Figure Inventory
- Fig 1: [hero figure description, data source or placeholder plan]
- Fig 2: [main results table/plot]
- Fig 3: [ablation/analysis]

## Paper Framing
- Working title:
- Target venue:
- Paper type: empirical / theory / method
- Related-work buckets:
- Sections likely needed:

## Citations To Verify
- [paper / why cited]

## Remaining Gaps
- [gap 1]
- [gap 2]
```

Rules for this stage:
- Do not overclaim. If the best evidence is weak, say so explicitly in the narrative.
- Convert every surviving claim into claim-evidence form.
- Make figure requirements concrete enough that `/paper-figure` can act.
- If the research loop ended below submission quality, still write the narrative, but mark the status as `draft-with-known-gaps`.

### Stage 6: Paper Writing (Workflow 3)

Once `NARRATIVE_REPORT.md` exists, continue directly into the paper pipeline:

```
/paper-writing "NARRATIVE_REPORT.md — venue: [TARGET_VENUE], auto-proceed, allow placeholder figures"
```

**What this does:**
- Plan the paper structure from the narrative
- Generate real figures/tables from available results
- Create placeholder figures for any still-manual diagrams so the pipeline does not stall
- Write LaTeX sections
- Compile `paper/main.pdf`
- Run the paper improvement loop

**Output:** `paper/` directory containing LaTeX source, intermediate PDFs, `PAPER_IMPROVEMENT_LOG.md`, final `paper/main.pdf`, and `review/` artifacts containing the final review opinion and score.

### Stage 7: Final Summary

After the paper pipeline completes, write a final status report:

```markdown
# Research Pipeline Report

**Direction**: $ARGUMENTS
**Chosen Idea**: [title]
**Venue**: [TARGET_VENUE]
**Date**: [start] → [end]
**Pipeline**: idea-discovery → implement → run-experiment → auto-review-loop → narrative-report → paper-writing

## Journey Summary
- Ideas generated: X → filtered to Y → piloted Z → chose 1
- Implementation: [brief description of what was built]
- Experiments: [number of GPU experiments, total compute time]
- Review rounds: N/4, final score: X/10
- Paper score progression: [round0] → [round1] → [round2]

## Final Status
- [ ] Compiled paper produced
- [ ] Ready for submission / [ ] Draft with known gaps

## Remaining TODOs (if any)
- [manual figure upgrades, missing citations, or unresolved research weaknesses]

## Key Outputs
- IDEA_REPORT.md
- AUTO_REVIEW.md
- NARRATIVE_REPORT.md
- PAPER_PLAN.md
- paper/main.pdf
- paper/PAPER_IMPROVEMENT_LOG.md
- review/REVIEW_OPINION.md
- review/review_scorecard.json
```

## Key Rules

- **Present checkpoints, but auto-continue by default.** Only block if the user explicitly asked for manual approval at each stage.
- **Stages 2-6 should run autonomously** once the idea is chosen. This is the "sleep and wake up to a review-improved paper package" path.
- **If Stage 4 ends at round 4 without positive assessment**, do not loop forever. Write an honest `NARRATIVE_REPORT.md`, then continue into paper-writing with limitations clearly stated.
- **Do not stall on missing manual figures.** Use the paper-writing placeholder path and flag upgrades in the final report.
- **Budget awareness**: Track total GPU-hours across the pipeline. Flag if approaching user-defined limits.
- **Documentation**: Every stage updates its own output file. The full history should be self-contained.
- **Fail gracefully**: If any stage fails (no good ideas, experiments crash, review loop stuck), report clearly and suggest alternatives rather than forcing forward.

## Typical Timeline

| Stage | Duration | Can sleep? |
|-------|----------|------------|
| 1. Idea Discovery | 30-60 min | No (interactive checkpoints) |
| 2. Implementation | 15-60 min | No (may need user input) |
| 3. Deploy | 5 min + experiment time | Yes ✅ |
| 4. Auto Review | 1-4 hours (depends on experiments) | Yes ✅ |
| 5. Narrative Consolidation | 5-15 min | Yes ✅ |
| 6. Paper Writing | 45-90 min | Yes ✅ |

**Sweet spot**: Run Stage 1-2 in the evening, launch Stages 3-6 before bed, wake up to a compiled paper, score-tracked revision history, and final review artifacts.
