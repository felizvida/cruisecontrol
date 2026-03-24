---
name: paper-upgrade
description: "Upgrade a linked paper into a publication-grade new manuscript. Use when the user provides a paper URL and wants a full automatic reboot: analyze the source paper, find a real novelty gap, design a stronger contribution, write a polished new paper, and document the improvements."
argument-hint: [paper-url-and-ownership-note]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent, Skill, mcp__codex__codex, mcp__codex__codex-reply
---

# Paper Upgrade: Linked Paper → Stronger Publication

Turn a linked paper into a stronger, polished new manuscript for: **$ARGUMENTS**

## Overview

This workflow is for cases where the user brings a paper URL and wants a full publication-oriented upgrade:

```
paper link → source-paper review → literature gap scan → breakthrough gate
→ upgrade plan → narrative report → /paper-writing → paper/main.pdf
                               └→ improvement log / final review opinion / scorecard / diff report
```

The workflow must aim for a real contribution increase, not a cosmetic rewrite.

All outputs stay in the current local repository. Never invent external GitHub repositories, URLs, or remote destinations for artifacts.

## Required Inputs

The user should provide:

1. **A paper URL** — landing page or direct PDF link
2. **Ownership mode** — one of:
   - `this is my paper`
   - `I have permission to revise it`
   - `treat this as inspiration only`

If the URL is missing, stop and ask for it.
If ownership is unclear, ask before proceeding.

## Hard Guardrails

- **No cosmetic-only rewrites.** If the upgrade path is only wording, formatting, or citation cleanup, stop and write `NO_PUBLICATION_UPGRADE.md`.
- **No fabrication.** Do not invent experiments, datasets, theorem proofs, or benchmark results.
- **Respect authorship.**
  - If it is the user's paper or they have permission, direct revision is allowed.
  - If it is not their paper, do **not** produce a near-copy. Instead, produce a clearly new manuscript that cites the source paper and adds a distinct contribution.
- **Do not reuse source figures, tables, or close structural copies** unless the user owns the paper or explicitly has permission to revise it.
- **Do not mirror the full source text into repo outputs.** Use the linked paper for analysis, but persist summaries, notes, and derived reports rather than verbatim extraction dumps.

## Constants

- **AUTO_PROCEED = true** — Continue automatically unless the user explicitly asks to review each stage.
- **REVIEWER_MODEL = `gpt-5.4`** — Reviewer used through the `codex` MCP server.
- **TARGET_VENUE = `ICLR`** — Default venue. Override inline if needed.
- **MIN_PUBLICATION_DELTA = 1** — At least one non-cosmetic contribution upgrade is required.

Valid publication-grade deltas include:
- a new experiment regime or benchmark
- a stronger ablation or failure analysis that changes the claim set
- a new theorem, proposition, or formal analysis
- a broader unifying framing with evidence the source paper did not include
- a systems/deployment law or insight that changes the practical conclusion

## Workflow

### Stage 0: Intake and Rights Check

Parse the argument and normalize it into:

```markdown
# Paper Upgrade Intake

- Source URL:
- Ownership mode:
- Target venue:
- User constraints:
```

If ownership mode is `treat this as inspiration only`, the deliverable must be a new paper inspired by the linked work, not a lightly rewritten derivative.

### Stage 1: Read the Source Paper

Fetch the paper landing page and, if possible, the PDF.

Use the paper for analysis, then write a local summary:

`SOURCE_PAPER_NOTES.md`

It must include:
- title
- citation
- problem statement
- main claims
- methodology summary
- evidence and experiments
- stated limitations
- what feels strongest
- what feels weakest

Do **not** paste long verbatim sections from the source paper.

### Stage 2: External Review of the Source

Run a brutal external review focused on publication lift:

```
/research-review "[source paper summary + target venue + ask for publication-grade upgrade paths]"
```

Save the result as:

`SOURCE_PAPER_REVIEW.md`

