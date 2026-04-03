#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = json.loads((ROOT / "results" / "summary_metrics.json").read_text())

TIMELINE_ROWS = list(csv.DictReader((ROOT / "results" / "event_timeline.csv").open()))
THEME_ROWS = list(csv.DictReader((ROOT / "results" / "theme_counts.csv").open()))
EDGE_ROWS = list(csv.DictReader((ROOT / "results" / "network_edges.csv").open()))

PAPER_FIGURES = ROOT / "paper" / "figures"
ASSET_TIMELINE = ROOT / "figure_assets" / "timeline"
ASSET_NETWORK = ROOT / "figure_assets" / "network"


PHASE_COLORS = {
    "access_and_utility": "blue!65!black",
    "frontier_brokerage": "green!50!black",
    "burr_crisis": "red!70!black",
    "rehabilitation": "orange!80!black",
    "retrospective_memory": "purple!70!black",
    "local_context": "brown!80!black",
    "frederick_repair": "yellow!60!orange!90!black",
}


NODE_POSITIONS = {
    "James Wilkinson": (0.0, 0.0),
    "Thomas Jefferson": (-3.4, 1.8),
    "James Madison": (3.2, 1.6),
    "William Eustis": (1.8, 3.2),
    "John Adams": (3.4, -1.4),
    "Frederick Town": (5.4, 0.0),
    "Frederick Barracks": (4.7, 2.8),
    "Meriwether Lewis": (-5.2, 2.6),
    "Lewis and Clark Expedition": (-4.6, 4.0),
    "Aaron Burr": (-2.1, -2.5),
    "Zebulon Pike": (-4.3, -0.7),
    "Monocacy": (5.0, -2.7),
    "Jabeil Kinson": (7.2, -1.7),
    "Roger B. Taney": (7.4, 1.0),
}

NODE_WEIGHTS = {
    row["node"]: row["weight"]
    for row in SUMMARY["top_nodes"]
}


def ensure_dirs() -> None:
    PAPER_FIGURES.mkdir(parents=True, exist_ok=True)
    ASSET_TIMELINE.mkdir(parents=True, exist_ok=True)
    ASSET_NETWORK.mkdir(parents=True, exist_ok=True)


def timeline_tex() -> str:
    ordered_rows = sorted(TIMELINE_ROWS, key=lambda row: row["date"])
    x_step = 0.95
    lines = [
        r"\begin{figure}[t]",
        r"\centering",
        r"\resizebox{\linewidth}{!}{%",
        r"\begin{tikzpicture}[x=1cm,y=1cm]",
        rf"\draw[thick] (0,0) -- ({(len(ordered_rows) - 1) * x_step + 0.4:.2f},0);",
    ]
    seen_years = set()
    for idx, row in enumerate(ordered_rows):
        x = idx * x_step
        year = row["year"]
        lines.append(rf"\draw ({x:.2f},0.08) -- ({x:.2f},-0.08);")
        if year not in seen_years:
            lines.append(rf"\node[font=\scriptsize, anchor=north] at ({x:.2f},-0.10) {{{year}}};")
            seen_years.add(year)

    for idx, row in enumerate(ordered_rows):
        x = idx * x_step
        y = 1.1 if idx % 2 == 0 else -1.1
        color = "yellow!60!orange!90!black" if row["frederick_role"] else PHASE_COLORS[row["phase"]]
        label = row["title"].replace("&", r"\&")
        lines.append(rf"\filldraw[{color}] ({x:.2f},{y:.2f}) circle (2.2pt);")
        lines.append(rf"\draw[{color}, thin] ({x:.2f},0) -- ({x:.2f},{y:.2f});")
        anchor = "south" if y > 0 else "north"
        lines.append(
            rf"\node[font=\tiny, align=center, text width=3.4cm, anchor={anchor}] at ({x:.2f},{y + (0.16 if y > 0 else -0.16):.2f}) {{{label}}};"
        )

    lines.extend(
        [
            r"\end{tikzpicture}",
            r"}",
            r"\caption{Event timeline of the curated Wilkinson corpus. Gold points mark Frederick-linked records. The clustering of gold points after 1804 shows Frederick as a repeated site of repair rather than a random afterthought.}",
            r"\label{fig:timeline}",
            r"\end{figure}",
        ]
    )
    return "\n".join(lines) + "\n"


