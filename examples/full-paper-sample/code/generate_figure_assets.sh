#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
FIG_ROOT="${ROOT_DIR}/figure_assets"

build_one() {
  local subdir="$1"
  local base="$2"
  local dir="${FIG_ROOT}/${subdir}"
  cd "${dir}"
  latexmk -pdf -interaction=nonstopmode -halt-on-error "${base}.tex"
  cp "${base}.pdf" "${subdir}.pdf"
  pdftocairo -svg "${base}.pdf" "${subdir}.svg"
  pdftocairo -png -r 600 "${base}.pdf" "${subdir}"
  latexmk -c "${base}.tex"
  echo "Generated figure assets in ${dir}"
}

build_one "controller_placeholder" "controller_placeholder_standalone"
build_one "regime_placeholder" "regime_placeholder_standalone"
