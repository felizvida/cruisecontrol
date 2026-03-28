# JPR Submission Checklist

Use this checklist for an actual `Journal of Proteome Research` submission.

## Core Manuscript Package

- `paper/main.pdf`
- `paper/main.tex`
- bibliography and all figure files
- updated cover letter: `submission/COVER_LETTER_JPR.md`
- style and fit memo: `submission/JPR_20_PAPER_STYLE_MAP.md`

## Data and Code Availability

- public code repository URL
- immutable release or archive URL
- source-data manifest
- figure-generation scripts
- exact local file map for tables used in the manuscript

Recommended final improvement before submission:

- mint an archival release DOI for the current package
- expose a public repository path for code, traceability JSON/CSV, and figure scripts

## Manuscript-Level Checks

- make canonicalization rules explicit in the paper or supplement
- make protein-collapse rules explicit in the paper or supplement
- state intensity preprocessing order plainly
- cite the released Tel2/Teo2 tables and workbook note explicitly
- summarize any available acquisition-order or batch metadata
- keep the acetylation claim framed as suggestive rather than settled

## JPR-Facing Positioning

- article type: `Article`
- primary fit: proteoform-resolved and computational proteomics
- secondary fit: spatially resolved neuroproteomics from public top-down data
- claim style: one clear biological result, bounded by released-data limits

## Recommended Keywords

- `top-down proteomics`
- `proteoforms`
- `zebrafish brain`
- `telencephalon`
- `optic tectum`
- `regional proteomics`
- `spatial proteomics`
- `public data reuse`

## Nice-to-Have Before Submission

- a compact TOC graphic derived from the overlap/marker architecture figure
- a one-page supporting note listing public file locations used in each figure and table
- public-facing readme for code reproduction outside this repo