The review must answer:
- what prevents acceptance today
- what missing evidence/theory would most increase acceptance odds
- whether the source paper is under-claimed or over-claimed
- the smallest credible breakthrough that would make a new paper worthwhile

### Stage 3: Literature Update and Novelty Gap Scan

Search for work published after or around the source paper, using primary sources where possible.

Write:

`PRIOR_ART_UPDATE.md`

It must identify:
- new papers the source did not address
- places where the source is already saturated by later work
- the remaining open gap
- the most defensible novelty path from today's standpoint

### Stage 4: Breakthrough Gate

Before writing anything polished, decide whether a real publication-grade upgrade exists.

Write:

`PUBLICATION_DECISION.md`

Allowed outcomes:

1. **PROCEED** — a real upgrade path exists
2. **PIVOT** — the source paper is too saturated, but a related new contribution path exists
3. **STOP** — no credible non-cosmetic upgrade found

If the outcome is `STOP`, also write:

`NO_PUBLICATION_UPGRADE.md`

and end the workflow.

### Stage 5: Upgrade Plan

If the gate passes, write:

`BREAKTHROUGH_PLAN.md`

This is the backbone of the new paper. It must include:
- new title direction
- upgraded central claim
- what is genuinely new relative to the source
- required evidence for each new claim
- what to delete from the original claim set
- figure/table plan
- risk register

The plan must explicitly answer:

```markdown
## Why this is not just a facelift
- New contribution:
- New evidence/theory:
- What changed in the acceptance story:
```

### Stage 6: Improvement Diff

Write:

`IMPROVEMENT_DIFF.md`

This is the user-facing change log from source paper to upgraded paper:
- framing changes
- claim changes
- method changes
- evidence changes
- figure/table changes
- limitations kept or added

This document should read like an editor's memo, not a git diff.

### Stage 7: Narrative Handoff

Write:

`NARRATIVE_REPORT.md`

It must contain the upgraded paper story, including:
- source paper context
- new contribution
- claims-evidence matrix
- exact outputs or evidence available
- planned figures and tables
- limitations
- attribution note if the source paper was not the user's own

If the workflow is operating without new experimental evidence, the narrative must be honest about that and either:
- pivot to a theory/position/survey-style paper with a legitimate new angle, or
- stop before paper-writing if the paper would otherwise rely on fabricated results

### Stage 8: Write the New Paper

Continue into the writing workflow:

```
/paper-writing "NARRATIVE_REPORT.md — venue: [TARGET_VENUE], auto-proceed, allow placeholder figures"
```

Expected outputs:
- `PAPER_PLAN.md`
- `paper/main.pdf`
- `paper/PAPER_IMPROVEMENT_LOG.md`
- `review/REVIEW_OPINION.md`
- `review/review_scorecard.json`

### Stage 9: Final Upgrade Report

Write:

`UPGRADE_SUMMARY.md`

It must include:
- source URL
- ownership mode
- publication decision
- breakthrough thesis
- final paper path
- top improvements over the source
- remaining risks before submission

## Final Deliverables

A successful run should leave:

- `SOURCE_PAPER_NOTES.md`
- `SOURCE_PAPER_REVIEW.md`
- `PRIOR_ART_UPDATE.md`
- `PUBLICATION_DECISION.md`
- `BREAKTHROUGH_PLAN.md`
- `IMPROVEMENT_DIFF.md`
- `NARRATIVE_REPORT.md`
- `UPGRADE_SUMMARY.md`
- `paper/main.pdf`
- `paper/PAPER_IMPROVEMENT_LOG.md`
- `review/REVIEW_OPINION.md`
- `review/review_scorecard.json`

## Key Rules

- The source paper is an input, not a license to copy.
- A publication-grade upgrade must change the claim-evidence story, not only the prose.
- If the only available changes are editorial, stop instead of pretending there is novelty.
- If the user does not own the source paper, produce a clearly new manuscript with explicit citation and attribution.
- Never carry over the source paper's figures, tables, or section structure closely enough that the new paper reads like a disguised copy.
- Prefer a narrow, defensible new contribution over a broad but weak rewrite.
