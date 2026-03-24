#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

"$ROOT/code/build_inputs.sh"

cd "$ROOT/paper"
latexmk -C
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

