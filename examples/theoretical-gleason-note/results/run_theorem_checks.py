#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DIMENSIONS = [2, 3, 4]
TRIALS_PER_DIM = 250
EFFECT_CHECKS_PER_TRIAL = 12
SPHERE_TRIPLES = 1500
SEED = 20260323


Matrix = list[list[float]]


def zeros(n: int) -> Matrix:
    return [[0.0 for _ in range(n)] for _ in range(n)]


def identity(n: int) -> Matrix:
    out = zeros(n)
    for idx in range(n):
        out[idx][idx] = 1.0
    return out


def transpose(a: Matrix) -> Matrix:
    return [list(row) for row in zip(*a)]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    rows = len(a)
    cols = len(b[0])
    inner = len(b)
    out = zeros(rows)
    for i in range(rows):
        for j in range(cols):
            out[i][j] = sum(a[i][k] * b[k][j] for k in range(inner))
    return out


def add(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    return [[a[i][j] + b[i][j] for j in range(n)] for i in range(n)]


def sub(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    return [[a[i][j] - b[i][j] for j in range(n)] for i in range(n)]


def scale(c: float, a: Matrix) -> Matrix:
    n = len(a)
    return [[c * a[i][j] for j in range(n)] for i in range(n)]


def trace(a: Matrix) -> float:
    return sum(a[i][i] for i in range(len(a)))


def dot(x: list[float], y: list[float]) -> float:
    return sum(a * b for a, b in zip(x, y))


def frobenius_max_abs(a: Matrix) -> float:
    return max(abs(entry) for row in a for entry in row)


def random_matrix(n: int, rng: random.Random) -> Matrix:
    return [[rng.uniform(-1.0, 1.0) for _ in range(n)] for _ in range(n)]


def random_psd(n: int, rng: random.Random) -> Matrix:
    raw = random_matrix(n, rng)
    return matmul(transpose(raw), raw)


def random_density(n: int, rng: random.Random) -> Matrix:
    psd = random_psd(n, rng)
    return scale(1.0 / trace(psd), psd)


def random_effect(n: int, rng: random.Random) -> Matrix:
    psd = random_psd(n, rng)
    return scale(0.85 / trace(psd), psd)


def random_effect_pair(n: int, rng: random.Random) -> tuple[Matrix, Matrix]:
    a = random_psd(n, rng)
    b = random_psd(n, rng)
    total = trace(add(a, b))
    factor = 0.85 / total
    return scale(factor, a), scale(factor, b)


def projector(n: int, idx: int) -> Matrix:
    out = zeros(n)
    out[idx][idx] = 1.0
    return out


def sum_effect(n: int, i: int, j: int) -> Matrix:
    out = zeros(n)
    out[i][i] = 0.5
    out[j][j] = 0.5
    out[i][j] = 0.5
    out[j][i] = 0.5
    return out


def effect_value(rho: Matrix, eff: Matrix) -> float:
    return trace(matmul(rho, eff))


def reconstruct_rho(rho: Matrix) -> Matrix:
    n = len(rho)
    out = zeros(n)
    diag_values = [effect_value(rho, projector(n, i)) for i in range(n)]
    for i in range(n):
        out[i][i] = diag_values[i]
    for i in range(n):
        for j in range(i + 1, n):
            sij = effect_value(rho, sum_effect(n, i, j))
            entry = sij - 0.5 * diag_values[i] - 0.5 * diag_values[j]
            out[i][j] = entry
            out[j][i] = entry
    return out


def orthonormal_triple(rng: random.Random) -> list[list[float]]:
    basis: list[list[float]] = []
    while len(basis) < 3:
        vec = [rng.uniform(-1.0, 1.0) for _ in range(3)]
        for prev in basis:
            proj = dot(vec, prev)
            vec = [v - proj * p for v, p in zip(vec, prev)]
        norm = math.sqrt(dot(vec, vec))
        if norm < 1e-8:
            continue
        basis.append([v / norm for v in vec])
    return basis


def g_beta_alpha(zsq: float, beta: float) -> float:
    alpha = 1.0 - 3.0 * beta
    return beta + alpha * zsq


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rng = random.Random(SEED)

    rows: list[dict[str, object]] = []
    summaries: list[dict[str, object]] = []

    for dim in DIMENSIONS:
        max_reconstruction = 0.0
        max_representation = 0.0
        max_additivity = 0.0
        sample_record: dict[str, object] | None = None

        for trial in range(TRIALS_PER_DIM):
            rho = random_density(dim, rng)
            recovered = reconstruct_rho(rho)
            reconstruction_error = frobenius_max_abs(sub(rho, recovered))
            max_reconstruction = max(max_reconstruction, reconstruction_error)

            max_trial_rep = 0.0
            max_trial_add = 0.0
            for _ in range(EFFECT_CHECKS_PER_TRIAL):
                eff = random_effect(dim, rng)
                residual = abs(effect_value(rho, eff) - effect_value(recovered, eff))
                max_trial_rep = max(max_trial_rep, residual)

                eff_a, eff_b = random_effect_pair(dim, rng)
                additivity = abs(
                    effect_value(rho, add(eff_a, eff_b))
                    - effect_value(rho, eff_a)
                    - effect_value(rho, eff_b)
                )
                max_trial_add = max(max_trial_add, additivity)

            max_representation = max(max_representation, max_trial_rep)
            max_additivity = max(max_additivity, max_trial_add)

            if sample_record is None:
                sample_record = {
                    "dimension": dim,
                    "rho": rho,
                    "recovered_rho": recovered,
                    "reconstruction_error": reconstruction_error,
                    "max_representation_residual": max_trial_rep,
                    "max_additivity_residual": max_trial_add,
                }

        rows.append(
            {
                "dimension": dim,
                "trials": TRIALS_PER_DIM,
                "effects_per_trial": EFFECT_CHECKS_PER_TRIAL,
                "max_reconstruction_error": f"{max_reconstruction:.3e}",
                "max_representation_residual": f"{max_representation:.3e}",
                "max_additivity_residual": f"{max_additivity:.3e}",
            }
        )
        summaries.append(
            {
                "dimension": dim,
                "max_reconstruction_error": max_reconstruction,
                "max_representation_residual": max_representation,
                "max_additivity_residual": max_additivity,
                "sample": sample_record,
            }
        )

    sphere_checks: list[dict[str, object]] = []
    max_sphere_residual = 0.0
    beta = 0.22
    for triple_idx in range(SPHERE_TRIPLES):
        triple = orthonormal_triple(rng)
        heights = [vec[2] ** 2 for vec in triple]
        total = sum(g_beta_alpha(height, beta) for height in heights)
        residual = abs(total - 1.0)
        max_sphere_residual = max(max_sphere_residual, residual)
        if triple_idx < 3:
            sphere_checks.append(
                {
                    "heights_squared": heights,
                    "value_sum": total,
                    "residual": residual,
                }
            )

    payload = {
        "seed": SEED,
        "matrix_checks": {
            "dimensions": summaries,
            "trials_per_dimension": TRIALS_PER_DIM,
            "effects_per_trial": EFFECT_CHECKS_PER_TRIAL,
        },
        "sphere_warmup": {
            "beta": beta,
            "alpha": 1.0 - 3.0 * beta,
            "triple_count": SPHERE_TRIPLES,
            "max_residual": max_sphere_residual,
            "sample_triples": sphere_checks,
        },
    }

    (ROOT / "reconstruction_checks.json").write_text(json.dumps(payload, indent=2))
    write_csv(ROOT / "check_summary.csv", rows)

    print(f"Wrote {ROOT / 'reconstruction_checks.json'}")
    print(f"Wrote {ROOT / 'check_summary.csv'}")


if __name__ == "__main__":
    main()
