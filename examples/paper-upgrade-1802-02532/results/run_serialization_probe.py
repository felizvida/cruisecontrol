#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import random
from itertools import product
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT.parent / "data"

GRID_SIZE = 16
NUM_SAMPLES = 240
SEED_BASE = 1000
ADJ_THRESHOLDS = [4, 8, 16, 32, 64, 128, 256]
CONTEXT_BUDGETS = [64, 128, 256, 512, 1024]
ORDERING_LABELS = {
    "hilbert": "Hilbert",
    "morton": "Morton",
    "raster": "Raster",
    "random": "Random",
}
N6_FORWARD = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
N26 = [(dx, dy, dz) for dx, dy, dz in product((-1, 0, 1), repeat=3) if (dx, dy, dz) != (0, 0, 0)]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def transpose_to_axes(x: list[int], dims: int, bits: int) -> list[int]:
    axes = list(x)
    limit = 2 << (bits - 1)
    tail = axes[dims - 1] >> 1
    for idx in range(dims - 1, 0, -1):
        axes[idx] ^= axes[idx - 1]
    axes[0] ^= tail

    q = 2
    while q != limit:
        p = q - 1
        for idx in range(dims - 1, -1, -1):
            if axes[idx] & q:
                axes[0] ^= p
            else:
                delta = (axes[0] ^ axes[idx]) & p
                axes[0] ^= delta
                axes[idx] ^= delta
        q <<= 1
    return axes


def hilbert_point(distance: int, dims: int, bits: int) -> tuple[int, ...]:
    axes = [0] * dims
    for bit_idx in range(bits):
        for dim_idx in range(dims):
            bit = (distance >> (bit_idx * dims + (dims - dim_idx - 1))) & 1
            axes[dim_idx] |= bit << bit_idx
    return tuple(transpose_to_axes(axes, dims, bits))


def build_orderings() -> dict[str, dict[tuple[int, int, int], int]]:
    total_points = GRID_SIZE ** 3
    orderings: dict[str, dict[tuple[int, int, int], int]] = {}

    hilbert = [hilbert_point(distance, 3, 4) for distance in range(total_points)]
    orderings["hilbert"] = {point: idx for idx, point in enumerate(hilbert)}

    morton_pairs: list[tuple[tuple[int, int, int], int]] = []
    for x, y, z in product(range(GRID_SIZE), repeat=3):
        code = 0
        for bit in range(4):
            code |= ((x >> bit) & 1) << (3 * bit + 2)
            code |= ((y >> bit) & 1) << (3 * bit + 1)
            code |= ((z >> bit) & 1) << (3 * bit)
        morton_pairs.append(((x, y, z), code))
    morton_pairs.sort(key=lambda item: item[1])
    orderings["morton"] = {point: idx for idx, (point, _) in enumerate(morton_pairs)}

    orderings["raster"] = {
        (x, y, z): ((x * GRID_SIZE) + y) * GRID_SIZE + z for x, y, z in product(range(GRID_SIZE), repeat=3)
    }

    random_points = [(x, y, z) for x, y, z in product(range(GRID_SIZE), repeat=3)]
    random.Random(7).shuffle(random_points)
    orderings["random"] = {point: idx for idx, point in enumerate(random_points)}
    return orderings


def add_walk(
    occupied: dict[tuple[int, int, int], int],
    length: int,
    start: tuple[int, int, int],
    dirs: list[int],
    token_cycle: list[int],
) -> None:
    position = list(start)
    for step in range(length):
        occupied[tuple(position)] = token_cycle[step % len(token_cycle)]
        axis = dirs[step % len(dirs)]
        position[axis] += 1
        if position[axis] >= GRID_SIZE - 1:
            position[axis] = 1


