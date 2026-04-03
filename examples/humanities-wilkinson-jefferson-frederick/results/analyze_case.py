#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import platform
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "curated_corpus.json"
INVENTORY_JSON = ROOT / "data" / "corpus_inventory.json"
TRACEABILITY_JSON = ROOT / "data" / "evidence_traceability.json"

TIMELINE_CSV = ROOT / "results" / "event_timeline.csv"
THEME_CSV = ROOT / "results" / "theme_counts.csv"
EDGE_CSV = ROOT / "results" / "network_edges.csv"
SUMMARY_JSON = ROOT / "results" / "summary_metrics.json"
SENSITIVITY_JSON = ROOT / "results" / "sensitivity_checks.json"
ENVIRONMENT_JSON = ROOT / "code" / "environment_versions.json"
PLACE_NODES = ["Frederick Town", "Frederick Barracks", "Monocacy"]
NON_SOCIAL_MODES = {
    "instrumental",
    "protective",
    "self_vindication",
    "official_settlement",
    "retrospective_defense",
    "procedural_management",
    "evidentiary_collection",
    "testimonial_support",
}


LEXICONS = {
    "warmth": {"esteem", "respect", "attachment", "friend", "friendly", "sympathy", "regard", "wishes"},
    "utility": {"service", "services", "public", "conduct", "duty", "duties", "orders", "direction", "country"},
    "defense": {"honor", "calumny", "calumnies", "persecution", "persecutions", "trial", "fair", "vindication", "confidence", "support"},
}

CONSERVATIVE_LEXICONS = {
    "warmth": {"esteem", "respect", "sympathy", "regard"},
    "utility": {"service", "services", "duty", "duties", "orders"},
    "defense": {"honor", "calumny", "calumnies", "persecution", "persecutions", "trial", "vindication"},
}


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z]+", text.lower())


def repository_identifier(url: str) -> str:
    if "founders.archives.gov/documents/" in url:
        return url.rstrip("/").rsplit("/", 1)[-1]
    if "wardepartmentpapers.org/s/home/item/" in url:
        return "wardepartment:" + url.rstrip("/").rsplit("/", 1)[-1]
    if "loc.gov/item/" in url:
        return "loc:" + url.rstrip("/").rsplit("/", 1)[-1]
    if "archive.org/details/" in url:
        return "archive:" + url.rstrip("/").rsplit("/", 1)[-1]
    if "archives.gov" in url and "court-martial-case-files" in url:
        return "nara:rg153-court-martial-guide"
    if "hmdb.org" in url:
        return "hmdb:" + url.split("=")[-1]
    if "maryland.gov" in url or "msa.maryland.gov" in url:
        return "msa:" + url.rstrip("/").rsplit("/", 1)[-1]
    if "umich.edu" in url:
        return "clements:" + url.rstrip("/").rsplit("/", 1)[-1]
    return url


def compute_theme_stats(records: list[dict], *, lexicons: dict[str, set[str]], include_summary: bool) -> dict[str, dict]:
    author_buckets = {"James Wilkinson": Counter(), "Thomas Jefferson": Counter()}
    author_totals = {
        "James Wilkinson": {"records": 0, "tokens": 0},
        "Thomas Jefferson": {"records": 0, "tokens": 0},
    }
    for row in records:
        text = row["excerpt"] if not include_summary else f'{row["excerpt"]} {row["summary"]}'
        tokens = tokenize(text)
        author = row["author"]
        if author not in author_buckets:
            continue
        author_totals[author]["records"] += 1
        author_totals[author]["tokens"] += len(tokens)
        for category, words in lexicons.items():
            author_buckets[author][category] += sum(1 for token in tokens if token in words)

    result = {}
    for author, counts in author_buckets.items():
        tokens = author_totals[author]["tokens"]
        result[author] = {
            "warmth": counts["warmth"],
            "utility": counts["utility"],
            "defense": counts["defense"],
            "records": author_totals[author]["records"],
            "tokens": tokens,
            "warmth_per_1000_tokens": round(counts["warmth"] * 1000 / tokens, 2) if tokens else 0.0,
            "utility_per_1000_tokens": round(counts["utility"] * 1000 / tokens, 2) if tokens else 0.0,
            "defense_per_1000_tokens": round(counts["defense"] * 1000 / tokens, 2) if tokens else 0.0,
        }
    return result


