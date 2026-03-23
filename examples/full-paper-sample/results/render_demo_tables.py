#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "demo_benchmark.json").read_text())
PAPER_FIGURES = ROOT.parent / "paper" / "figures"
FIGURE_ASSETS = ROOT.parent / "figure_assets"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def latex_escape(text: str) -> str:
    return (
        text.replace("\\", "\\textbackslash{}")
        .replace("&", "\\&")
        .replace("%", "\\%")
        .replace("_", "\\_")
        .replace("#", "\\#")
    )


def render_main_results() -> str:
    lines = [
        "\\begin{table*}[t]",
        "\\centering",
        "\\caption{Mission-level results from the executable stochastic deployment simulator. Higher mission return and distance are better. Lower system cost of transport, falls, and adaptation-compute energy are better.}",
        "\\label{tab:main-results}",
        "\\small",
        "\\resizebox{\\textwidth}{!}{%",
        "\\begin{tabular}{llrrrrr}",
        "\\toprule",
        "Regime & Method & Return & Distance (m) & System CoT & Falls / 100m & Compute Wh \\\\",
        "\\midrule",
    ]
    for regime in DATA["regimes"]:
        first = True
        for method in regime["methods"]:
            prefix = latex_escape(regime["name"]) if first else ""
            lines.append(
                f"{prefix} & {latex_escape(method['name'])} & {method['mission_return']:.2f} & {method['distance_m']} & {method['cost_of_transport']:.2f} & {method['falls_per_100m']:.2f} & {method['compute_wh']:.2f} \\\\"
            )
            first = False
        lines.append("\\midrule")
    lines[-1] = "\\bottomrule"
    lines.extend(["\\end{tabular}", "}", "\\end{table*}"])
    return "\n".join(lines) + "\n"


def render_cost_sweep() -> str:
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\caption{Low-battery terrain sweep over adaptation-cost scaling. Battery-gated adaptation matches always-on performance at low cost, overtakes it at moderate cost, and then degrades once adaptation becomes extremely expensive.}",
        "\\label{tab:cost-sweep}",
        "\\small",
        "\\begin{tabular}{rrrr}",
        "\\toprule",
        "Cost scale & Periodic & Always-on & Battery-gated \\\\",
        "\\midrule",
    ]
    for row in DATA["cost_sweep"]:
        lines.append(
            f"{row['cost_scale']:.2f} & {row['periodic']:.2f} & {row['always_on']:.2f} & {row['battery_gated']:.2f} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}", "\\end{table}"])
    return "\n".join(lines) + "\n"


def render_ablation() -> str:
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\caption{Low-battery terrain ablation. Removing battery state or compute-cost awareness weakens the scheduler and increases compute usage.}",
        "\\label{tab:ablation}",
        "\\small",
        "\\begin{tabular}{lrrr}",
        "\\toprule",
        "Variant & Return & Compute Wh & Adapt Calls \\\\",
        "\\midrule",
    ]
    for row in DATA["ablation"]:
        lines.append(
            f"{latex_escape(row['variant'])} & {row['mission_return']:.2f} & {row['compute_wh']:.2f} & {row['adapt_calls']} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}", "\\end{table}"])
    return "\n".join(lines) + "\n"


def get_regime(name: str) -> dict[str, object]:
    for regime in DATA["regimes"]:
        if regime["name"] == name:
            return regime
    raise KeyError(name)


def controller_standalone() -> str:
    return r"""\documentclass[border=10pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{times}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning}

\begin{document}
\begin{tikzpicture}[
  >=Latex,
  font=\small,
  box/.style={draw, rounded corners=3pt, align=center, minimum width=2.7cm, minimum height=1.0cm},
  flow/.style={->, line width=0.9pt}
]
\node[box, fill=blue!6] (obs) {State history\\and proprioception};
\node[box, fill=green!6, right=1.1cm of obs] (estimate) {Forward-only\\shift estimate};
\node[box, fill=yellow!10, above=1.1cm of estimate] (battery) {Battery state\\$\lambda(b_t)$};
\node[box, fill=orange!10, right=1.1cm of estimate] (scheduler) {Scheduler\\$s_t = \mathrm{gain}_t - \lambda(b_t)\,\mathrm{cost}_t$};
\node[box, fill=purple!8, right=1.1cm of scheduler] (adapt) {Adapt latent\\alignment};
\node[box, fill=gray!10, below=1.1cm of adapt] (skip) {Skip update};
\node[box, fill=red!6, right=1.2cm of adapt] (controller) {Locomotion\\controller};
\node[box, fill=cyan!8, right=1.1cm of controller] (action) {Action\\and energy use};

\draw[flow] (obs) -- (estimate);
\draw[flow] (estimate) -- node[midway, above] {$\mathrm{gain}_t,\mathrm{cost}_t$} (scheduler);
\draw[flow] (battery) -- (scheduler);
\draw[flow] (scheduler) -- node[midway, above] {$a_t=1$} (adapt);
\draw[flow] (scheduler) -- node[midway, right] {$a_t=0$} (skip);
\draw[flow] (adapt) -- (controller);
\draw[flow] (skip) -- (controller);
\draw[flow] (controller) -- (action);

\node[draw, rounded corners=3pt, align=left, anchor=north west, fill=white, text width=8.8cm] at ([xshift=-0.3cm,yshift=-0.7cm]obs.south west) {%
\textbf{Decision rule.}
Adaptation is treated as a control action rather than a free inner loop.
When battery is scarce, the scheduler penalizes compute more aggressively and falls back to sparse updates unless mismatch is high.};
\end{tikzpicture}
\end{document}
"""


