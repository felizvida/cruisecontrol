#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
FIG_DIR="${ROOT_DIR}/figure_assets/serialization_view"
FIG_BASENAME="serialization_view_standalone"

cd "${FIG_DIR}"
latexmk -pdf -interaction=nonstopmode -halt-on-error "${FIG_BASENAME}.tex"

cp "${FIG_BASENAME}.pdf" "serialization_view.pdf"
pdftocairo -svg "${FIG_BASENAME}.pdf" "serialization_view.svg"
pdftocairo -png -r 600 "${FIG_BASENAME}.pdf" "serialization_view"
latexmk -c "${FIG_BASENAME}.tex"

echo "Generated:"
echo "  ${FIG_DIR}/serialization_view.pdf"
echo "  ${FIG_DIR}/${FIG_BASENAME}.pdf"
echo "  ${FIG_DIR}/serialization_view.svg"
echo "  ${FIG_DIR}/serialization_view-1.png"
