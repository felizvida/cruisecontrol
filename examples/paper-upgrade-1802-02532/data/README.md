# Data Package

This example paper is a **computation-backed interface paper**, not a full biomolecular benchmark paper.

That means the relevant source data are:

1. the original user-owned source paper and its TeX archive
2. the primary literature used to justify the upgraded framing
3. the deterministic synthetic microenvironment corpus used for the executable serialization probe

## Local Source Material

- Original arXiv source archive: [../source/arxiv-source.tar](../source/arxiv-source.tar)
- Original source TeX: [../source/unpacked/main.tex](../source/unpacked/main.tex)
- Original compiled PDF: [../source/unpacked/main.pdf](../source/unpacked/main.pdf)

## Literature Manifest

- Machine-readable manifest: [source_manifest.json](source_manifest.json)
- Generated sample corpus: [synthetic_microenvironment_corpus.jsonl](synthetic_microenvironment_corpus.jsonl)

## Rebuild Interpretation

To "run" this paper package, the relevant inputs are the manuscript source, the probe-generation code, the generated sample corpus, and the document corpus listed in `source_manifest.json`.
