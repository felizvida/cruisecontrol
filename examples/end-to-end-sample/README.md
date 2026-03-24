# End-to-End Sample

This folder is a tracked sample artifact set for the repo's early-stage **Workflow 1**:

```text
research-lit -> idea-creator -> novelty-check -> research-review
```

## Topic

**Test-time adaptation for battery-constrained quadruped robots**

## Included

- [01_literature_review.md](01_literature_review.md)
- [02_idea_report.md](02_idea_report.md)
- [03_novelty_check.md](03_novelty_check.md)
- [04_research_review.md](04_research_review.md)

## What This Shows

This is the shape of the first leg of a concrete auto-research pass in this repo:

1. map the literature
2. generate and rank ideas
3. pressure-test novelty
4. get a hard review before implementation

## What It Does Not Show

- no GPU experiments were run
- no target research codebase was modified
- no `run-experiment`, `auto-review-loop`, or `research-pipeline` stage was executed

Those later stages need a real research project with a filled `AGENTS.md`.

In the fully automatic path, a complete `/research-pipeline` run should continue on to:

- `AUTO_REVIEW.md`
- `NARRATIVE_REPORT.md`
- `PAPER_PLAN.md`
- `paper/main.pdf`
- `paper/PAPER_IMPROVEMENT_LOG.md`
- `review/REVIEW_OPINION.md`
- `review/review_scorecard.json`

For a tracked sample that includes those downstream artifacts and a complete paper package, see [../full-paper-sample/README.md](../full-paper-sample/README.md).
