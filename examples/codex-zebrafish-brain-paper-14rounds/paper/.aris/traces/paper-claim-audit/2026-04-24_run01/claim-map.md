# Paper Claim Audit Trace

Date: 2026-04-24
Paper: `examples/codex-zebrafish-brain-paper-14rounds/paper`

This trace records the evidence-to-claim audit for the current zebrafish manuscript.

Safe corrections applied before the final verdict:

- Updated the technical-sensitivity table in `sections/3_results.tex` so the Chao2 lower bounds now match `results/summary_metrics.json` and `results/source_table_metrics.json`:
  - telencephalon: `385.5`
  - optic tectum: `887.0`

Audit coverage:

- article-level overlap counts from `data/curated_evidence.json`
- exact-ID, canonicalized, protein-level, and gene-symbol overlap metrics
- normalization sensitivity ranges
- duplicate-based detectability adjustment
- misidentification ceiling
- curated marker-panel alignment statistics
- independent-panel alignment statistics
- PTM and acetylation sensitivity models
- duplicate technical summary values

Outcome:

- No unsupported numerical claims remained after the table correction.
- Remaining differences between prose and evidence are ordinary rounding.
