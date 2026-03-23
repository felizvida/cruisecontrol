# Paper Upgrade Example: arXiv 1802.02532

This folder is a concrete example of the linked-paper upgrade workflow applied to:

- Source paper: [A Spatial Mapping Algorithm with Applications in Deep Learning-Based Structure Classification](https://arxiv.org/abs/1802.02532)
- Ownership mode: `this is my paper`

## Outcome

The workflow does **not** recommend a direct 2026 resubmission of the 2018 empirical paper.

Instead, it takes the `PIVOT` path:

1. preserve and review the source paper
2. identify why the original experimental framing is now saturated
3. reinterpret the core idea as an early precursor to modern 3D serialization/tokenization
4. generate a new publication-oriented perspective paper with a distinct contribution

## Key Artifacts

- [SOURCE_PAPER_NOTES.md](SOURCE_PAPER_NOTES.md)
- [SOURCE_PAPER_REVIEW.md](SOURCE_PAPER_REVIEW.md)
- [PRIOR_ART_UPDATE.md](PRIOR_ART_UPDATE.md)
- [PUBLICATION_DECISION.md](PUBLICATION_DECISION.md)
- [BREAKTHROUGH_PLAN.md](BREAKTHROUGH_PLAN.md)
- [IMPROVEMENT_DIFF.md](IMPROVEMENT_DIFF.md)
- [NARRATIVE_REPORT.md](NARRATIVE_REPORT.md)
- [UPGRADE_SUMMARY.md](UPGRADE_SUMMARY.md)
- [paper/main.pdf](paper/main.pdf)
- [paper/main_round0_original.pdf](paper/main_round0_original.pdf)
- [paper/main_round1.pdf](paper/main_round1.pdf)
- [paper/main_round2.pdf](paper/main_round2.pdf)
- [paper/main_round3_complete_package.pdf](paper/main_round3_complete_package.pdf)
- [paper/PAPER_IMPROVEMENT_LOG.md](paper/PAPER_IMPROVEMENT_LOG.md)
- [code/README.md](code/README.md)
- [data/README.md](data/README.md)
- [figure_assets/README.md](figure_assets/README.md)
- [review/REVIEW_OPINION.md](review/REVIEW_OPINION.md)

## Source Archive

The original arXiv source was downloaded to:

- [source/arxiv-source.tar](source/arxiv-source.tar)
- [source/unpacked/main.tex](source/unpacked/main.tex)
- [source/unpacked/main.pdf](source/unpacked/main.pdf)

## What Changed

The upgraded paper is not a facelift of the 2018 manuscript.

It becomes a new perspective paper:

- old paper: Hilbert-curve mapping as an alternative to volumetric 3D CNNs
- new paper: serialization as a first-class interface between irregular 3D structures and modern sequence-native models, especially for biomolecular AI

That pivot is the only credible publication path available here without inventing new experiments.

## Final Status

The example now ends in a completed paper artifact:

- paper type: perspective / position paper
- final output: [paper/main.pdf](paper/main.pdf)
- build status: clean LaTeX build, 9 pages, fonts embedded

## Completeness Package

This example now includes the additional pieces needed for a more complete publication bundle:

- executable build and validation code in [code/](code/)
- a source-data and literature manifest in [data/](data/)
- dedicated high-resolution figure exports in [figure_assets/](figure_assets/)
- a detailed scored review in [review/](review/)

Because the final paper is a perspective manuscript, there is no training pipeline or benchmark dataset in this example. The shipped code and data package therefore cover manuscript building, figure generation, and the document corpus used to justify the paper.
