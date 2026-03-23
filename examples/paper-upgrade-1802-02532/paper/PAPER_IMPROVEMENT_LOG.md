# Paper Improvement Log

## Score Progression

| Round | Verdict | Key changes |
|-------|---------|-------------|
| Round 0 | Complete first draft | Established the full perspective-paper scaffold and compiled the first end-to-end manuscript |
| Round 1 | Publication framing tightened | Reduced the manuscript from 9 pages to 8, clarified the authorship/presentation framing, and cleaned the figure and bibliography layout |
| Round 2 | Final sample quality | Removed the last table overflow, aligned metadata, and produced the clean final PDF |
| Round 3 | Complete artifact bundle | Added code, source-data manifest, dedicated figure assets, and a scored review, then updated the appendix to point at them |

## Round 0

- Preserved as `main_round0_original.pdf`
- Established:
  - `main.tex`
  - section files
  - bibliography
  - figure/table assets
- Main issues addressed later:
  1. The first draft still looked slightly repo-oriented in presentation.
  2. The taxonomy table and figure needed cleaner layout.
  3. The bibliography URLs made the PDF noisier than necessary.

## Round 1

- Preserved as `main_round1.pdf`
- Changes made:
  1. Switched the tables to ragged-right column layouts.
  2. Simplified the central schematic figure.
  3. Removed inline URL clutter from bibliography entries.
  4. Tightened the front-matter presentation so the manuscript reads more like a paper and less like a generated note.

## Round 2

- Preserved as `main_round2.pdf`
- Also copied to `main.pdf`
- Changes made:
  1. Removed the last table overflow in the taxonomy spread.
  2. Aligned the PDF metadata with the manuscript framing.
  3. Confirmed a clean build with no LaTeX warnings in `main.log`.

## Round 3

- Preserved as `main_round3_complete_package.pdf`
- Changes made:
  1. Added executable scripts for rebuild and validation.
  2. Added a document-corpus data manifest so the paper's source inputs are explicit.
  3. Added dedicated high-resolution figure exports and their standalone source.
  4. Added a detailed scored review and wired the appendix to reference the full package.

## Build Status

- Final PDF: `main.pdf`
- Pages: `9`
- Undefined references/citations: `0`
- Overfull/underfull warnings detected in `main.log`: `0`
- Fonts embedded: yes