def policy_tradeoff_standalone() -> str:
    terrain = get_regime("Terrain shift, 25% battery")
    payload = get_regime("Payload shift, 25% battery")

    def plot_coordinates(regime: dict[str, object]) -> str:
        parts = []
        for method in regime["methods"]:
            parts.append(f"({method['compute_wh']},{method['mission_return']})")
        return " ".join(parts)

    def point_labels(regime: dict[str, object]) -> list[str]:
        labels: list[str] = []
        for method in regime["methods"]:
            x = method["compute_wh"]
            y = method["mission_return"]
            anchor = "west" if method["name"] != "Always-on" else "east"
            labels.append(
                f"\\node[font=\\scriptsize, anchor={anchor}] at (axis cs:{x},{y}) {{{latex_escape(method['name'])}}};"
            )
        return labels

    terrain_points = plot_coordinates(terrain)
    payload_points = plot_coordinates(payload)
    terrain_labels = "\n".join(point_labels(terrain))
    payload_labels = "\n".join(point_labels(payload))

    return rf"""\documentclass[border=10pt]{{standalone}}
\usepackage[T1]{{fontenc}}
\usepackage{{times}}
\usepackage{{pgfplots}}
\pgfplotsset{{compat=1.18}}

\begin{{document}}
\begin{{tabular}}{{cc}}
\begin{{tikzpicture}}
\begin{{axis}}[
  width=7.2cm,
  height=5.6cm,
  title={{Terrain shift, 25\% battery}},
  xlabel={{Adaptation-compute energy (Wh)}},
  ylabel={{Mission return}},
  xmin=0,
  xmax=0.46,
  ymin=0.10,
  ymax=0.62,
  grid=major,
  tick label style={{font=\scriptsize}},
  label style={{font=\small}},
  title style={{font=\small}},
]
\addplot[only marks, mark=*, mark size=2.5pt, color=blue] coordinates {{{terrain_points}}};
{terrain_labels}
\end{{axis}}
\end{{tikzpicture}}
&
\begin{{tikzpicture}}
\begin{{axis}}[
  width=7.2cm,
  height=5.6cm,
  title={{Payload shift, 25\% battery}},
  xlabel={{Adaptation-compute energy (Wh)}},
  ylabel={{Mission return}},
  xmin=0,
  xmax=0.46,
  ymin=0.10,
  ymax=0.70,
  grid=major,
  tick label style={{font=\scriptsize}},
  label style={{font=\small}},
  title style={{font=\small}},
]
\addplot[only marks, mark=square*, mark size=2.5pt, color=red!75!black] coordinates {{{payload_points}}};
{payload_labels}
\end{{axis}}
\end{{tikzpicture}}
\end{{tabular}}
\end{{document}}
"""


def include_graphic(relative_path: str) -> str:
    return (
        "\\centering\n"
        f"\\includegraphics[width=0.98\\linewidth]{{{relative_path}}}\n"
    )


def render_figure_sources() -> None:
    controller_dir = FIGURE_ASSETS / "controller_schematic"
    tradeoff_dir = FIGURE_ASSETS / "policy_tradeoff"
    controller_dir.mkdir(parents=True, exist_ok=True)
    tradeoff_dir.mkdir(parents=True, exist_ok=True)

    write(controller_dir / "controller_schematic_standalone.tex", controller_standalone())
    write(tradeoff_dir / "policy_tradeoff_standalone.tex", policy_tradeoff_standalone())

    write(
        PAPER_FIGURES / "FIG_controller_schematic.tex",
        include_graphic("../figure_assets/controller_schematic/controller_schematic.pdf"),
    )
    write(
        PAPER_FIGURES / "FIG_policy_tradeoff.tex",
        include_graphic("../figure_assets/policy_tradeoff/policy_tradeoff.pdf"),
    )


PAPER_FIGURES.mkdir(parents=True, exist_ok=True)
write(PAPER_FIGURES / "TABLE_main_results.tex", render_main_results())
write(PAPER_FIGURES / "TABLE_cost_sweep.tex", render_cost_sweep())
write(PAPER_FIGURES / "TABLE_ablation.tex", render_ablation())
render_figure_sources()
