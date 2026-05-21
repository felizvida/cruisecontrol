---
name: figure-spec
description: "Generate deterministic workflow, architecture, and pipeline diagrams from structured JSON into editable SVG. Use for publication-ready non-data figures that should be precise rather than painterly."
argument-hint: [description-of-diagram]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

# Figure Spec

Generate a structured diagram for: **$ARGUMENTS**

This skill is for figures whose meaning comes from layout and relationships rather than from aesthetic illustration. Use it for architecture figures, workflow diagrams, audit cascades, and paper pipeline schematics.

## When To Use It

Use this for:

- architecture diagrams
- workflow figures
- system topology
- audit or review cascades
- structured process graphics that need to stay editable

Do not use this for:

- empirical plots
- image grids
- naturalistic illustrations

For plots and tables, use `/paper-figure`.

## Tooling

This repo ships a local renderer:

```bash
python3 scripts/figure_renderer.py validate path/to/spec.json
python3 scripts/figure_renderer.py render path/to/spec.json --output path/to/figure.svg
python3 scripts/figure_renderer.py schema
```

The renderer is deterministic, local, and produces editable SVG.

## Workflow

### Step 1: Decide the figure structure

Identify:

- main entities
- directional relationships
- grouping or layers
- whether the layout should be left-to-right, top-down, hub-and-spoke, or clustered

### Step 2: Draft a FigureSpec JSON

Save the spec alongside the figure, typically under:

```text
figures/specs/<figure_name>.json
```

Minimal example:

```json
{
  "canvas": {"width": 900, "height": 320},
  "nodes": [
    {"id": "input", "label": "Narrative Report", "x": 120, "y": 160},
    {"id": "plan", "label": "Paper Plan", "x": 320, "y": 160},
    {"id": "write", "label": "Paper Write", "x": 520, "y": 160},
    {"id": "review", "label": "Review Loop", "x": 720, "y": 160}
  ],
  "edges": [
    {"from": "input", "to": "plan"},
    {"from": "plan", "to": "write"},
    {"from": "write", "to": "review"}
  ]
}
```

### Step 3: Validate and render

Validate first, then render:

```bash
python3 scripts/figure_renderer.py validate figures/specs/workflow.json
python3 scripts/figure_renderer.py render figures/specs/workflow.json --output figures/workflow.svg
```

If you need LaTeX inclusion, convert the SVG to PDF with the local toolchain you already use for figure assets.

### Step 4: Review the figure

Check:

- label readability
- no overlapping nodes or group boxes
- edges land cleanly
- layout matches the paper argument

If the figure is too busy, simplify the spec rather than post-editing the SVG by hand.

## Design Rules

- Prefer short labels over paragraph labels.
- Use grouping to clarify structure, not to decorate the canvas.
- Do not put figure titles inside the SVG. Keep titles in the manuscript caption.
- Save the spec file with the output so the figure is reproducible.

## Integration Points

- `/paper-figure` should prefer this skill for architecture and workflow diagrams instead of ad hoc placeholders when the structure is clear enough.
- `/paper-writing` can call this indirectly whenever the figure plan contains formal non-data diagrams.
