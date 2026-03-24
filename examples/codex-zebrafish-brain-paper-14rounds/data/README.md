# Data Package

This example is a computation-backed re-analysis of published zebrafish brain proteomics.

## Included files

- `source_manifest.json`
  Bibliographic metadata and URLs for the source literature used in the paper.

- `curated_evidence.json`
  The machine-readable extraction used for the computation:
  - region-level proteoform totals
  - protein-level overlap
  - per-marker proteoform counts discussed in the source paper
  - technical replicate summary values reported in the article
  - post-translational modification totals

## Provenance note

The quantitative core comes from the 2022 LCM-CZE-MS/MS zebrafish brain paper and its repository metadata. This example does not pretend to reprocess the raw mass spectrometry files. It computes from values explicitly recoverable from the published article and linked dataset metadata, then derives additional statistical and visualization outputs locally.

