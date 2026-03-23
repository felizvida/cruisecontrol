# Paper Improvement Log

## Score Progression

| Round | Score | Verdict | Key changes |
|-------|------:|---------|-------------|
| Round 0 | 5.9/10 | Not ready | First compiled sample paper after fixing the synthetic-results tables |
| Round 1 | 6.8/10 | Almost | Clarified the low-battery crossover and added an average-effect summary |
| Round 2 | 7.3/10 | Good demo sample | Tightened the limitations and conclusion so the scope matches the synthetic benchmark |
| Round 3 | 7.4/10 | Complete package | Added code, data manifest, figure assets, and a scored review bundle |

## Round 0

- Preserved as `main_round0_original.pdf`
- Establishes the complete paper tree:
  - `main.tex`
  - section files
  - bibliography
  - generated tables and placeholder figures

Main issues addressed later:

1. The paper needed a clearer summary of the low-battery average effect.
2. The scope note needed to be even sharper about synthetic evidence versus workflow demonstration.

## Round 1

- Preserved as `main_round1.pdf`
- Changes made:
  1. Added an average low-battery return gain to the abstract.
  2. Added an average low-battery compute-energy reduction to the results section.

Why this mattered:

- The first draft had the right per-regime numbers, but the main pattern was still more scattered than it needed to be.
- The round-1 edits made the crossover legible at a glance.

## Round 2

- Preserved as `main_round2.pdf`
- Also copied to `main.pdf`
- Changes made:
  1. Tightened the discussion so the result is framed as a scheduling variable, not a new universal default.
  2. Added a stronger limitations sentence that explicitly says the paper is a workflow artifact with a plausible hypothesis.
  3. Added an appendix build command so the sample is easier to rebuild locally.

## Round 3

- Preserved as `main_round3_complete_package.pdf`
- Changes made:
  1. Added rebuild and validation scripts.
  2. Added a data manifest tied to the synthetic benchmark JSON.
  3. Added dedicated high-resolution exports for the placeholder figures.
  4. Added a scored review packet and updated the appendix to reference the full bundle.

## Build Status

- Final PDF: `main.pdf`
- Pages: `7`
- Undefined references/citations: `0`
- Overfull/underfull warnings detected in `main.log`: `0`
- Fonts embedded: yes
