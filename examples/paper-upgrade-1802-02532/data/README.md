# Data Package

This example paper is a **document-driven perspective manuscript**, not an empirical benchmark paper.

That means the relevant source data are:

1. the original user-owned source paper and its TeX archive
2. the primary literature used to justify the upgraded framing

There is no synthetic benchmark table, trained model checkpoint, or experiment dataset in this example because the paper does not claim new experimental results.

## Local Source Material

- Original arXiv source archive: [../source/arxiv-source.tar](../source/arxiv-source.tar)
- Original source TeX: [../source/unpacked/main.tex](../source/unpacked/main.tex)
- Original compiled PDF: [../source/unpacked/main.pdf](../source/unpacked/main.pdf)

## Literature Manifest

- Machine-readable manifest: [source_manifest.json](source_manifest.json)

## Rebuild Interpretation

To "run" this paper package, the relevant inputs are the manuscript source, the figure-generation code, and the document corpus listed in `source_manifest.json`.