def make_sample(seed: int) -> dict[tuple[int, int, int], int]:
    rng = random.Random(seed)
    occupied: dict[tuple[int, int, int], int] = {}

    for _ in range(3):
        start = (rng.randrange(2, 10), rng.randrange(2, 10), rng.randrange(2, 10))
        dirs = list(rng.sample([0, 1, 2], 3))
        add_walk(occupied, rng.randrange(12, 18), start, dirs, [1, 2, 3, 2])

    for _ in range(2):
        anchor = (rng.randrange(2, 12), rng.randrange(2, 12), rng.randrange(2, 12))
        for dx, dy, dz in product(range(3), repeat=3):
            if rng.random() < 0.78:
                token = 2 if dz == 1 else 3
                occupied[(anchor[0] + dx, anchor[1] + dy, anchor[2] + dz)] = token

    for _ in range(25):
        point = (rng.randrange(1, GRID_SIZE - 1), rng.randrange(1, GRID_SIZE - 1), rng.randrange(1, GRID_SIZE - 1))
        occupied[point] = rng.choice([1, 2, 3])

    return occupied


def support_radius(
    point: tuple[int, int, int], occupied: dict[tuple[int, int, int], int], index_map: dict[tuple[int, int, int], int]
) -> int | None:
    center = index_map[point]
    buckets = {1: [], 2: [], 3: []}
    for dx, dy, dz in N26:
        neighbor = (point[0] + dx, point[1] + dy, point[2] + dz)
        token = occupied.get(neighbor)
        if token:
            buckets[token].append(abs(index_map[neighbor] - center))

    if len(buckets[1]) < 1 or len(buckets[2]) < 2 or len(buckets[3]) < 2:
        return None

    buckets[1].sort()
    buckets[2].sort()
    buckets[3].sort()
    return max(buckets[1][0], buckets[2][1], buckets[3][1])


def round_value(value: float) -> float:
    return round(value, 4)


