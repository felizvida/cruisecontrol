# Code Package

This example now includes the executable code used to generate the probe results, rebuild the figures, compile the paper, and validate the artifact package.

## Scope Note

The upgraded manuscript is a **hybrid interface paper**. It does **not** present a real biomolecular benchmark, model training run, or inference pipeline. Accordingly, there is no training code to ship here without fabricating a workflow the paper does not claim.

What is included instead is the full code required to:

1. generate a deterministic synthetic serialization probe
2. emit the benchmark JSON, CSV summaries, and sample corpus
3. regenerate the dedicated high-resolution figure assets
4. rebuild the paper PDF from source
5. validate the final PDF and LaTeX build state

## Files

- `build_paper.sh`
  Runs the probe, regenerates the high-resolution figure assets, and then compiles the paper.

- `../results/run_serialization_probe.py`
  Generates the deterministic synthetic corpus plus the computed locality and context-budget metrics used in the paper.

- `../results/render_probe_assets.py`
  Converts the computed metrics into LaTeX tables, paper-side figure snippets, and standalone figure sources.

- `generate_figure_assets.sh`
  Compiles the standalone figure sources and exports vector and raster versions.

- `validate_artifacts.sh`
  Checks the paper PDF, LaTeX log, and embedded fonts.

## Usage

```bash
cd examples/paper-upgrade-1802-02532/code
./build_paper.sh
./validate_artifacts.sh
```