def standalone_from_inner(inner: str, captionless: bool = False) -> str:
    lines = [
        r"\documentclass[tikz,border=6pt]{standalone}",
        r"\usepackage{tikz}",
        r"\begin{document}",
    ]
    if captionless:
        start = inner.find(r"\begin{tikzpicture}")
        end = inner.find(r"\end{tikzpicture}")
        if start != -1 and end != -1:
            inner = inner[start : end + len(r"\end{tikzpicture}")]
        else:
            inner = inner.replace(r"\begin{figure}[t]", "").replace(r"\end{figure}", "")
    lines.append(inner)
    lines.extend([r"\end{document}", ""])
    return "\n".join(lines)


def network_tex() -> str:
    lines = [
        r"\begin{figure}[t]",
        r"\centering",
        r"\begin{tikzpicture}[x=1cm,y=1cm]",
    ]

    interesting = []
    for row in EDGE_ROWS:
        if row["source"] in NODE_POSITIONS and row["target"] in NODE_POSITIONS:
            interesting.append(row)

    for row in interesting:
        source = row["source"]
        target = row["target"]
        weight = int(row["weight"])
        sx, sy = NODE_POSITIONS[source]
        tx, ty = NODE_POSITIONS[target]
        width = 0.4 + 0.35 * weight
        color = "yellow!60!orange!90!black" if "Frederick" in source or "Frederick" in target else "black!55"
        lines.append(rf"\draw[{color}, line width={width:.2f}pt] ({sx:.2f},{sy:.2f}) -- ({tx:.2f},{ty:.2f});")

    for node, (x, y) in NODE_POSITIONS.items():
        fill = "yellow!20" if "Frederick" in node else "blue!10"
        draw = "yellow!60!orange!90!black" if "Frederick" in node else "blue!60!black"
        label = node.replace("&", r"\&")
        weight = NODE_WEIGHTS.get(node, 1)
        inner_sep = 2.5 + 0.18 * weight
        font = r"\scriptsize" if weight < 5 else r"\footnotesize"
        lines.append(
            rf"\node[draw={draw}, fill={fill}, rounded corners=4pt, font={font}, align=center, inner sep={inner_sep:.2f}pt] at ({x:.2f},{y:.2f}) {{{label}}};"
        )

    lines.extend(
        [
            r"\end{tikzpicture}",
            r"\caption{Weighted connection network derived from the coded corpus. Node size and edge width both reflect weight. Frederick appears not merely as backdrop but as a bridge node linking Wilkinson to Adams, Madison, Taney, and the barracks that also served Jefferson's western projects.}",
            r"\label{fig:network}",
            r"\end{figure}",
        ]
    )
    return "\n".join(lines) + "\n"


def table_findings_tex() -> str:
    metrics = SUMMARY["core_claim_metrics"]
    total = SUMMARY["total_records"]
    frederick_records = SUMMARY["frederick_records"]
    share = int(round(SUMMARY["frederick_share"] * 100))
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\small",
        r"\begin{tabular}{p{0.52\linewidth}r}",
        r"\toprule",
        r"Metric & Value \\",
        r"\midrule",
        rf"Coded records in corpus & {total} \\",
        rf"Frederick-linked records & {frederick_records} ({share}\%) \\",
        rf"Frederick-linked records in rehabilitation phase & {metrics['frederick_rehabilitation_records']} \\",
        rf"Non-social survival modes & {metrics['instrumental_plus_protective_modes']} \\",
        rf"Pure social-access mode & {metrics['social_access_modes']} \\",
        rf"Retrospective-esteem mode & {metrics['retrospective_esteem_modes']} \\",
        r"\bottomrule",
        r"\end{tabular}",
        r"\caption{Core metrics from the coded corpus. The counts support a relationship defined much more by use and protection than by simple friendship.}",
        r"\label{tab:keyfindings}",
        r"\end{table}",
    ]
    return "\n".join(lines) + "\n"


def table_evidence_tex() -> str:
    evidence = SUMMARY["evidence_tiers"]
    primary_share = int(round(evidence["frederick_primary_share"] * 100))
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\small",
        r"\begin{tabular}{p{0.58\linewidth}r}",
        r"\toprule",
        r"Evidence tier & Records \\",
        r"\midrule",
        rf"Direct Jefferson--Wilkinson primary correspondence & {evidence['direct_relationship_primary']} \\",
        rf"Primary Frederick venue and outcome records & {evidence['primary_frederick_venue']} \\",
        rf"Contextual Frederick local sources & {evidence['contextual_frederick_local']} \\",
        rf"Primary share of Frederick-linked corpus & {primary_share}\% \\",
        r"\bottomrule",
        r"\end{tabular}",
        r"\caption{Evidence ladder for the paper's core claims. The Jefferson--Wilkinson thesis rests mostly on direct correspondence, while the Frederick synthesis combines a substantial primary procedural chain with contextual local sources.}",
        r"\label{tab:evidence}",
        r"\end{table}",
    ]
    return "\n".join(lines) + "\n"


