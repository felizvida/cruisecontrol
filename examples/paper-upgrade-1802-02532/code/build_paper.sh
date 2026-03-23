#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
PAPER_DIR="${ROOT_DIR}/paper"

"${SCRIPT_DIR}/generate_figure_assets.sh"

cd "${PAPER_DIR}"
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

echo "Built ${PAPER_DIR}/main.pdf"
