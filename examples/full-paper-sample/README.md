# Full Paper Sample

This folder is a tracked, end-to-end sample artifact set for the repo's intended fully automatic path:

```text
research-lit -> idea-creator -> novelty-check -> research-review
-> auto-review-loop -> narrative report -> paper plan -> paper writing -> compiled PDF
```

## Topic

**Battery-gated forward-only adaptation for battery-constrained quadruped robots**

## Important Note

This sample is now a real computation-backed simulation study, not just a hand-authored workflow demo.

- The first four markdown files are copied from the earlier idea-stage sample.
- The downstream artifacts continue that idea with a lightweight stochastic deployment simulator implemented in [results/simulate_battery_benchmark.py](results/simulate_battery_benchmark.py).
- The final paper is still not a hardware-validated robotics result. It is a reproducible simulation study whose evidence is generated locally from code and episode-level runs.

## Included

- [01_literature_review.md](01_literature_review.md)
- [02_idea_report.md](02_idea_report.md)
- [03_novelty_check.md](03_novelty_check.md)
- [04_research_review.md](04_research_review.md)
- [05_auto_review.md](05_auto_review.md)
- [06_narrative_report.md](06_narrative_report.md)
- [07_paper_plan.md](07_paper_plan.md)
- [results/simulate_battery_benchmark.py](results/simulate_battery_benchmark.py)
- [results/demo_benchmark.json](results/demo_benchmark.json)
- [results/episode_metrics.csv](results/episode_metrics.csv)
- [results/render_demo_tables.py](results/render_demo_tables.py)
- [paper/main.pdf](paper/main.pdf)
- [paper/main_round0_original.pdf](paper/main_round0_original.pdf)
- [paper/main_round1.pdf](paper/main_round1.pdf)
- [paper/main_round2.pdf](paper/main_round2.pdf)
- [paper/main_round3_complete_package.pdf](paper/main_round3_complete_package.pdf)
- [paper/main_round4_simulation_package.pdf](paper/main_round4_simulation_package.pdf)
- [paper/PAPER_IMPROVEMENT_LOG.md](paper/PAPER_IMPROVEMENT_LOG.md)
- [code/README.md](code/README.md)
- [data/README.md](data/README.md)
- [figure_assets/README.md](figure_assets/README.md)
- [review/REVIEW_OPINION.md](review/REVIEW_OPINION.md)
- [review/review_scorecard.json](review/review_scorecard.json)

## What This Shows

This is the repo’s intended end state:

1. early-stage research artifacts
2. a reviewer-driven refinement pass
3. a narrative handoff
4. a paper outline
5. executable simulation code and generated benchmark outputs
6. LaTeX source and a compiled PDF
7. a complete-paper package with code, data manifest, figure assets, and review

## What This Does Not Show

- no real quadruped codebase was modified
- no real robot benchmark was executed
- no claim of hardware transfer is made

The value of this folder is that it now demonstrates both the artifact shape of a complete run and the minimum amount of real coding and computation needed to back the final paper with executable evidence.

## Completeness Package

This example now also includes:

- rebuild and validation scripts in [code/](code/)
- simulation-data documentation in [data/](data/)
- dedicated high-resolution figure exports in [figure_assets/](figure_assets/)
- a detailed scored review in [review/](review/)

## Provenance Note

The early markdown artifacts still preserve the original pre-simulation workflow narrative. The simulator-backed paper and review documents are the authoritative end state for this folder.
