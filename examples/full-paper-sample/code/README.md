# Code Package

This example includes the code required to rebuild the paper artifact and regenerate the paper-side assets derived from the synthetic benchmark.

## Included Code

- `../results/render_demo_tables.py`
  Generates the LaTeX tables and placeholder figure snippets from the synthetic benchmark JSON.

- `build_paper.sh`
  Runs the table-generation script, rebuilds dedicated figure assets, and compiles the paper.

- `generate_figure_assets.sh`
  Compiles standalone high-resolution versions of the placeholder figures used in the paper.

- `validate_artifacts.sh`
  Checks the final PDF metadata, LaTeX log cleanliness, and embedded fonts.

## Usage

```bash
cd examples/full-paper-sample/code
./build_paper.sh
./validate_artifacts.sh
```

## Scope Note

This paper is a **synthetic workflow demonstration**, not a real robotics experiment. The executable code in this package therefore covers:

1. synthetic benchmark rendering into paper tables
2. figure asset generation
3. paper compilation and validation

It does not include a real quadruped controller, simulator, or policy-training pipeline because the paper does not claim to have executed one.
