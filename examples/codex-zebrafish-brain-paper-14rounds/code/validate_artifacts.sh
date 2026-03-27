#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PAPER_DIR="$ROOT/paper"
PDF="$PAPER_DIR/main.pdf"

test -f "$PDF"
test -f "$PAPER_DIR/main_round0_original.pdf"
test -f "$PAPER_DIR/main_round14.pdf"
test -f "$PAPER_DIR/main_round15.pdf"
test -f "$PAPER_DIR/main_round16.pdf"
test -f "$PAPER_DIR/main_round17.pdf"
test -f "$PAPER_DIR/main_round18.pdf"
test -f "$PAPER_DIR/main_round19.pdf"
test -f "$PAPER_DIR/main_round20.pdf"
test -f "$PAPER_DIR/main_round21.pdf"
test -f "$PAPER_DIR/main_round22.pdf"
test -f "$PAPER_DIR/main_round23.pdf"
test -f "$PAPER_DIR/main_round24.pdf"
test -f "$PAPER_DIR/main_round25.pdf"
test -f "$PAPER_DIR/main_round26.pdf"
test -f "$ROOT/review/ROUND_REVIEWS_LIVE.md"
test -f "$ROOT/review/REVIEW_OPINION.md"
test -f "$ROOT/review/review_scorecard.json"
test -f "$ROOT/review/round15_review.md"
test -f "$ROOT/review/round16_review.md"
test -f "$ROOT/review/round17_review.md"
test -f "$ROOT/review/round18_review.md"
test -f "$ROOT/review/round19_review.md"
test -f "$ROOT/review/round20_review.md"
test -f "$ROOT/review/round21_submission_blocked.md"
test -f "$ROOT/figure_assets/region_overview/region_overview.pdf"
test -f "$ROOT/results/summary_metrics.json"
test -f "$ROOT/results/sensitivity_scenarios.csv"
test -f "$ROOT/results/canonicalization_examples.csv"
test -f "$ROOT/results/presence_overlap_significance.csv"
test -f "$ROOT/results/mnar_similarity_sensitivity.csv"
test -f "$ROOT/results/acetylation_covariate_sensitivity.csv"
test -f "$ROOT/results/independent_panel_marker_bias.csv"
test -f "$ROOT/code/environment_versions.json"

echo "== PDF info =="
pdfinfo "$PDF"

echo
echo "== Embedded fonts =="
pdffonts "$PDF"

echo
echo "== Layout warnings =="
grep -n 'Overfull\\|Underfull\\|undefined' "$PAPER_DIR/main.log" || true
