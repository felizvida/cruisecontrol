# Code Package

This example now includes the executable code used to build and validate the paper artifact.

## Scope Note

The upgraded manuscript is a **perspective / position paper**. It does **not** present new benchmark experiments, model training runs, or inference pipelines. Accordingly, there is no training code to ship here without fabricating a workflow the paper does not claim.

What is included instead is the full code required to:

1. regenerate the dedicated high-resolution figure asset
2. rebuild the paper PDF from source
3. validate the final PDF and LaTeX build state

## Files

- `build_paper.sh`
  Rebuilds the high-resolution figure assets and then compiles the paper.

- `generate_figure_assets.sh`
  Compiles the standalone figure source and exports vector and raster versions.

- `validate_artifacts.sh`
  Checks the paper PDF, LaTeX log, and embedded fonts.

## Usage

```bash
cd examples/paper-upgrade-1802-02532/code
./build_paper.sh
./validate_artifacts.sh
```
