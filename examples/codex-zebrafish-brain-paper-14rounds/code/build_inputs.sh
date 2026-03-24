#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

mkdir -p .cache
export XDG_CACHE_HOME="$ROOT/.cache"

python3 results/analyze_region_proteome.py
/usr/local/bin/Rscript results/render_figures.R