def table_themes_tex() -> str:
    rows = []
    for row in THEME_ROWS:
        rows.append(
            rf"{row['author'].replace('&', r'\&')} & {row['warmth']} & {row['utility']} & {row['defense']} & {row['total']} \\"
        )
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\small",
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Author & Warmth & Utility & Defense & Total \\",
        r"\midrule",
        *rows,
        r"\bottomrule",
        r"\end{tabular}",
        r"\caption{Lexicon counts from excerpted correspondence and summaries. Wilkinson's surviving voice is especially saturated with defense language, while Jefferson's is warmer only when folded into judgment and utility.}",
        r"\label{tab:themes}",
        r"\end{table}",
    ]
    return "\n".join(lines) + "\n"


def table_theme_rates_tex() -> str:
    rows = []
    for author, counts in SUMMARY["theme_counts"].items():
        rows.append(
            rf"{author.replace('&', r'\&')} & {counts['warmth_per_1000_tokens']:.2f} & {counts['utility_per_1000_tokens']:.2f} & {counts['defense_per_1000_tokens']:.2f} \\"
        )
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\small",
        r"\begin{tabular}{lrrr}",
        r"\toprule",
        r"Author & Warmth / 1000 tok. & Utility / 1000 tok. & Defense / 1000 tok. \\",
        r"\midrule",
        *rows,
        r"\bottomrule",
        r"\end{tabular}",
        r"\caption{Normalized theme rates per 1000 tokens in the coded excerpts and summaries. The normalized view still leaves Wilkinson's voice more defense-heavy than warmth-heavy, while Jefferson remains most associated with utility language.}",
        r"\label{tab:themerates}",
        r"\end{table}",
    ]
    return "\n".join(lines) + "\n"


def table_primary_network_tex() -> str:
    rows = []
    for row in SUMMARY["primary_only_top_nodes"][:5]:
        rows.append(rf"{row['node'].replace('&', r'\&')} & {row['weight']} \\")
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\small",
        r"\begin{tabular}{lr}",
        r"\toprule",
        r"Primary-only node & Weight \\",
        r"\midrule",
        *rows,
        r"\bottomrule",
        r"\end{tabular}",
        r"\caption{Top nodes in the primary-only connection network. Frederick Town remains one of the heaviest nodes even when the later local-context sources are removed.}",
        r"\label{tab:primarynetwork}",
        r"\end{table}",
    ]
    return "\n".join(lines) + "\n"


def table_phase_modes_tex() -> str:
    phase_labels = {
        "access_and_utility": "Access / utility",
        "burr_crisis": "Burr crisis",
        "rehabilitation": "Rehabilitation",
        "retrospective_memory": "Retrospective memory",
        "frederick_repair": "Frederick repair",
        "frontier_brokerage": "Frontier brokerage",
        "local_context": "Local context",
    }
    interesting_modes = [
        "instrumental",
        "protective",
        "self_vindication",
        "procedural_management",
        "official_settlement",
        "retrospective_esteem",
        "testimonial_support",
    ]
    rows = []
    for phase in [
        "access_and_utility",
        "frontier_brokerage",
        "burr_crisis",
        "frederick_repair",
        "rehabilitation",
        "retrospective_memory",
        "local_context",
    ]:
        counts = SUMMARY["phase_mode_counts"].get(phase, {})
        row = [phase_labels[phase]]
        for mode in interesting_modes:
            row.append(str(counts.get(mode, 0)))
        rows.append(" & ".join(row) + r" \\")
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\small",
        r"\begin{tabular}{lccccccc}",
        r"\toprule",
        r"Phase & Inst. & Prot. & Self-vind. & Proced. & Official & Esteem & Testimony \\",
        r"\midrule",
        *rows,
        r"\bottomrule",
        r"\end{tabular}",
        r"\caption{Phase-by-mode summary from the coded corpus. The Burr crisis is almost purely protective, while rehabilitation mixes self-defense, procedure, testimony, and official settlement.}",
        r"\label{tab:phasemodes}",
        r"\end{table}",
    ]
    return "\n".join(lines) + "\n"


