# Improvement Diff

## Framing Changes

- **Old**: lower-dimensional CNNs can compete with volumetric CNNs when 3D data are mapped with a Hilbert-style traversal
- **New**: serialization is a first-class design interface for irregular 3D and biomolecular learning

## Claim Changes

- **Removed**: the original benchmark comparison as the headline contribution
- **Added**: a cross-era taxonomy of serialized 3D learning
- **Added**: an executable context-budget study of serialization quality
- **Added**: a design framework for locality, token efficiency, channel semantics, and reversibility
- **Added**: a biomolecular AI agenda

## Method Changes

- **Old**: empirical methods paper with handcrafted CNN comparisons
- **New**: hybrid paper grounded in source-paper analysis, modern primary literature, and a deterministic synthetic probe

## Evidence Changes

- **Old**: ModelNet10 and K-Ras/H-Ras experiments
- **New**: literature synthesis across Point Transformer, Point Transformer V3, PointMamba, Voxel Mamba, NoKSR, and AtoMAE, plus executable locality and context-budget measurements generated in this repo

## Figure / Table Changes

- **Old**: performance tables and rendering examples
- **New**: source-vs-upgrade comparison, serialization taxonomy, executable probe summary, research agenda, and computed probe curves

## Limitation Changes

- **Old**: future work on scaling the original empirical method
- **New**: explicit statement that the upgraded paper includes a real synthetic probe but does not claim a real biomolecular benchmark

## Why The New Manuscript Is Distinct

This is not a line edit of the 2018 paper. It is a new paper with:

- a different audience
- a different paper type
- a different central claim
- a different supporting evidence base
- a new executable computation path
