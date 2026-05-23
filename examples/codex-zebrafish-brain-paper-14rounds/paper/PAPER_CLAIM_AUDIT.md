# Paper Claim Audit

Overall verdict: `PASS`

The current manuscript reports its own numerical evidence faithfully. After one safe correction to the technical-sensitivity table, the remaining paper-to-evidence differences were ordinary rounding rather than mismatched arithmetic or overclaim.

Counts by status:

- `exact_match`: 13
- `rounding_ok`: 8
- `ambiguous_mapping`: 0
- `missing_evidence`: 0
- `config_mismatch`: 0
- `aggregation_mismatch`: 0
- `number_mismatch`: 0
- `scope_overclaim`: 0
- `unsupported_claim`: 0

Safe correction applied before final verdict:

- [sections/3_results.tex](/Users/liux17/codex/autoresearch/examples/codex-zebrafish-brain-paper-14rounds/paper/sections/3_results.tex): the Chao2 lower bounds in Table `tab:technical` were stale relative to the current result files. They were updated from `379.5` / `873.2` to `385.5` / `887.0`.

High-priority checks:

- Article-level aggregate counts `309 / 533 / 35` match the preserved source-study record.
- Exact-ID overlap `29 / 805` and Jaccard `0.0360` match the spreadsheet-derived evidence.
- Prevalence-adjusted and canonicalized overlap results match the current sensitivity files.
- Marker-panel alignment statistics, motor-family stress test, and independent-panel results match the saved permutation outputs.
- PTM totals, acetylation sensitivity models, and duplicate summary values match the current result files.

Conclusion:

The manuscript is numerically trustworthy at the current source snapshot. No unsupported empirical claims remain.
