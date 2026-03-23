#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "serialization_probe.json").read_text())
PAPER_FIGURES = ROOT.parent / "paper" / "figures"
FIGURE_ASSETS = ROOT.parent / "figure_assets"

ORDER_STYLES = {
    "Hilbert": {"color": "blue!75!black", "mark": "*"},
    "Morton": {"color": "green!45!black", "mark": "square*"},
    "Raster": {"color": "orange!90!black", "mark": "triangle*"},
    "Random": {"color": "red!75!black", "mark": "diamond*"},
}


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


def orderings() -> list[dict[str, object]]:
    return DATA["orderings"]


def render_probe_summary_table() -> str:
    avg_occ = DATA["dataset"]["average_occupied_voxels"]
    num_samples = DATA["dataset"]["num_samples"]
    lines = [
        "\\begin{table*}[t]",
        "\\centering",
        "\\small",
        f"\\caption{{Summary of the executable serialization probe on {num_samples} synthetic 16$^3$ microenvironments (average occupancy {avg_occ:.1f} voxels). Lower neighbor span is better. Higher retention and recoverability are better.}}",
        "\\label{tab:probe-summary}",
        "\\resizebox{\\textwidth}{!}{%",
        "\\begin{tabular}{lrrrrrrr}",
        "\\toprule",
        "Ordering & Mean 6-neighbor span & Median 6-neighbor span & Adj. $\\leq 8$ & Adj. $\\leq 16$ & Recover $\\leq 128$ & Recover $\\leq 256$ & Recover $\\leq 512$ \\\\",
        "\\midrule",
    ]
    for item in orderings():
        adjacency = item["adjacency"]
        recovery = item["support_recovery"]
        rec_128 = next(row["recoverability"] for row in recovery["recoverability"] if row["budget"] == 128)
        rec_256 = next(row["recoverability"] for row in recovery["recoverability"] if row["budget"] == 256)
        rec_512 = next(row["recoverability"] for row in recovery["recoverability"] if row["budget"] == 512)
        adj_8 = next(row["retention"] for row in adjacency["retention"] if row["threshold"] == 8)
        adj_16 = next(row["retention"] for row in adjacency["retention"] if row["threshold"] == 16)
        lines.append(
            f"{latex_escape(item['label'])} & {adjacency['mean_span']:.1f} & {adjacency['median_span']} & {adj_8:.3f} & {adj_16:.3f} & {rec_128:.3f} & {rec_256:.3f} & {rec_512:.3f} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}", "}", "\\end{table*}"])
    return "\n".join(lines) + "\n"


def curve_coordinates(rows: list[dict[str, object]], x_key: str, y_key: str) -> str:
    return " ".join(f"({row[x_key]},{row[y_key]})" for row in rows)


def probe_curves_standalone() -> str:
    first_axis_plots = []
    second_axis_plots = []
    for item in orderings():
        label = item["label"]
        style = ORDER_STYLES[label]
        adjacency_coords = curve_coordinates(item["adjacency"]["retention"], "threshold", "retention")
        recovery_coords = curve_coordinates(item["support_recovery"]["recoverability"], "budget", "recoverability")
        first_axis_plots.append(
            rf"\addplot[line width=1.0pt, color={style['color']}, mark={style['mark']}, mark size=2.4pt] coordinates {{{adjacency_coords}}};"
        )
        second_axis_plots.append(
            rf"\addplot[line width=1.0pt, color={style['color']}, mark={style['mark']}, mark size=2.4pt] coordinates {{{recovery_coords}}};"
        )

    legend = "\n".join(rf"\addlegendentry{{{latex_escape(item['label'])}}}" for item in orderings())
    return rf"""\documentclass[border=10pt]{{standalone}}
\usepackage[T1]{{fontenc}}
\usepackage{{times}}
\usepackage{{pgfplots}}
\usepgfplotslibrary{{groupplots}}
\pgfplotsset{{compat=1.18}}

\begin{{document}}
\begin{{tikzpicture}}
\begin{{groupplot}}[
  group style={{group size=2 by 1, horizontal sep=1.6cm}},
]
\nextgroupplot[
  width=7.2cm,
  height=5.9cm,
  xlabel={{Span threshold}},
  ylabel={{Adjacent-pair retention}},
  xmin=2,
  xmax=264,
  ymin=0,
  ymax=1.05,
  xtick={{4,8,16,32,64,128,256}},
  xticklabels={{4,8,16,32,64,128,256}},
  grid=major,
  tick label style={{font=\scriptsize}},
  label style={{font=\small}},
  title style={{font=\small}},
  title={{Occupied 6-neighbor locality}},
  legend style={{font=\scriptsize, draw=none, at={{(0.5,-0.25)}}, anchor=north, legend columns=2}}
]
{chr(10).join(first_axis_plots)}
{legend}

\nextgroupplot[
  width=7.2cm,
  height=5.9cm,
  xlabel={{Sequence budget}},
  ylabel={{Neighborhood recoverability}},
  xmin=48,
  xmax=1040,
  ymin=0,
  ymax=1.05,
  xtick={{64,128,256,512,1024}},
  xticklabels={{64,128,256,512,1024}},
  grid=major,
  tick label style={{font=\scriptsize}},
  label style={{font=\small}},
  title style={{font=\small}},
  title={{Context-budget microenvironment recovery}}
]
{chr(10).join(second_axis_plots)}
\end{{groupplot}}
\end{{tikzpicture}}
\end{{document}}
"""


def include_graphic(relative_path: str) -> str:
    return (
        "\\begin{figure}[t]\n"
        "\\centering\n"
        f"\\includegraphics[width=0.98\\linewidth]{{{relative_path}}}\n"
        "\\caption{Computed probe curves. Left: retention of occupied 6-neighbor pairs as the allowable serialized span increases. Right: recovery of mixed-channel local environments as the available sequence budget increases. Hilbert and Morton behave smoothly under tight budgets, raster shows a plane-boundary cliff, and random order destroys locality.}\n"
        "\\label{fig:probe-curves}\n"
        "\\end{figure}\n"
    )


def main() -> None:
    probe_dir = FIGURE_ASSETS / "probe_curves"
    write(PAPER_FIGURES / "TABLE_probe_summary.tex", render_probe_summary_table())
    write(PAPER_FIGURES / "FIG_probe_curves.tex", include_graphic("../figure_assets/probe_curves/probe_curves.pdf"))
    write(probe_dir / "probe_curves_standalone.tex", probe_curves_standalone())


if __name__ == "__main__":
    main()
