#!/usr/bin/env python3
"""Compute reproducible summaries for the Codex zebrafish brain paper."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "curated_evidence.json"
RESULTS_DIR = ROOT / "results"


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def wilson_interval(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return 0.0, 0.0
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    margin = z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n) / denom
    return max(0.0, center - margin), min(1.0, center + margin)


def hypergeom_prob(a: int, row1: int, col1: int, total: int) -> float:
    return math.comb(col1, a) * math.comb(total - col1, row1 - a) / math.comb(total, row1)


def fisher_one_sided_greater(a: int, b: int, c: int, d: int) -> float:
    row1 = a + b
    col1 = a + c
    total = a + b + c + d
    min_a = max(0, row1 - (total - col1))
    max_a = min(row1, col1)
    return sum(hypergeom_prob(x, row1, col1, total) for x in range(a, max_a + 1))


def main() -> None:
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    totals = payload["region_totals"]
    markers = payload["marker_counts"]
    ptms = payload["ptm_totals"]

    tel_total = totals["telencephalon_proteoforms"]
    teo_total = totals["optic_tectum_proteoforms"]
    shared = totals["shared_proteoforms"]
    union = tel_total + teo_total - shared
    protein_overlap = totals["protein_overlap"]
    protein_union = totals["protein_union"]

    summary = {
        "telencephalon_proteoforms": tel_total,
        "optic_tectum_proteoforms": teo_total,
        "shared_proteoforms": shared,
        "union_proteoforms": union,
        "jaccard_overlap": round(shared / union, 4),
        "telencephalon_unique": tel_total - shared,
        "optic_tectum_unique": teo_total - shared,
        "telencephalon_specialization_fraction": round((tel_total - shared) / tel_total, 4),
        "optic_tectum_specialization_fraction": round((teo_total - shared) / teo_total, 4),
        "protein_overlap_fraction": round(protein_overlap / protein_union, 4),
        "teo_to_tel_ratio": round(teo_total / tel_total, 4),
        "modification_fraction": round(ptms["modified_total"] / ptms["total_proteoforms"], 4),
        "n_terminal_acetylation_fraction_of_modified": round(
            ptms["n_terminal_acetylated"] / ptms["modified_total"], 4
        ),
        "single_run_high_water_mark": totals["single_run_high_water_mark"],
        "cells_per_section_estimate": totals["cells_per_section_estimate"],
        "cells_per_run_estimate": totals["cells_per_run_estimate"],
    }
    tel_prevalence = tel_total / (tel_total + teo_total)
    teo_prevalence = teo_total / (tel_total + teo_total)

    marker_rows: list[dict[str, object]] = []
    group_consistency_rows: list[dict[str, object]] = []
    axis_totals = {
        "telencephalon": {"matched": 0, "spillover": 0},
        "optic_tectum": {"matched": 0, "spillover": 0},
    }
    aligned_total = 0
    marker_total = 0
    groups_favoring_expected = 0
    group_matched_shares: list[float] = []

    for marker in markers:
        tel = marker["tel_count"]
        teo = marker["teo_count"]
        total = tel + teo
        bias = math.log2((tel + 1) / (teo + 1))
        axis = marker["functional_axis"]
        matched = tel if axis == "telencephalon" else teo
        spillover = teo if axis == "telencephalon" else tel
        matched_share = matched / total
        favors_expected = matched > spillover
        groups_favoring_expected += 1 if favors_expected else 0
        group_matched_shares.append(matched_share)
        aligned_total += matched
        marker_total += total
        axis_totals[axis]["matched"] += matched
        axis_totals[axis]["spillover"] += spillover
        marker_rows.append(
            {
                "gene": marker["gene"],
                "label": marker["label"],
                "functional_axis": axis,
                "tel_count": tel,
                "teo_count": teo,
                "matched_count": matched,
                "spillover_count": spillover,
                "total_count": total,
                "log2_tel_over_teo_plus1": round(bias, 3),
                "interpretation": marker["interpretation"],
            }
        )
        group_consistency_rows.append(
            {
                "label": marker["label"],
                "functional_axis": axis,
                "matched_share": round(matched_share, 4),
                "favors_expected_region": "yes" if favors_expected else "no",
            }
        )

    axis_expected = {}
    axis_rows = []
    for axis, counts in axis_totals.items():
        total = counts["matched"] + counts["spillover"]
        low, high = wilson_interval(counts["matched"], total)
        expected = tel_prevalence if axis == "telencephalon" else teo_prevalence
        axis_expected[axis] = expected
        axis_rows.append(
            {
                "functional_axis": axis,
                "matched_count": counts["matched"],
                "spillover_count": counts["spillover"],
                "alignment_fraction": round(counts["matched"] / total, 4),
                "wilson_low": round(low, 4),
                "wilson_high": round(high, 4),
                "expected_fraction_under_region_prevalence": round(expected, 4),
                "alignment_lift_over_prevalence": round(counts["matched"] / total - expected, 4),
            }
        )

    summary["marker_alignment_fraction"] = round(aligned_total / marker_total, 4)
    expected_overall_alignment = sum(
        (counts["matched"] + counts["spillover"]) * axis_expected[axis]
        for axis, counts in axis_totals.items()
    ) / marker_total
    summary["expected_alignment_under_region_prevalence"] = round(expected_overall_alignment, 4)
    summary["alignment_excess_over_prevalence"] = round(
        summary["marker_alignment_fraction"] - expected_overall_alignment, 4
    )
    summary["marker_panel_total_counts"] = marker_total
    summary["marker_panel_fraction_of_regional_count_mass"] = round(
        marker_total / (tel_total + teo_total), 4
    )
    summary["marker_groups_total"] = len(markers)
    summary["marker_groups_favoring_expected_region"] = groups_favoring_expected
    summary["group_level_mean_matched_share"] = round(
        sum(group_matched_shares) / len(group_matched_shares), 4
    )
    summary["group_level_min_matched_share"] = round(min(group_matched_shares), 4)
    summary["group_level_one_sided_sign_p"] = round(0.5 ** len(markers), 6)
    summary["protein_to_proteoform_overlap_ratio"] = round(
        summary["protein_overlap_fraction"] / summary["jaccard_overlap"], 4
    )

    a = axis_totals["telencephalon"]["matched"]
    b = axis_totals["telencephalon"]["spillover"]
    c = axis_totals["optic_tectum"]["spillover"]
    d = axis_totals["optic_tectum"]["matched"]
    fisher = {
        "table": {
            "tel_axis_in_tel": a,
            "tel_axis_in_teo": b,
            "teo_axis_in_tel": c,
            "teo_axis_in_teo": d,
        },
        "odds_ratio": round((a * d) / (b * c), 4),
        "one_sided_p_greater": fisher_one_sided_greater(a, b, c, d),
    }

    leave_one_out_rows = []
    for marker in markers:
        remaining = [m for m in markers if m["gene"] != marker["gene"]]
        matched = 0
        total = 0
        for item in remaining:
            axis = item["functional_axis"]
            tel = item["tel_count"]
            teo = item["teo_count"]
            matched += tel if axis == "telencephalon" else teo
            total += tel + teo
        leave_one_out_rows.append(
            {
                "removed_marker": marker["label"],
                "remaining_alignment_fraction": round(matched / total, 4),
            }
        )
    summary["leave_one_out_min_alignment"] = round(
        min(row["remaining_alignment_fraction"] for row in leave_one_out_rows), 4
    )
    summary["leave_one_out_max_alignment"] = round(
        max(row["remaining_alignment_fraction"] for row in leave_one_out_rows), 4
    )

    technical_rows = [
        {
            "region": "telencephalon",
            "duplicate_mean": totals["tel_duplicate_mean"],
            "duplicate_sd": totals["tel_duplicate_sd"],
            "cv": round(totals["tel_duplicate_sd"] / totals["tel_duplicate_mean"], 4),
            "duplicate_recovery_fraction": round(
                totals["tel_duplicate_mean"] / tel_total, 4
            ),
        },
        {
            "region": "optic_tectum",
            "duplicate_mean": totals["teo_duplicate_mean"],
            "duplicate_sd": totals["teo_duplicate_sd"],
            "cv": round(totals["teo_duplicate_sd"] / totals["teo_duplicate_mean"], 4),
            "duplicate_recovery_fraction": round(
                totals["teo_duplicate_mean"] / teo_total, 4
            ),
        },
    ]
    summary["single_run_proteoforms_per_estimated_cell"] = round(
        totals["single_run_high_water_mark"] / totals["cells_per_run_estimate"], 4
    )

    ptm_rows = []
    total_ptm = ptms["total_proteoforms"]
    for key, value in ptms.items():
        ptm_rows.append(
            {
                "modification": key,
                "count": value,
                "fraction_of_total": round(value / total_ptm, 4),
            }
        )

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "summary_metrics.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (RESULTS_DIR / "functional_test.json").write_text(
        json.dumps(fisher, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_csv(
        RESULTS_DIR / "region_summary.csv",
        [{"metric": key, "value": value} for key, value in summary.items()],
        ["metric", "value"],
    )
    write_csv(
        RESULTS_DIR / "marker_bias.csv",
        marker_rows,
        [
            "gene",
            "label",
            "functional_axis",
            "tel_count",
            "teo_count",
            "matched_count",
            "spillover_count",
            "total_count",
            "log2_tel_over_teo_plus1",
            "interpretation",
        ],
    )
    write_csv(
        RESULTS_DIR / "group_consistency.csv",
        group_consistency_rows,
        [
            "label",
            "functional_axis",
            "matched_share",
            "favors_expected_region",
        ],
    )
    write_csv(
        RESULTS_DIR / "axis_summary.csv",
        axis_rows,
        [
            "functional_axis",
            "matched_count",
            "spillover_count",
            "alignment_fraction",
            "wilson_low",
            "wilson_high",
            "expected_fraction_under_region_prevalence",
            "alignment_lift_over_prevalence",
        ],
    )
    write_csv(
        RESULTS_DIR / "leave_one_out_alignment.csv",
        leave_one_out_rows,
        ["removed_marker", "remaining_alignment_fraction"],
    )
    write_csv(
        RESULTS_DIR / "technical_replicate_summary.csv",
        technical_rows,
        ["region", "duplicate_mean", "duplicate_sd", "cv", "duplicate_recovery_fraction"],
    )
    write_csv(
        RESULTS_DIR / "ptm_summary.csv",
        ptm_rows,
        ["modification", "count", "fraction_of_total"],
    )


if __name__ == "__main__":
    main()
