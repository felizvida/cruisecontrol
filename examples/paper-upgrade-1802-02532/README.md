# Paper Upgrade Example: arXiv 1802.02532

This folder is a concrete example of the linked-paper upgrade workflow applied to:

- Source paper: [A Spatial Mapping Algorithm with Applications in Deep Learning-Based Structure Classification](https://arxiv.org/abs/1802.02532)
- Ownership mode: `this is my paper`

## Outcome

The workflow does **not** recommend a direct 2026 resubmission of the 2018 empirical paper.

Instead, it takes the `PIVOT + EXECUTABLE PROBE` path:

1. preserve and review the source paper
2. identify why the original experimental framing is now saturated
3. reinterpret the core idea as an early precursor to modern 3D serialization/tokenization
4. add a new deterministic computation-backed probe that tests the paper's central serialization claim
5. generate a new publication-oriented paper with a distinct contribution

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
- [paper/main_round4_computation_backed.pdf](paper/main_round4_computation_backed.pdf)
- [paper/PAPER_IMPROVEMENT_LOG.md](paper/PAPER_IMPROVEMENT_LOG.md)
- [code/README.md](code/README.md)
- [data/README.md](data/README.md)
- [results/serialization_probe.json](results/serialization_probe.json)
- [results/ordering_summary.csv](results/ordering_summary.csv)
- [data/synthetic_microenvironment_corpus.jsonl](data/synthetic_microenvironment_corpus.jsonl)
- [figure_assets/README.md](figure_assets/README.md)
- [review/REVIEW_OPINION.md](review/REVIEW_OPINION.md)

## Source Archive

The original arXiv source was downloaded to:

- [source/arxiv-source.tar](source/arxiv-source.tar)
- [source/unpacked/main.tex](source/unpacked/main.tex)
- [source/unpacked/main.pdf](source/unpacked/main.pdf)

## What Changed

The upgraded paper is not a facelift of the 2018 manuscript.

It becomes a new computation-backed interface paper:

- old paper: Hilbert-curve mapping as an alternative to volumetric 3D CNNs
- new paper: serialization as a first-class interface between irregular 3D structures and modern sequence-native models, especially for biomolecular AI
- new executable evidence: a deterministic context-budget probe comparing Hilbert, Morton, raster, and random orderings on synthetic channel-rich microenvironments

That pivot is the most credible publication path available here without fabricating a modern biomolecular benchmark.

## Final Status

The example now ends in a completed paper artifact:

- paper type: hybrid literature-synthesis / executable-interface paper
- final output: [paper/main.pdf](paper/main.pdf)
- build status: clean LaTeX build, 11 pages, fonts embedded

## Completeness Package

This example now includes the additional pieces needed for a more complete publication bundle:

- executable probe, figure-generation, build, and validation code in [code/](code/) and [results/](results/)
- a source-paper archive plus generated sample corpus and manifest in [data/](data/)
- dedicated high-resolution figure exports in [figure_assets/](figure_assets/)
- a detailed scored review in [review/](review/)

Because the final paper is still an honest scoped example, there is no claim of a real biomolecular benchmark, training run, or SOTA method. The shipped computation instead covers a deterministic synthetic serialization probe that generates the figures, tables, and core quantitative claims used in the manuscript.
