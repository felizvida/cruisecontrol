#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "reconstruction_checks.json").read_text())
PAPER_FIGURES = ROOT.parent / "paper" / "figures"
FIGURE_ASSETS = ROOT.parent / "figure_assets"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def table_numeric_checks() -> str:
    rows = []
    with (ROOT / "check_summary.csv").open() as handle:
        for row in csv.DictReader(handle):
            rows.append(row)

    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\small",
        "\\caption{Generated numeric sanity checks for the theorem package. The theorem is proved analytically; the table simply confirms that the basis-effect reconstruction and additivity formulas behave at machine precision on random sampled examples.}",
        "\\label{tab:numeric-checks}",
        "\\begin{tabular}{rrrr}",
        "\\toprule",
        "$d$ & Max recon. error & Max rep. residual & Max additivity residual \\\\",
        "\\midrule",
    ]
    for row in rows:
        lines.append(
            f"{row['dimension']} & {row['max_reconstruction_error']} & {row['max_representation_residual']} & {row['max_additivity_residual']} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}", "\\end{table}"])
    return "\n".join(lines) + "\n"


def proof_staircase_standalone() -> str:
    return r"""\documentclass[border=10pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{times}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning}

\begin{document}
\begin{tikzpicture}[
  >=Latex,
  font=\small,
  box/.style={draw, rounded corners=4pt, align=center, minimum width=3.2cm, minimum height=1.1cm},
  arrow/.style={->, line width=0.9pt}
]
\node[box, fill=blue!8] (a) {Bounded interval\\additivity};
\node[box, fill=green!8, right=1.1cm of a] (b) {Three-number\\rule on $[0,1]$};
\node[box, fill=orange!10, right=1.1cm of b] (c) {Shadow rule\\on the sphere};
\node[box, fill=red!8, right=1.1cm of c] (d) {Matrix theorem\\on effects};

\draw[arrow] (a) -- (b);
\draw[arrow] (b) -- (c);
\draw[arrow] (c) -- (d);

\node[draw, rounded corners=4pt, align=left, fill=white, text width=11.5cm, anchor=north west]
at ([xshift=-0.2cm,yshift=-0.8cm]a.south west) {%
\textbf{Idea.}
The paper climbs one rung at a time.
First show that a bounded rule with $h(x+y)=h(x)+h(y)$ must be linear.
Then turn that into an elementary sphere result.
Finally lift the same additivity idea to real symmetric matrices and recover the trace formula.};
\end{tikzpicture}
\end{document}
"""


def sphere_shadow_standalone() -> str:
    return r"""\documentclass[border=10pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{times}
\usepackage{tikz}
\usetikzlibrary{arrows.meta}

\begin{document}
\begin{tikzpicture}[>=Latex, font=\small]
\draw[line width=0.8pt] (0,0) circle (2.2);
\draw[dashed] (-2.2,0) -- (2.2,0);
\fill (0,2.2) circle (1.5pt);
\node[above] at (0,2.2) {$p$};
\fill (1.45,1.3) circle (1.4pt);
\node[right] at (1.45,1.3) {$u$};
\draw[->, line width=0.9pt] (0,0) -- (1.45,1.3);
\draw[dotted] (1.45,1.3) -- (1.45,0);
\node[below] at (1.45,0) {equator};
\node[right] at (1.55,0.68) {$\sqrt{t}$};

\node[draw, rounded corners=4pt, align=left, fill=white, text width=6.4cm, anchor=west]
at (3.1,0.4) {%
\textbf{Warmup picture.}
If a rule depends only on the squared height $t=(u\cdot p)^2$, then an orthonormal triple gives three numbers $a,b,c$ with $a+b+c=1$. The proof becomes a one-variable problem on $[0,1]$.};
\end{tikzpicture}
\end{document}
"""


def include_figure(relative_path: str, caption: str, label: str) -> str:
    return (
        "\\begin{figure}[t]\n"
        "\\centering\n"
        f"\\includegraphics[width=0.98\\linewidth]{{{relative_path}}}\n"
        f"\\caption{{{caption}}}\n"
        f"\\label{{{label}}}\n"
        "\\end{figure}\n"
    )


def main() -> None:
    PAPER_FIGURES.mkdir(parents=True, exist_ok=True)

    staircase_dir = FIGURE_ASSETS / "proof_staircase"
    shadow_dir = FIGURE_ASSETS / "sphere_shadow"
    staircase_dir.mkdir(parents=True, exist_ok=True)
    shadow_dir.mkdir(parents=True, exist_ok=True)

    write(PAPER_FIGURES / "TABLE_numeric_checks.tex", table_numeric_checks())
    write(
        PAPER_FIGURES / "FIG_proof_staircase.tex",
        include_figure(
            "../figure_assets/proof_staircase/proof_staircase.pdf",
            "The proof route used in the paper. Each step keeps the ideas concrete and postpones the matrix theorem until the one-variable and sphere warmups are already in place.",
            "fig:staircase",
        ),
    )
    write(
        PAPER_FIGURES / "FIG_sphere_shadow.tex",
        include_figure(
            "../figure_assets/sphere_shadow/sphere_shadow.pdf",
            "The high-school warmup picture. A rule that depends only on squared height turns an orthonormal triple on the sphere into a three-number identity on $[0,1]$.",
            "fig:shadow",
        ),
    )
    write(staircase_dir / "proof_staircase_standalone.tex", proof_staircase_standalone())
    write(shadow_dir / "sphere_shadow_standalone.tex", sphere_shadow_standalone())


if __name__ == "__main__":
    main()
