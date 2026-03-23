# Narrative Report

## Working Title

**From Shadow Lengths to Density Matrices: A No-Physics Route to a Finite-Dimensional Gleason-Type Theorem**

## Core Goal

Produce a theoretical paper example that is much simpler to explain than the usual Gleason-theorem literature, while staying mathematically honest about scope.

## Chosen Claim

The paper does **not** claim a new proof of Gleason's original 1957 theorem.

The paper does claim:

1. an elementary one-variable lemma about bounded additive functions on `[0,1]`
2. an immediate corollary for sphere rules that depend only on squared height
3. a short proof of the finite-dimensional **real effect-space** analogue of Gleason's theorem

## Why This Is A Good Theoretical Example

- The warmup theorem really can be explained with fractions, boundedness, and "numbers that add to one."
- The main matrix theorem uses only finite-dimensional linear algebra.
- The result is strong enough to feel like real theory, but modest enough to state honestly.

## Computation Role

Because this repo requires papers to ship with computation-backed artifacts, the package also includes scripts that:

1. generate random density matrices and random effects
2. reconstruct the representing matrix from basis-effect values
3. verify tiny residuals across random trials
4. emit paper tables and figure assets from the generated outputs

These computations do **not** prove the theorem. They act as reproducible sanity checks and illustrations.
