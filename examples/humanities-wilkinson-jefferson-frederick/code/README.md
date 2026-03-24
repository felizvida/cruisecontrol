# Code Package

This humanities example ships executable analysis code even though the argument is historical rather than experimental.

## Included Code

- `../results/analyze_case.py`
  Loads the curated source corpus, computes theme counts, source counts, weighted network edges, and timeline outputs.

- `../results/render_assets.py`
  Turns the computed outputs into paper-side tables and TikZ figures, including the evidence-ladder table, plus standalone figure sources for the asset folder.

- `build_paper.sh`
  Runs the analysis, renders the assets, builds standalone figures, and compiles the paper.

- `generate_figure_assets.sh`
  Exports the standalone figure PDFs, SVGs, and 600 DPI PNGs.

- `validate_artifacts.sh`
  Checks the paper PDF, LaTeX log, and embedded fonts.

## Usage

```bash
cd examples/humanities-wilkinson-jefferson-frederick/code
./build_paper.sh
./validate_artifacts.sh
```

## Scope Note

The code does not "prove" the historical argument on its own. It makes the source coding, theme counts, network drawing, and paper figures reproducible.
