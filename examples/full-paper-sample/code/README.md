# Code Package

This example includes the code required to run the stochastic simulator, regenerate the paper-side assets, and rebuild the final paper package.

## Included Code

- `../results/simulate_battery_benchmark.py`
  Runs the lightweight stochastic deployment simulator and writes the benchmark JSON plus the episode-level CSV.

- `../results/render_demo_tables.py`
  Generates the LaTeX tables, paper-side figure snippets, and standalone figure sources from the computed benchmark JSON.

- `build_paper.sh`
  Runs the table-generation script, rebuilds dedicated figure assets, and compiles the paper.

- `generate_figure_assets.sh`
  Compiles standalone high-resolution versions of the controller schematic and tradeoff plot used in the paper.

- `validate_artifacts.sh`
  Checks the final PDF metadata, LaTeX log cleanliness, and embedded fonts.

## Usage

```bash
cd examples/full-paper-sample/code
./build_paper.sh
./validate_artifacts.sh
```

## Scope Note

This paper is a **reproducible simulation study**, not a hardware robotics experiment. The executable code in this package therefore covers:

1. stochastic benchmark generation
2. episode-level metric export
3. table and figure generation
4. paper compilation and validation

It does not include a real quadruped controller, a physics-faithful locomotion simulator, or a policy-training pipeline because the paper does not claim to have executed them.
