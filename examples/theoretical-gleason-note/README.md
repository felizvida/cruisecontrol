# Theoretical Example: A No-Physics Gleason-Type Note

This folder is a concrete theoretical-paper example for the repo.

It does **not** claim a new elementary proof of Gleason's original 1957 theorem.
Instead, it packages a simpler and fully defensible target:

1. a high-school-friendly warmup theorem about bounded functions on `[0,1]`
2. a sphere corollary that turns that warmup into an elementary "shadow-length" rule
3. a short proof of a **finite-dimensional real Gleason-type theorem** on effect matrices
4. computation-backed sanity checks and reproducible figure assets

## Final Paper

- [paper/main.pdf](paper/main.pdf)
- [paper/main_round0_original.pdf](paper/main_round0_original.pdf)
- [paper/main_round1.pdf](paper/main_round1.pdf)
- [paper/main_round2.pdf](paper/main_round2.pdf)
- [paper/main_round3.pdf](paper/main_round3.pdf)
- [paper/main_round4.pdf](paper/main_round4.pdf)
- [paper/main_round1_complete_package.pdf](paper/main_round1_complete_package.pdf)
- [paper/PAPER_IMPROVEMENT_LOG.md](paper/PAPER_IMPROVEMENT_LOG.md)

## Key Supporting Files

- [NARRATIVE_REPORT.md](NARRATIVE_REPORT.md)
- [HIGH_SCHOOL_EXPLANATION.md](HIGH_SCHOOL_EXPLANATION.md)
- [code/README.md](code/README.md)
- [data/README.md](data/README.md)
- [results/reconstruction_checks.json](results/reconstruction_checks.json)
- [results/check_summary.csv](results/check_summary.csv)
- [review/REVIEW_OPINION.md](review/REVIEW_OPINION.md)
- [review/review_scorecard.json](review/review_scorecard.json)

## What The Paper Honestly Claims

The paper proves the following theorem in plain real-matrix language:

> If `f` assigns a number in `[0,1]` to every real symmetric matrix `E` with `0 <= E <= I`,
> if `f(I)=1`,
> and if `f(E+F)=f(E)+f(F)` whenever `E`, `F`, and `E+F` all stay in the same effect space,
> then `f(E)=tr(rho E)` for a unique positive semidefinite trace-one matrix `rho`.

This is a **Gleason-type theorem**, not Gleason's original theorem. The assumption is stronger because additivity is required on the full effect space rather than only on orthogonal projections.

## Why This Example Matters

The value of this example is methodological:

- the main proof avoids physics vocabulary
- the warmup section is explainable to a strong high school student
- the theorem package is complete and reproducible
- the computations generate real numeric checks rather than hand-written claims

## High-School-Level Picture

The proof begins with a very simple idea:

- if a bounded rule on numbers satisfies `rule(x+y)=rule(x)+rule(y)`, then it has no room to bend and must be a straight line
- if three squared lengths always add to `1`, then any bounded rule on those triples must be an affine rule in the squared length
- once the same rigidity is applied to matrices, the only possible additive rule is a trace rule `tr(rho E)`

So the paper's strategy is not "start with quantum mechanics and simplify later." It is "start with fractions and boundedness, then climb one clean step at a time."

## Completeness Package

This example includes:

- the finished paper PDF and LaTeX source
- explicit round-0 through round-4 paper snapshots from the review-refresh loop
- all code used to generate the numeric checks and paper-side assets
- generated result files and a source manifest
- dedicated high-resolution figure assets
- a detailed review opinion
- a score

The older [paper/main_round1_complete_package.pdf](paper/main_round1_complete_package.pdf) snapshot is preserved as a legacy freeze from the earlier one-shot package build.
