#!/usr/bin/env python3
"""Simple queue manager for multi-job GPU experiment batches.

This is a local port of the upstream experiment-queue utility, trimmed to the
behavior this repo needs most:

- launch queued jobs onto free GPUs via `screen`
- persist queue state continuously
- detect stale screens and completed outputs
- retry CUDA OOM failures a bounded number of times
- respect phase dependencies when the manifest uses phases
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import shlex
import socket
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


OOM_RE = re.compile(r"(CUDA out of memory|torch\.OutOfMemoryError)")
DEFAULT_POLL_INTERVAL = 60
DEFAULT_GPU_FREE_THRESHOLD_MIB = 500


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def run(command: str) -> tuple[str, int]:
    proc = subprocess.run(command, shell=True, text=True, capture_output=True)
    return proc.stdout.strip(), proc.returncode


def load_manifest(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        manifest = json.load(handle)
    if not isinstance(manifest, dict):
        raise ValueError("manifest must be a JSON object")
    manifest["_path"] = str(path.resolve())
    return manifest


def detect_conda_hook(manifest: dict[str, Any]) -> str:
    value = manifest.get("conda_hook")
    if isinstance(value, str) and value:
        if value.startswith("eval "):
            return value
        return f'eval "$({value} shell.bash hook)"'
    env_value = os.environ.get("ARIS_CONDA_HOOK")
    if env_value:
        if env_value.startswith("eval "):
            return env_value
        return f'eval "$({env_value} shell.bash hook)"'
    for path in (
        Path.home() / "anaconda3/bin/conda",
        Path.home() / "miniconda3/bin/conda",
        Path.home() / "miniforge3/bin/conda",
        Path("/opt/anaconda3/bin/conda"),
        Path("/opt/miniconda3/bin/conda"),
        Path("/opt/miniforge3/bin/conda"),
    ):
        if path.exists():
            return f'eval "$({path} shell.bash hook)"'
    return 'eval "$(conda shell.bash hook)"'


def manifest_jobs(manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    phases = manifest.get("phases")
    if isinstance(phases, list) and phases:
        phase_specs = []
        jobs = []
        for phase_index, phase in enumerate(phases):
            phase_name = phase.get("name", f"phase_{phase_index}")
            depends_on = phase.get("depends_on", [])
            phase_specs.append({"name": phase_name, "depends_on": depends_on, "status": "pending"})
            for raw_job in phase.get("jobs", []):
                job = dict(raw_job)
                job["phase"] = phase_name
                jobs.append(job)
        return jobs, phase_specs

    top_jobs = [dict(job) for job in manifest.get("jobs", [])]
    return top_jobs, [{"name": "main", "depends_on": [], "status": "pending"}]


def default_state(manifest: dict[str, Any]) -> dict[str, Any]:
    jobs, phases = manifest_jobs(manifest)
    state_jobs = []
    for job in jobs:
        state_jobs.append(
            {
                "id": job["id"],
                "phase": job.get("phase", "main"),
                "cmd": job["cmd"],
                "expected_output": job.get("expected_output"),
                "status": "pending",
                "gpu": None,
                "screen_name": None,
                "pid": None,
                "attempts": 0,
                "started": None,
                "completed": None,
                "error": None,
            }
        )
    return {
        "meta": {
            "project": manifest.get("project", "unknown"),
            "started": now_iso(),
            "host": socket.gethostname(),
            "manifest_path": manifest["_path"],
        },
        "phases": phases,
        "jobs": state_jobs,
    }


def load_state(path: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    if path.exists():
        with path.open() as handle:
            return json.load(handle)
    return default_state(manifest)


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(state, indent=2))
    tmp.replace(path)


def gpu_memory_used() -> list[int]:
    output, code = run("nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null")
    if code != 0 or not output:
        return []
    return [int(line.strip()) for line in output.splitlines() if line.strip()]


def free_gpus(allowed: list[int], threshold_mib: int) -> list[int]:
    used = gpu_memory_used()
    free = []
    for gpu in allowed:
        if gpu < len(used) and used[gpu] < threshold_mib:
            free.append(gpu)
    return free


def screen_exists(name: str) -> bool:
    output, _ = run(f"screen -ls | grep -F '.{name}'")
    return name in output


def kill_screen(name: str) -> None:
    run(f"screen -S {shlex.quote(name)} -X quit >/dev/null 2>&1")


def process_alive(pid: int | None) -> bool:
    if not pid:
        return False
    _, code = run(f"ps -p {pid} >/dev/null")
    return code == 0


def output_exists(cwd: Path, expected: str | None) -> bool:
    if not expected:
        return False
    full_path = Path(expected)
    if not full_path.is_absolute():
        full_path = cwd / expected
    if any(char in str(full_path) for char in "*?[]"):
        return bool(glob.glob(str(full_path)))
    return full_path.exists()


def log_path_for(job: dict[str, Any], log_dir: Path) -> Path:
    return log_dir / f"{job['id']}.log"


def detect_oom(log_path: Path) -> bool:
    if not log_path.exists():
        return False
    try:
        tail = log_path.read_text(errors="ignore")[-10000:]
    except OSError:
        return False
    return bool(OOM_RE.search(tail))


def phase_ready(phase_name: str, state: dict[str, Any]) -> bool:
    phase = next(item for item in state["phases"] if item["name"] == phase_name)
    for dependency in phase.get("depends_on", []):
        dep_phase = next((item for item in state["phases"] if item["name"] == dependency), None)
        if dep_phase is None or dep_phase["status"] != "completed":
            return False
    return True


def update_phase_statuses(state: dict[str, Any]) -> None:
    for phase in state["phases"]:
        phase_jobs = [job for job in state["jobs"] if job["phase"] == phase["name"]]
        if not phase_jobs:
            phase["status"] = "completed"
        elif all(job["status"] in {"completed", "stuck"} for job in phase_jobs):
            phase["status"] = "completed"
        elif any(job["status"] == "running" for job in phase_jobs):
            phase["status"] = "running"
        elif phase_ready(phase["name"], state):
            phase["status"] = "ready"
        else:
            phase["status"] = "pending"


def launch_job(job: dict[str, Any], manifest: dict[str, Any], gpu: int, log_dir: Path) -> None:
    cwd = Path(manifest["cwd"])
    conda_env = manifest.get("conda")
    conda_hook = detect_conda_hook(manifest)
    log_path = log_path_for(job, log_dir)
    screen_name = f"EQ_{job['id']}"

    shell_parts = [f"cd {shlex.quote(str(cwd))}", conda_hook]
    if conda_env:
        shell_parts.append(f"conda activate {shlex.quote(conda_env)}")
    shell_parts.append(f"export CUDA_VISIBLE_DEVICES={gpu}")
    shell_parts.append(f"{job['cmd']} 2>&1 | tee {shlex.quote(str(log_path))}")
    shell_body = " && ".join(shell_parts)
    command = f"screen -dmS {shlex.quote(screen_name)} bash -lc {shlex.quote(shell_body)}"
    _, code = run(command)
    if code != 0:
        raise RuntimeError(f"failed to launch job {job['id']}")

    pid_output, _ = run(f"screen -ls | grep -F '.{screen_name}' | awk '{{print $1}}' | cut -d. -f1 | head -n1")
    job["status"] = "running"
    job["gpu"] = gpu
    job["screen_name"] = screen_name
    job["pid"] = int(pid_output) if pid_output.isdigit() else None
    job["attempts"] += 1
    job["started"] = now_iso()
    job["error"] = None


def refresh_job_state(job: dict[str, Any], manifest: dict[str, Any], log_dir: Path) -> None:
    if job["status"] != "running":
        return

    cwd = Path(manifest["cwd"])
    log_path = log_path_for(job, log_dir)
    if output_exists(cwd, job.get("expected_output")):
        if job.get("screen_name"):
            kill_screen(job["screen_name"])
        job["status"] = "completed"
        job["completed"] = now_iso()
        return

    if process_alive(job.get("pid")) or (job.get("screen_name") and screen_exists(job["screen_name"])):
        return

    if detect_oom(log_path):
        job["status"] = "failed_oom"
        job["error"] = "cuda_oom"
    else:
        job["status"] = "stuck"
        job["error"] = "process_exited_without_expected_output"


def retry_ready(job: dict[str, Any], manifest: dict[str, Any]) -> bool:
    if job["status"] != "failed_oom":
        return False
    retry = manifest.get("oom_retry", {})
    delay = int(retry.get("delay", 120))
    limit = int(retry.get("max_attempts", 3))
    if job["attempts"] >= limit:
        job["status"] = "stuck"
        job["error"] = "oom_retry_exhausted"
        return False
    started = job.get("started")
    if not started:
        return True
    return datetime.now(timezone.utc) - datetime.fromisoformat(started.replace("Z", "+00:00")) >= timedelta(seconds=delay)


def scheduler_loop(manifest: dict[str, Any], state_path: Path, log_path: Path) -> int:
    state = load_state(state_path, manifest)
    poll_interval = int(manifest.get("poll_interval_sec", DEFAULT_POLL_INTERVAL))
    if poll_interval <= 0:
        raise ValueError("manifest 'poll_interval_sec' must be a positive integer")
    raw_gpus = manifest.get("gpus")
    if raw_gpus is None:
        detected_gpus = gpu_memory_used()
        gpu_list = list(range(len(detected_gpus)))
        if not gpu_list:
            raise ValueError("manifest must define a non-empty 'gpus' list or run on a host with nvidia-smi-visible GPUs")
    elif isinstance(raw_gpus, list) and all(isinstance(gpu, int) and gpu >= 0 for gpu in raw_gpus):
        gpu_list = raw_gpus
        if not gpu_list:
            raise ValueError("manifest 'gpus' must be a non-empty list of GPU indexes")
    else:
        raise ValueError("manifest 'gpus' must be a list of non-negative integer GPU indexes")

    max_parallel = int(manifest.get("max_parallel", len(gpu_list)))
    if max_parallel <= 0:
        raise ValueError("manifest 'max_parallel' must be a positive integer")
    threshold = int(manifest.get("gpu_free_threshold_mib", DEFAULT_GPU_FREE_THRESHOLD_MIB))
    if threshold < 0:
        raise ValueError("manifest 'gpu_free_threshold_mib' must be non-negative")
    log_dir = log_path.parent / "queue_logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    while True:
        for job in state["jobs"]:
            refresh_job_state(job, manifest, log_dir)
            if retry_ready(job, manifest):
                job["status"] = "pending"

        update_phase_statuses(state)

        running_jobs = [job for job in state["jobs"] if job["status"] == "running"]
        available_slots = max_parallel - len(running_jobs)
        free = free_gpus(gpu_list, threshold)

        if available_slots > 0 and free:
            for job in state["jobs"]:
                if available_slots <= 0 or not free:
                    break
                if job["status"] != "pending":
                    continue
                if not phase_ready(job["phase"], state):
                    continue
                gpu = free.pop(0)
                try:
                    launch_job(job, manifest, gpu, log_dir)
                    available_slots -= 1
                except Exception as exc:  # noqa: BLE001
                    job["status"] = "stuck"
                    job["error"] = str(exc)

        update_phase_statuses(state)
        save_state(state_path, state)
        log_path.write_text(json.dumps({"updated_at": now_iso(), "state": state}, indent=2))

        unfinished = [job for job in state["jobs"] if job["status"] not in {"completed", "stuck"}]
        if not unfinished:
            return 0
        time.sleep(poll_interval)


def main() -> int:
    parser = argparse.ArgumentParser(description="Queue manager for multi-job GPU experiment batches.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--state", required=True)
    parser.add_argument("--log", required=True)
    args = parser.parse_args()

    manifest = load_manifest(Path(args.manifest))
    Path(args.state).parent.mkdir(parents=True, exist_ok=True)
    Path(args.log).parent.mkdir(parents=True, exist_ok=True)
    return scheduler_loop(manifest, Path(args.state), Path(args.log))


if __name__ == "__main__":
    sys.exit(main())
