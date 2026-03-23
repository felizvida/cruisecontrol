#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

python3 "${ROOT_DIR}/results/run_theorem_checks.py"
python3 "${ROOT_DIR}/results/render_assets.py"
bash "${SCRIPT_DIR}/generate_figure_assets.sh"

cd "${ROOT_DIR}/paper"
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

echo "Built ${ROOT_DIR}/paper/main.pdf"
