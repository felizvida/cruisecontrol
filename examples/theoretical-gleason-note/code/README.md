# Code Package

This example includes the code required to generate the numeric sanity checks, rebuild the paper assets, compile the paper, and validate the final PDF.

## Included Code

- `../results/run_theorem_checks.py`
  Generates random matrix sanity checks for the theorem package and writes JSON plus CSV summaries.

- `../results/render_assets.py`
  Turns the generated results into paper-side tables and standalone figure sources.

- `build_paper.sh`
  Runs the result-generation scripts, regenerates the figure assets, and compiles the paper.

- `generate_figure_assets.sh`
  Compiles the standalone figure sources and exports vector and raster versions.

- `validate_artifacts.sh`
  Checks the paper PDF, LaTeX log cleanliness, and embedded fonts.

## Usage

```bash
cd examples/theoretical-gleason-note/code
./build_paper.sh
./validate_artifacts.sh
```

## Scope Note

The theorem is proved on paper. The shipped computation is there to generate real reproducible artifacts:

1. random reconstruction checks
2. validation residual summaries
3. table and figure assets
4. paper compilation and validation
