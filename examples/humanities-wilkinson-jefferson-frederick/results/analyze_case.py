#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "curated_corpus.json"

TIMELINE_CSV = ROOT / "results" / "event_timeline.csv"
THEME_CSV = ROOT / "results" / "theme_counts.csv"
EDGE_CSV = ROOT / "results" / "network_edges.csv"
SUMMARY_JSON = ROOT / "results" / "summary_metrics.json"


LEXICONS = {
    "warmth": {"esteem", "respect", "attachment", "friend", "friendly", "sympathy", "regard", "wishes"},
    "utility": {"service", "services", "public", "conduct", "duty", "duties", "orders", "direction", "country"},
    "defense": {"honor", "calumny", "calumnies", "persecution", "persecutions", "trial", "fair", "vindication", "confidence", "support"},
}


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z]+", text.lower())


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

    author_buckets = {"James Wilkinson": Counter(), "Thomas Jefferson": Counter()}
    relationship_counts = Counter()
    phase_counts = Counter()
    source_counts = Counter()
    frederick_records = []
    frederick_phase_counts = Counter()
    frederick_roles = Counter()
    edge_weights = Counter()
    node_weights = Counter()

    for row in records:
        phase_counts[row["phase"]] += 1
        relationship_counts[row["relationship_mode"]] += 1
        source_counts[row["source_class"]] += 1

        if row["frederick_role"]:
            frederick_records.append(row)
            frederick_phase_counts[row["phase"]] += 1
            frederick_roles[row["frederick_role"]] += 1

        text = f'{row["excerpt"]} {row["summary"]}'
        tokens = tokenize(text)
        author = row["author"]
        if author in author_buckets:
            for category, words in LEXICONS.items():
                author_buckets[author][category] += sum(1 for token in tokens if token in words)

        for left, right in row["connections"]:
            a, b = sorted((left, right))
            edge_weights[(a, b)] += 1
            node_weights[left] += 1
            node_weights[right] += 1

    with THEME_CSV.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["author", "warmth", "utility", "defense", "total"])
        writer.writeheader()
        for author, counts in author_buckets.items():
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
        "frederick_phase_counts": dict(frederick_phase_counts),
        "frederick_roles": dict(frederick_roles),
        "phase_counts": dict(phase_counts),
        "relationship_counts": dict(relationship_counts),
        "source_counts": dict(source_counts),
        "theme_counts": {
            author: {
                "warmth": counts["warmth"],
                "utility": counts["utility"],
                "defense": counts["defense"],
            }
            for author, counts in author_buckets.items()
        },
        "top_nodes": [
            {"node": node, "weight": weight}
            for node, weight in node_weights.most_common(8)
        ],
        "top_edges": [
            {"source": source, "target": target, "weight": weight}
            for (source, target), weight in edge_weights.most_common(10)
        ],
        "core_claim_metrics": {
            "instrumental_plus_protective_modes": relationship_counts["instrumental"]
            + relationship_counts["protective"]
            + relationship_counts["self_vindication"]
            + relationship_counts["official_settlement"],
            "social_access_modes": relationship_counts["social_access"],
            "retrospective_esteem_modes": relationship_counts["retrospective_esteem"],
            "frederick_rehabilitation_records": frederick_phase_counts["rehabilitation"],
        },
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