def table_frederick_spine_tex() -> str:
    spine_rows = []
    label_map = {
        "reputational_repair": "Wilkinson to Adams on fame",
        "trial_planning": "Eustis on venue",
        "jurisdiction_management": "Madison on jurisdiction",
        "witness_coordination": "Eustis on witness orders",
        "interrogatory_collection": "Kinson with interrogatories",
        "trial_venue": "Wilkinson on fairness",
        "external_testimony": "Adams in reply",
        "trial_outcome": "Madison on acquittal",
    }
    function_map = {
        "reputational_repair": "Shows Frederick as an early site of reputational self-defense",
        "trial_planning": "Shows Frederick chosen in advance as the intended court-martial venue",
        "jurisdiction_management": "Shows the president leaving the Frederick tribunal in possession of the case",
        "witness_coordination": "Shows the War Department mobilizing officers for the Frederick proceedings",
        "interrogatory_collection": "Shows Frederick reaching outward to collect testimony by interrogatory",
        "trial_venue": "Shows Frederick as the place where Wilkinson sought procedural fairness",
        "external_testimony": "Shows national testimony flowing back into the Frederick defense record",
        "trial_outcome": "Puts Frederick into the federal record through approved acquittal",
    }
    for row in TIMELINE_ROWS:
        if row["source_class"] == "primary" and row["frederick_role"] in function_map:
            spine_rows.append(
                rf"{row['year']} & {label_map[row['frederick_role']].replace('&', r'\&')} & {function_map[row['frederick_role']].replace('&', r'\&')} \\"
            )
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\small",
        r"\begin{tabular}{p{0.08\linewidth}>{\raggedright\arraybackslash}p{0.28\linewidth}>{\raggedright\arraybackslash}p{0.51\linewidth}}",
        r"\toprule",
        r"Year & Document & Function in argument \\",
        r"\midrule",
        *spine_rows,
        r"\bottomrule",
        r"\end{tabular}",
        r"\caption{The Frederick primary documentary chain used in the paper's core local argument. These records show venue choice, jurisdiction, evidence gathering, plea, and settlement before later contextual sources are added.}",
        r"\label{tab:frederickspine}",
        r"\end{table}",
    ]
    return "\n".join(lines) + "\n"


def table_place_nodes_tex() -> str:
    rows = []
    for row in SUMMARY["place_node_weights"]:
        rows.append(
            rf"{row['node'].replace('&', r'\&')} & {row['overall_weight']} & {row['primary_only_weight']} \\"
        )
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\small",
        r"\begin{tabular}{lrr}",
        r"\toprule",
        r"Place node & Full corpus & Primary-only \\",
        r"\midrule",
        *rows,
        r"\bottomrule",
        r"\end{tabular}",
        r"\caption{Place-node ranking in the connection network. Frederick Town dominates both in the full corpus and in the primary-only subset, reinforcing its role as the paper's central local geography.}",
        r"\label{tab:placenodes}",
        r"\end{table}",
    ]
    return "\n".join(lines) + "\n"


def write_text(path: Path, content: str) -> None:
    path.write_text(content)


def main() -> None:
    ensure_dirs()
    timeline = timeline_tex()
    network = network_tex()
    table_findings = table_findings_tex()
    table_evidence = table_evidence_tex()
    table_themes = table_themes_tex()
    table_theme_rates = table_theme_rates_tex()
    table_primary_network = table_primary_network_tex()
    table_phase_modes = table_phase_modes_tex()
    table_frederick_spine = table_frederick_spine_tex()
    table_place_nodes = table_place_nodes_tex()

    write_text(PAPER_FIGURES / "FIG_timeline.tex", timeline)
    write_text(PAPER_FIGURES / "FIG_network.tex", network)
    write_text(PAPER_FIGURES / "TABLE_findings.tex", table_findings)
    write_text(PAPER_FIGURES / "TABLE_evidence.tex", table_evidence)
    write_text(PAPER_FIGURES / "TABLE_themes.tex", table_themes)
    write_text(PAPER_FIGURES / "TABLE_theme_rates.tex", table_theme_rates)
    write_text(PAPER_FIGURES / "TABLE_primary_network.tex", table_primary_network)
    write_text(PAPER_FIGURES / "TABLE_phase_modes.tex", table_phase_modes)
    write_text(PAPER_FIGURES / "TABLE_frederick_spine.tex", table_frederick_spine)
    write_text(PAPER_FIGURES / "TABLE_place_nodes.tex", table_place_nodes)

    write_text(ASSET_TIMELINE / "timeline_standalone.tex", standalone_from_inner(timeline, captionless=True))
    write_text(ASSET_NETWORK / "network_standalone.tex", standalone_from_inner(network, captionless=True))


if __name__ == "__main__":
    main()