def summarize_ordering(
    samples: list[dict[tuple[int, int, int], int]], ordering_key: str, index_map: dict[tuple[int, int, int], int]
) -> tuple[dict[str, object], list[dict[str, object]], list[dict[str, object]]]:
    adjacency_spans: list[int] = []
    support_radii: list[int] = []

    for occupied in samples:
        for point in occupied:
            for dx, dy, dz in N6_FORWARD:
                neighbor = (point[0] + dx, point[1] + dy, point[2] + dz)
                if neighbor in occupied:
                    adjacency_spans.append(abs(index_map[neighbor] - index_map[point]))

            radius = support_radius(point, occupied, index_map)
            if radius is not None:
                support_radii.append(radius)

    adjacency_spans.sort()
    support_radii.sort()

    adjacency_curve = []
    for threshold in ADJ_THRESHOLDS:
        retention = sum(span <= threshold for span in adjacency_spans) / len(adjacency_spans)
        adjacency_curve.append({"ordering": ordering_key, "threshold": threshold, "retention": round_value(retention)})

    context_curve = []
    for budget in CONTEXT_BUDGETS:
        recovery = sum(radius <= budget for radius in support_radii) / len(support_radii)
        context_curve.append({"ordering": ordering_key, "budget": budget, "recoverability": round_value(recovery)})

    summary = {
        "ordering": ordering_key,
        "label": ORDERING_LABELS[ordering_key],
        "adjacency": {
            "pair_count": len(adjacency_spans),
            "mean_span": round_value(mean(adjacency_spans)),
            "median_span": adjacency_spans[len(adjacency_spans) // 2],
            "p90_span": adjacency_spans[int(0.9 * len(adjacency_spans))],
            "retention": adjacency_curve,
        },
        "support_recovery": {
            "positive_count": len(support_radii),
            "median_radius": support_radii[len(support_radii) // 2],
            "p90_radius": support_radii[int(0.9 * len(support_radii))],
            "recoverability": context_curve,
        },
    }
    return summary, adjacency_curve, context_curve


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def export_corpus(samples: list[dict[tuple[int, int, int], int]]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    corpus_path = DATA_DIR / "synthetic_microenvironment_corpus.jsonl"
    with corpus_path.open("w") as handle:
        for sample_idx, occupied in enumerate(samples):
            payload = {
                "sample_id": sample_idx,
                "seed": SEED_BASE + sample_idx,
                "grid_size": GRID_SIZE,
                "occupied_voxels": [
                    {"x": x, "y": y, "z": z, "token": token}
                    for (x, y, z), token in sorted(occupied.items(), key=lambda item: item[0])
                ],
            }
            handle.write(json.dumps(payload, sort_keys=True))
            handle.write("\n")


def main() -> None:
    samples = [make_sample(SEED_BASE + idx) for idx in range(NUM_SAMPLES)]
    orderings = build_orderings()

    summaries = []
    adjacency_rows: list[dict[str, object]] = []
    context_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []

    for ordering_key, index_map in orderings.items():
        summary, adjacency_curve, context_curve = summarize_ordering(samples, ordering_key, index_map)
        summaries.append(summary)
        adjacency_rows.extend(adjacency_curve)
        context_rows.extend(context_curve)
        summary_rows.append(
            {
                "ordering": summary["label"],
                "adj_mean_span": summary["adjacency"]["mean_span"],
                "adj_median_span": summary["adjacency"]["median_span"],
                "adj_p90_span": summary["adjacency"]["p90_span"],
                "adj_retention_le_8": next(item["retention"] for item in summary["adjacency"]["retention"] if item["threshold"] == 8),
                "adj_retention_le_16": next(item["retention"] for item in summary["adjacency"]["retention"] if item["threshold"] == 16),
                "adj_retention_le_32": next(item["retention"] for item in summary["adjacency"]["retention"] if item["threshold"] == 32),
                "support_median_radius": summary["support_recovery"]["median_radius"],
                "support_p90_radius": summary["support_recovery"]["p90_radius"],
                "recoverability_le_128": next(
                    item["recoverability"] for item in summary["support_recovery"]["recoverability"] if item["budget"] == 128
                ),
                "recoverability_le_256": next(
                    item["recoverability"] for item in summary["support_recovery"]["recoverability"] if item["budget"] == 256
                ),
                "recoverability_le_512": next(
                    item["recoverability"] for item in summary["support_recovery"]["recoverability"] if item["budget"] == 512
                ),
            }
        )

    export_corpus(samples)

    dataset = {
        "name": "synthetic_microenvironment_probe",
        "description": (
            "Deterministic 16^3 voxel microenvironments combining backbone-like walks, dense pocket patches, and distractor voxels "
            "with three semantic channels. The probe tests how serialization affects local-neighborhood exposure under sequence budgets."
        ),
        "grid_size": GRID_SIZE,
        "num_samples": NUM_SAMPLES,
        "seed_base": SEED_BASE,
        "average_occupied_voxels": round_value(mean(len(sample) for sample in samples)),
        "channels": {
            "1": "backbone-like support voxel",
            "2": "polar / pocket core voxel",
            "3": "hydrophobic / shell voxel",
        },
        "positive_support_rule": "At least one channel-1 neighbor, two channel-2 neighbors, and two channel-3 neighbors inside a 26-neighborhood.",
    }

    summary_path = ROOT / "serialization_probe.json"
    summary_path.write_text(json.dumps({"dataset": dataset, "orderings": summaries}, indent=2))

    write_csv(ROOT / "locality_curve.csv", ["ordering", "threshold", "retention"], adjacency_rows)
    write_csv(ROOT / "context_budget_curve.csv", ["ordering", "budget", "recoverability"], context_rows)
    write_csv(
        ROOT / "ordering_summary.csv",
        [
            "ordering",
            "adj_mean_span",
            "adj_median_span",
            "adj_p90_span",
            "adj_retention_le_8",
            "adj_retention_le_16",
            "adj_retention_le_32",
            "support_median_radius",
            "support_p90_radius",
            "recoverability_le_128",
            "recoverability_le_256",
            "recoverability_le_512",
        ],
        summary_rows,
    )

    print(f"Wrote {summary_path}")
    print(f"Wrote {ROOT / 'locality_curve.csv'}")
    print(f"Wrote {ROOT / 'context_budget_curve.csv'}")
    print(f"Wrote {ROOT / 'ordering_summary.csv'}")
    print(f"Wrote {DATA_DIR / 'synthetic_microenvironment_corpus.jsonl'}")


if __name__ == "__main__":
    main()
