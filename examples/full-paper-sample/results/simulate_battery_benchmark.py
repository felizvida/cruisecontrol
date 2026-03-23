#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Regime:
    name: str
    shift_family: str
    battery_state: str
    battery_pct: int
    base_shift: float
    variability: float
    shock_prob: float
    shock_scale: float
    drift: float


REGIMES = [
    Regime(
        name="Terrain shift, 25% battery",
        shift_family="terrain",
        battery_state="low",
        battery_pct=25,
        base_shift=0.92,
        variability=0.22,
        shock_prob=0.16,
        shock_scale=0.42,
        drift=0.72,
    ),
    Regime(
        name="Terrain shift, 80% battery",
        shift_family="terrain",
        battery_state="high",
        battery_pct=80,
        base_shift=0.92,
        variability=0.22,
        shock_prob=0.16,
        shock_scale=0.42,
        drift=0.72,
    ),
    Regime(
        name="Payload shift, 25% battery",
        shift_family="payload",
        battery_state="low",
        battery_pct=25,
        base_shift=0.74,
        variability=0.13,
        shock_prob=0.08,
        shock_scale=0.18,
        drift=0.88,
    ),
    Regime(
        name="Payload shift, 80% battery",
        shift_family="payload",
        battery_state="high",
        battery_pct=80,
        base_shift=0.74,
        variability=0.13,
        shock_prob=0.08,
        shock_scale=0.18,
        drift=0.88,
    ),
]


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def sigmoid(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def adaptation_lambda(battery_frac: float) -> float:
    return 0.50 + 2.40 * (1.0 - battery_frac) ** 2


def step_shift(regime: Regime, rng: random.Random, shift: float, shock: float) -> tuple[float, float]:
    if regime.shift_family == "terrain":
        if rng.random() < regime.shock_prob:
            shock += abs(rng.gauss(regime.shock_scale, regime.shock_scale * 0.35))
        target = regime.base_shift + shock + rng.gauss(0.0, regime.variability)
        shift = regime.drift * shift + (1.0 - regime.drift) * target
        shock *= 0.58
    else:
        if rng.random() < regime.shock_prob:
            shock += abs(rng.gauss(regime.shock_scale, regime.shock_scale * 0.25))
        target = regime.base_shift + 0.55 * shock + rng.gauss(0.0, regime.variability)
        shift = regime.drift * shift + (1.0 - regime.drift) * target
        shock *= 0.82
    return clamp(shift, 0.0, 2.0), shock


def choose_action(
    policy: str,
    step_idx: int,
    obs_mismatch: float,
    battery_frac: float,
    cost_scale: float,
    tau: float,
    periodic_interval: int,
) -> bool:
    expected_cost = cost_scale * (0.014 + 0.010 * obs_mismatch)
    gain = max(0.0, 0.150 * obs_mismatch - 0.014)
    if policy == "Static":
        return False
    if policy == "Periodic":
        return step_idx % periodic_interval == 0
    if policy == "Always-on":
        return True
    if policy == "Battery-gated":
        return gain - adaptation_lambda(battery_frac) * expected_cost > tau
    if policy == "No battery-state input":
        return gain - 0.95 * expected_cost > tau
    if policy == "No compute-cost penalty":
        return gain > tau
    if policy == "Slip-threshold heuristic":
        return obs_mismatch > 0.42
    raise ValueError(f"unknown policy {policy}")


def simulate_episode(
    regime: Regime,
    policy: str,
    rng: random.Random,
    *,
    tau: float,
    cost_scale: float = 1.0,
    periodic_interval: int = 4,
    steps: int = 52,
) -> dict[str, float]:
    battery_capacity_wh = 17.0
    battery_wh = battery_capacity_wh * (regime.battery_pct / 100.0)
    shift = regime.base_shift + rng.gauss(0.0, regime.variability * 0.5)
    shock = 0.0
    estimate = 0.0

    total_distance = 0.0
    locomotion_wh = 0.0
    compute_wh = 0.0
    falls = 0
    adapt_calls = 0
    reward = 0.0
    completed_steps = 0

    for step_idx in range(steps):
        battery_frac = clamp(battery_wh / battery_capacity_wh, 0.0, 1.0)
        low_battery_penalty = max(0.0, 0.38 - battery_frac)
        shift, shock = step_shift(regime, rng, shift, shock)
        observation = shift + rng.gauss(0.0, 0.09 if regime.shift_family == "terrain" else 0.06)
        obs_mismatch = abs(observation - estimate)

        adapt = choose_action(
            policy,
            step_idx,
            obs_mismatch,
            battery_frac,
            cost_scale,
            tau,
            periodic_interval,
        )

        adapt_energy = 0.0
        adaptation_latency = 0.0
        if adapt:
            alpha = 0.68 if regime.shift_family == "terrain" else 0.61
            estimate = estimate + alpha * (observation - estimate)
            adapt_energy = cost_scale * (0.014 + 0.010 * obs_mismatch)
            compute_wh += adapt_energy
            adapt_calls += 1
            adaptation_latency = 0.014 + 0.060 * low_battery_penalty + 0.010 * (cost_scale - 1.0)
        else:
            estimate *= 0.992

        mismatch = abs(shift - estimate)
        fall_logit = -2.9 + 4.8 * (mismatch - 0.36) + 3.2 * low_battery_penalty
        if regime.shift_family == "terrain":
            fall_logit += 0.25
        fall_logit += 1.1 * adaptation_latency
        fall_prob = sigmoid(fall_logit)
        fell = rng.random() < fall_prob

        stability = clamp(
            1.02 - 0.46 * mismatch - 0.22 * low_battery_penalty - 0.85 * adaptation_latency,
            0.22,
            1.0,
        )
        step_distance = 6.35 * (0.22 if fell else stability)
        move_wh = (
            0.115
            + 0.026 * shift
            + 0.048 * mismatch
            + 0.055 * adaptation_latency
            + (0.065 if fell else 0.0)
        )

        total_distance += step_distance
        locomotion_wh += move_wh
        battery_wh -= move_wh + adapt_energy
        completed_steps += 1
        if fell:
            falls += 1

        reward += (
            0.72 * (step_distance / 6.35)
            - 0.58 * (1.0 if fell else 0.0)
            - 0.10 * adapt_energy
        )

        if battery_wh <= 0.0:
            break

    normalized_progress = total_distance / (steps * 6.35)
    completion_bonus = completed_steps / steps
    fall_rate = falls / max(total_distance / 100.0, 1e-6)
    mission_return = clamp(
        0.58 * normalized_progress
        + 0.24 * completion_bonus
        + 0.22 * max(0.0, 1.0 - 0.65 * fall_rate)
        + 0.06 * (reward / max(completed_steps, 1)),
        0.0,
        1.0,
    )
    cost_of_transport = clamp(
        ((locomotion_wh + 0.8 * compute_wh) * 6.0) / max(total_distance, 1e-6),
        0.18,
        2.2,
    )

    return {
        "mission_return": mission_return,
        "distance_m": total_distance,
        "cost_of_transport": cost_of_transport,
        "falls_per_100m": fall_rate,
        "adapt_calls": adapt_calls,
        "compute_wh": compute_wh,
    }


def aggregate_metrics(rows: list[dict[str, float]]) -> dict[str, float]:
    return {
        "mission_return": mean(row["mission_return"] for row in rows),
        "distance_m": mean(row["distance_m"] for row in rows),
        "cost_of_transport": mean(row["cost_of_transport"] for row in rows),
        "falls_per_100m": mean(row["falls_per_100m"] for row in rows),
        "adapt_calls": mean(row["adapt_calls"] for row in rows),
        "compute_wh": mean(row["compute_wh"] for row in rows),
    }


def tune_tau(seed: int, episodes: int) -> dict[str, float]:
    candidates = [round(-0.030 + x * 0.0025, 4) for x in range(0, 33)]
    best_tau = 0.0
    best_score = -1e9
    for tau in candidates:
        scores = []
        for regime_idx, regime in enumerate(REGIMES):
            for episode_idx in range(episodes):
                rng = random.Random(seed + 10000 * regime_idx + episode_idx)
                row = simulate_episode(regime, "Battery-gated", rng, tau=tau)
                penalty = 0.14 if regime.battery_state == "low" else 0.04
                scores.append(row["mission_return"] - penalty * row["compute_wh"])
        score = mean(scores)
        if score > best_score:
            best_tau = tau
            best_score = score
    return {"tau": best_tau, "objective": best_score}


def round_row(row: dict[str, float]) -> dict[str, float]:
    return {
        "mission_return": round(row["mission_return"], 2),
        "distance_m": int(round(row["distance_m"])),
        "cost_of_transport": round(row["cost_of_transport"], 2),
        "falls_per_100m": round(row["falls_per_100m"], 2),
        "adapt_calls": int(round(row["adapt_calls"])),
        "compute_wh": round(row["compute_wh"], 2),
    }


def write_episode_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fieldnames = [
        "regime",
        "shift_family",
        "battery_state",
        "battery_pct",
        "policy",
        "episode_idx",
        "mission_return",
        "distance_m",
        "cost_of_transport",
        "falls_per_100m",
        "adapt_calls",
        "compute_wh",
    ]
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=1024)
    parser.add_argument("--tune-episodes", type=int, default=256)
    parser.add_argument("--seed", type=int, default=20260323)
    args = parser.parse_args()

    tune = tune_tau(args.seed, args.tune_episodes)
    tau = tune["tau"]

    policies = ["Static", "Periodic", "Always-on", "Battery-gated"]
    raw_rows: list[dict[str, object]] = []
    regimes_out = []

    for regime_idx, regime in enumerate(REGIMES):
        methods = []
        for policy_idx, policy in enumerate(policies):
            rows = []
            for episode_idx in range(args.episodes):
                rng = random.Random(args.seed + 100000 * regime_idx + 1000 * policy_idx + episode_idx)
                row = simulate_episode(regime, policy, rng, tau=tau)
                rows.append(row)
                raw_rows.append(
                    {
                        "regime": regime.name,
                        "shift_family": regime.shift_family,
                        "battery_state": regime.battery_state,
                        "battery_pct": regime.battery_pct,
                        "policy": policy,
                        "episode_idx": episode_idx,
                        **row,
                    }
                )
            methods.append({"name": policy, **round_row(aggregate_metrics(rows))})
        regimes_out.append(
            {
                "name": regime.name,
                "shift_family": regime.shift_family,
                "battery_state": regime.battery_state,
                "battery_pct": regime.battery_pct,
                "methods": methods,
            }
        )

    cost_sweep = []
    for cost_scale in [0.25, 0.50, 1.00, 1.50, 2.00]:
        sweep = {}
        for policy in ["Periodic", "Always-on", "Battery-gated"]:
            rows = []
            for episode_idx in range(args.episodes):
                rng = random.Random(args.seed + 900000 + int(cost_scale * 1000) * 1000 + episode_idx * 17 + len(policy))
                row = simulate_episode(REGIMES[0], policy, rng, tau=tau, cost_scale=cost_scale)
                rows.append(row)
            sweep[policy] = mean(row["mission_return"] for row in rows)
        cost_sweep.append(
            {
                "cost_scale": cost_scale,
                "periodic": round(sweep["Periodic"], 2),
                "always_on": round(sweep["Always-on"], 2),
                "battery_gated": round(sweep["Battery-gated"], 2),
            }
        )

    ablation_rows = []
    for label, policy in [
        ("Full gated policy", "Battery-gated"),
        ("No battery-state input", "No battery-state input"),
        ("No compute-cost penalty", "No compute-cost penalty"),
        ("Slip-threshold heuristic", "Slip-threshold heuristic"),
    ]:
        rows = []
        for episode_idx in range(args.episodes):
            rng = random.Random(args.seed + 1200000 + 500 * episode_idx + len(policy))
            row = simulate_episode(REGIMES[0], policy, rng, tau=tau)
            rows.append(row)
        agg = aggregate_metrics(rows)
        ablation_rows.append(
            {
                "variant": label,
                "mission_return": round(agg["mission_return"], 2),
                "cost_of_transport": round(agg["cost_of_transport"], 2),
                "adapt_calls": int(round(agg["adapt_calls"])),
                "compute_wh": round(agg["compute_wh"], 2),
            }
        )

    output = {
        "topic": "Battery-gated forward-only adaptation for battery-constrained quadruped robots",
        "benchmark_note": (
            "Computed stochastic benchmark for the cruisecontrol end-to-end sample. "
            "Values are generated by results/simulate_battery_benchmark.py from a lightweight deployment simulator, "
            "not hand-authored."
        ),
        "simulator_note": (
            "Each metric is averaged over "
            f"{args.episodes} stochastic episodes per regime and policy. "
            "The battery-gated threshold tau is tuned on a smaller held-out sweep."
        ),
        "tuning": {
            "tau": tau,
            "objective": round(tune["objective"], 4),
            "objective_name": "battery-adjusted mission utility",
            "tune_episodes": args.tune_episodes,
            "seed": args.seed,
        },
        "regimes": regimes_out,
        "cost_sweep": cost_sweep,
        "ablation": ablation_rows,
    }

    (ROOT / "demo_benchmark.json").write_text(json.dumps(output, indent=2) + "\n")
    write_episode_csv(ROOT / "episode_metrics.csv", raw_rows)


if __name__ == "__main__":
    main()
