# Code Package

This example uses a small local computation stack:

- `../results/analyze_region_proteome.py`
  Computes overlap, specialization, marker-bias, axis-alignment, exact-test, robustness, PTM, and technical-replicate summaries.

- `../results/render_figures.R`
  Generates publication-ready PDF, SVG, and 600 DPI PNG figure assets.

- `build_inputs.sh`
  Rebuilds the analysis outputs and figures.

- `build_paper.sh`
  Rebuilds the analysis outputs and recompiles the paper.

- `validate_artifacts.sh`
  Checks the final paper package, saved review chain, figure assets, and PDF metadata.
