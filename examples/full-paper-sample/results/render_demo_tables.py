import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "demo_benchmark.json").read_text())
OUT = ROOT.parent / "paper" / "figures"


def write(path: Path, text: str) -> None:
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
        "\\caption{Synthetic mission-level benchmark used for the end-to-end workflow sample. Higher mission return and distance are better. Lower cost of transport, falls, and adaptation-compute energy are better.}",
        "\\label{tab:main-results}",
        "\\small",
        "\\begin{tabular}{llrrrrr}",
        "\\toprule",
        "Regime & Method & Return & Distance (m) & CoT & Falls / 100m & Compute Wh \\\\",
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
    lines.extend(["\\end{tabular}", "\\end{table*}"])
    return "\n".join(lines) + "\n"


def render_cost_sweep() -> str:
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\caption{Adaptation-cost sweep on the low-battery benchmark slice. The battery-gated policy degrades more slowly as adaptation cost increases.}",
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
        "\\caption{Low-battery ablation on the terrain-shift slice. Removing battery state or compute-cost awareness weakens the policy.}",
        "\\label{tab:ablation}",
        "\\small",
        "\\begin{tabular}{lrr}",
        "\\toprule",
        "Variant & Return & CoT \\\\",
        "\\midrule",
    ]
    for row in DATA["ablation"]:
        lines.append(
            f"{latex_escape(row['variant'])} & {row['mission_return']:.2f} & {row['cost_of_transport']:.2f} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}", "\\end{table}"])
    return "\n".join(lines) + "\n"


def render_controller_placeholder() -> str:
    return (
        "\\fbox{%\n"
        "\\parbox{0.93\\linewidth}{%\n"
        "\\textbf{[AUTO\\_PLACEHOLDER] Controller schematic.}\\\\\n"
        "State history and battery state feed a small scheduler. The scheduler chooses between no update, periodic update, or forward-only embedding alignment.\\\\\n"
        "The paper sample keeps this schematic as a placeholder because the repo does not ship a real quadruped controller implementation.}%\n"
        "}\n"
    )


def render_regime_placeholder() -> str:
    return (
        "\\fbox{%\n"
        "\\parbox{0.93\\linewidth}{%\n"
        "\\textbf{[AUTO\\_PLACEHOLDER] Regime map.}\\\\\n"
        "Low battery + strong shift: battery-gated policy wins.\\\\\n"
        "High battery + strong shift: always-on remains competitive.\\\\\n"
        "Low shift: static or periodic adaptation can be sufficient.}%\n"
        "}\n"
    )


OUT.mkdir(parents=True, exist_ok=True)
write(OUT / "TABLE_main_results.tex", render_main_results())
write(OUT / "TABLE_cost_sweep.tex", render_cost_sweep())
write(OUT / "TABLE_ablation.tex", render_ablation())
write(OUT / "FIG_controller_placeholder.tex", render_controller_placeholder())
write(OUT / "FIG_regime_placeholder.tex", render_regime_placeholder())
