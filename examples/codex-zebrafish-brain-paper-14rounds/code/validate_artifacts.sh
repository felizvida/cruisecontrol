#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PAPER_DIR="$ROOT/paper"
PDF="$PAPER_DIR/main.pdf"

test -f "$PDF"
test -f "$PAPER_DIR/main_round0_original.pdf"
test -f "$PAPER_DIR/main_round14.pdf"
test -f "$ROOT/review/ROUND_REVIEWS_LIVE.md"
test -f "$ROOT/review/REVIEW_OPINION.md"
test -f "$ROOT/review/review_scorecard.json"
test -f "$ROOT/figure_assets/region_overview/region_overview.pdf"
test -f "$ROOT/results/summary_metrics.json"

echo "== PDF info =="
pdfinfo "$PDF"

echo
echo "== Embedded fonts =="
pdffonts "$PDF"

echo
echo "== Layout warnings =="
grep -n 'Overfull\\|Underfull\\|undefined' "$PAPER_DIR/main.log" || true

