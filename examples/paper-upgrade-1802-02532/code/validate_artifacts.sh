#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
PAPER_DIR="${ROOT_DIR}/paper"

cd "${PAPER_DIR}"

echo "== pdfinfo =="
pdfinfo main.pdf | sed -n '1,24p'

echo
echo "== log warnings =="
if rg -n "Overfull|Underfull|undefined|Warning" main.log; then
  echo "Warnings detected above."
else
  echo "No LaTeX warnings detected."
fi

echo
echo "== fonts =="
pdffonts main.pdf
