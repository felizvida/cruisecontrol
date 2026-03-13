# Project Research Context

Fill the sections that apply to your project. The migrated skills read this file when they need server metadata, local paper-library paths, or paper-writing defaults.

## Paper Library

- Local PDFs: `/absolute/path/to/papers`
- Secondary PDFs: `/absolute/path/to/literature`
- Notes: use this section for any nonstandard collection layout

## Remote Server

- SSH: `ssh your-gpu-server`
- GPU: `4x A100 80GB`
- Conda: `eval "$(/opt/conda/bin/conda shell.bash hook)" && conda activate research`
- Code dir: `/home/you/research-project`
- Launch style: `screen`
- Notes: any quota, queue, or filesystem constraints

## Local Environment

- Hardware: `Linux CUDA` or `macOS MPS`
- Conda env: `research`
- Python: `3.11`
- Default launch command: `python train.py`

## Paper Defaults

- Venue: `ICLR`
- Anonymous: `true`
- Main body page limit: `9`
- Bibliography source: `refs/full.bib`

## Experiment Defaults

- Max pilot budget per idea: `2 GPU-hours`
- Max total pilot budget: `8 GPU-hours`
- Preferred metrics: `accuracy, calibration, latency`

## Notes

- Add any project-specific constraints the skills should respect.
