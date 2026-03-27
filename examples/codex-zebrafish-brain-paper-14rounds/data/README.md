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

- `evidence_traceability.json`
  Machine-readable links from the evidence fields in `curated_evidence.json` and the exact-ID overlap outputs back to the source paper and released tables.

- `source_tables/Proteoform_ID_Tel2.xlsx`
- `source_tables/proteoform_ID_Teo2.xlsx`
  Released PRIDE region tables used for exact-ID overlap, canonicalized-overlap diagnostics, duplicate-incidence sensitivity, marker-family membership, abundance-normalization checks, composition guardrails, and intensity-weighted follow-up analyses.

- `source_tables/supporting_information.xlsx`
  The journal supplementary workbook. Its `note` sheet states that the released proteoforms were identified with `1%` proteoform-spectrum-match FDR and `5%` proteoform-level FDR in TopPIC, and that duplicate label-free quantification was performed with TopDiff. Its `Tel2` and `Teo2` sheets match the standalone PRIDE XLSX tables exactly.

## Provenance note

The quantitative core comes from the 2022 LCM-CZE-MS/MS zebrafish brain paper, its journal supplement, and the released region tables in PRIDE. The PRIDE/OmicsDI landing page also lists the four raw duplicate files `Tel2_1.raw`, `Tel2_2.raw`, `Teo2_1.raw`, and `Teo2_2.raw`; we record those links in `source_manifest.json` for provenance, but this example does not pretend to reprocess them. It computes from values explicitly recoverable from the published article, the supplementary note sheet, and the public Tel2/Teo2 tables, then derives additional statistical and visualization outputs locally.