def place_weights_for_records(records: list[dict], *, primary_only: bool = False) -> dict[str, int]:
    weights = Counter()
    for row in records:
        if primary_only and row["source_class"] != "primary":
            continue
        for left, right in row["connections"]:
            weights[left] += 1
            weights[right] += 1
    return {node: weights.get(node, 0) for node in PLACE_NODES}


def latexmk_version() -> str | None:
    try:
        output = subprocess.check_output(["latexmk", "-v"], text=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    return output.splitlines()[0].strip() if output else None


def main() -> None:
    records = json.loads(DATA.read_text())

    TIMELINE_CSV.parent.mkdir(parents=True, exist_ok=True)

    with TIMELINE_CSV.open("w", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "id",
                "date",
                "year",
                "phase",
                "title",
                "author",
                "recipient",
                "location",
                "source_class",
                "relationship_mode",
                "frederick_role",
            ],
        )
        writer.writeheader()
        for row in records:
            writer.writerow(
                {
                    "id": row["id"],
                    "date": row["date"],
                    "year": row["year"],
                    "phase": row["phase"],
                    "title": row["title"],
                    "author": row["author"],
                    "recipient": row["recipient"],
                    "location": row["location"],
                    "source_class": row["source_class"],
                    "relationship_mode": row["relationship_mode"],
                    "frederick_role": row["frederick_role"] or "",
                }
            )

    theme_stats = compute_theme_stats(records, lexicons=LEXICONS, include_summary=True)
    relationship_counts = Counter()
    phase_counts = Counter()
    phase_mode_counts = defaultdict(Counter)
    source_counts = Counter()
    frederick_records = []
    frederick_primary_records = []
    frederick_local_records = []
    frederick_phase_counts = Counter()
    frederick_roles = Counter()
    edge_weights = Counter()
    node_weights = Counter()
    primary_edge_weights = Counter()
    primary_node_weights = Counter()

    for row in records:
        phase_counts[row["phase"]] += 1
        relationship_counts[row["relationship_mode"]] += 1
        phase_mode_counts[row["phase"]][row["relationship_mode"]] += 1
        source_counts[row["source_class"]] += 1

        if row["frederick_role"]:
            frederick_records.append(row)
            if row["source_class"] == "primary":
                frederick_primary_records.append(row)
            if row["source_class"] == "local":
                frederick_local_records.append(row)
            frederick_phase_counts[row["phase"]] += 1
            frederick_roles[row["frederick_role"]] += 1

        for left, right in row["connections"]:
            a, b = sorted((left, right))
            edge_weights[(a, b)] += 1
            node_weights[left] += 1
            node_weights[right] += 1
            if row["source_class"] == "primary":
                primary_edge_weights[(a, b)] += 1
                primary_node_weights[left] += 1
                primary_node_weights[right] += 1

    with THEME_CSV.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["author", "warmth", "utility", "defense", "total"])
        writer.writeheader()
        for author, counts in theme_stats.items():
            row = {
                "author": author,
                "warmth": counts["warmth"],
                "utility": counts["utility"],
                "defense": counts["defense"],
                "total": counts["warmth"] + counts["utility"] + counts["defense"],
            }
            writer.writerow(row)

    with EDGE_CSV.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["source", "target", "weight"])
        writer.writeheader()
        for (source, target), weight in sorted(edge_weights.items()):
            writer.writerow({"source": source, "target": target, "weight": weight})

    direct_jefferson_records = [
        row
        for row in records
        if {row["author"], row["recipient"]} == {"James Wilkinson", "Thomas Jefferson"}
    ]

    summary = {
        "total_records": len(records),
        "direct_jefferson_wilkinson_records": len(direct_jefferson_records),
        "frederick_records": len(frederick_records),
        "frederick_share": round(len(frederick_records) / len(records), 3),
        "frederick_primary_records": len(frederick_primary_records),
        "frederick_local_records": len(frederick_local_records),
        "frederick_phase_counts": dict(frederick_phase_counts),
        "frederick_roles": dict(frederick_roles),
        "phase_counts": dict(phase_counts),
        "phase_mode_counts": {
            phase: dict(counts)
            for phase, counts in phase_mode_counts.items()
        },
        "relationship_counts": dict(relationship_counts),
        "source_counts": dict(source_counts),
        "theme_counts": theme_stats,
        "top_nodes": [
            {"node": node, "weight": weight}
            for node, weight in node_weights.most_common(8)
        ],
        "top_edges": [
            {"source": source, "target": target, "weight": weight}
            for (source, target), weight in edge_weights.most_common(10)
        ],
        "primary_only_top_nodes": [
            {"node": node, "weight": weight}
            for node, weight in primary_node_weights.most_common(8)
        ],
        "primary_only_top_edges": [
            {"source": source, "target": target, "weight": weight}
            for (source, target), weight in primary_edge_weights.most_common(10)
        ],
        "place_node_weights": [
            {
                "node": node,
                "overall_weight": node_weights.get(node, 0),
                "primary_only_weight": primary_node_weights.get(node, 0),
            }
            for node in PLACE_NODES
        ],
        "core_claim_metrics": {
            "instrumental_plus_protective_modes": sum(
                relationship_counts[mode] for mode in NON_SOCIAL_MODES
            ),
            "social_access_modes": relationship_counts["social_access"],
            "retrospective_esteem_modes": relationship_counts["retrospective_esteem"],
            "frederick_rehabilitation_records": frederick_phase_counts["rehabilitation"],
        },
        "evidence_tiers": {
            "direct_relationship_primary": len(direct_jefferson_records),
            "primary_frederick_venue": len(frederick_primary_records),
            "contextual_frederick_local": len(frederick_local_records),
            "frederick_primary_share": round(
                len(frederick_primary_records) / len(frederick_records), 3
            )
            if frederick_records
            else 0.0,
        },
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2))

    inventory = []
    traceability = []
    for row in records:
        inventory.append(
            {
                "id": row["id"],
                "date": row["date"],
                "title": row["title"],
                "author": row["author"],
                "recipient": row["recipient"],
                "location": row["location"],
                "phase": row["phase"],
                "source_class": row["source_class"],
                "relationship_mode": row["relationship_mode"],
                "frederick_role": row["frederick_role"],
                "source_url": row["source_url"],
                "repository_identifier": repository_identifier(row["source_url"]),
            }
        )
        traceability.append(
            {
                **inventory[-1],
                "survival_modes": row["survival_modes"],
                "excerpt": row["excerpt"],
                "summary": row["summary"],
                "local_relevance": row["local_relevance"],
                "connections": row["connections"],
            }
        )

    INVENTORY_JSON.write_text(json.dumps({"records": inventory}, indent=2))
    TRACEABILITY_JSON.write_text(json.dumps({"records": traceability}, indent=2))

    excerpt_only_theme_stats = compute_theme_stats(records, lexicons=LEXICONS, include_summary=False)
    conservative_theme_stats = compute_theme_stats(records, lexicons=CONSERVATIVE_LEXICONS, include_summary=False)
    place_weights = place_weights_for_records(records)
    primary_place_weights = place_weights_for_records(records, primary_only=True)
    frederick_top_count = 0
    for idx in range(len(records)):
        subset = records[:idx] + records[idx + 1 :]
        subset_weights = place_weights_for_records(subset)
        leader = max(PLACE_NODES, key=lambda node: (subset_weights[node], node))
        if leader == "Frederick Town":
            frederick_top_count += 1

    sensitivity = {
        "theme_excerpt_only": excerpt_only_theme_stats,
        "theme_conservative_excerpt_only": conservative_theme_stats,
        "place_weights_full": place_weights,
        "place_weights_primary_only": primary_place_weights,
        "leave_one_out_place_rank": {
            "runs": len(records),
            "frederick_town_ranked_top_every_time": frederick_top_count == len(records),
            "frederick_town_top_count": frederick_top_count,
        },
        "note": "These are descriptive perturbation checks only. They do not replace independent coding or larger archival recovery.",
    }
    SENSITIVITY_JSON.write_text(json.dumps(sensitivity, indent=2))

    environment = {
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "latexmk_version": latexmk_version(),
    }
    ENVIRONMENT_JSON.write_text(json.dumps(environment, indent=2))


if __name__ == "__main__":
    main()
