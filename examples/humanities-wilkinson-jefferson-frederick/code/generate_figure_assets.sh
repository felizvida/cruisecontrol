#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

build_asset() {
  local dir="$1"
  local basename="$2"
  local stem="$3"

  cd "${dir}"
  latexmk -pdf -interaction=nonstopmode -halt-on-error "${basename}.tex"

  cp "${basename}.pdf" "${stem}.pdf"
  pdftocairo -svg "${basename}.pdf" "${stem}.svg"
  pdftocairo -png -r 600 "${basename}.pdf" "${stem}"
  latexmk -c "${basename}.tex"
}

build_asset "${ROOT_DIR}/figure_assets/timeline" "timeline_standalone" "timeline"
build_asset "${ROOT_DIR}/figure_assets/network" "network_standalone" "network"
