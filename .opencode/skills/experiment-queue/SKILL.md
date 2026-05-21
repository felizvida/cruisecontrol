---
name: experiment-queue
description: "Queue and monitor multi-job experiment batches with GPU-aware scheduling, stale-session cleanup, and OOM-aware retry. Use when one-off experiment launching is no longer enough."
argument-hint: [manifest-or-grid-spec]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, Skill
---

# Experiment Queue

Queue a batch of experiments for: **$ARGUMENTS**

This skill is for workloads that are too large or repetitive for `/run-experiment` to handle comfortably by hand.

## When To Use It

Use this when you have:

- 10 or more jobs
- multi-seed sweeps
- multi-configuration grids
- staged teacher -> student runs
- jobs that regularly hit OOM and need retry logic

Use `/run-experiment` for one-off jobs or very small batches.

## Tooling

This repo ships a local queue scheduler:

```bash
python3 scripts/experiment_queue/queue_manager.py --manifest manifest.json --state queue_state.json --log queue.log
```

The scheduler is designed to run where the jobs will actually launch. For remote machines, upload the manifest and the script, then run it there.

## Manifest Shape

Recommended manifest fields:

```json
{
  "project": "example_project",
  "cwd": "/path/to/code",
  "conda": "research",
  "conda_hook": "eval \"$(/opt/conda/bin/conda shell.bash hook)\"",
  "gpus": [0, 1, 2, 3],
  "max_parallel": 4,
  "gpu_free_threshold_mib": 500,
  "poll_interval_sec": 60,
  "oom_retry": {"delay": 120, "max_attempts": 3},
  "jobs": [
    {
      "id": "seed42",
      "cmd": "python train.py --seed 42",
      "expected_output": "results/seed42.json"
    }
  ]
}
```

The scheduler also supports `phases`, where each phase contains its own `jobs` and may depend on earlier phases.

## Workflow

### Step 1: Build the manifest

Expand the user request into explicit jobs:

- concrete ids
- concrete commands
- expected outputs
- GPU list
- retry policy

Save the manifest under a project-local queue folder such as:

```text
experiment_queue/<timestamp>/manifest.json
```

### Step 2: Pre-flight

Before launching:

- verify the target working directory exists
- verify the conda environment exists
- verify `screen` is available if using detached launch
- verify GPUs are visible
- verify any input checkpoints already exist

### Step 3: Launch the scheduler

Run the queue manager in a detached session or background process on the target machine. The scheduler:

- finds free GPUs by `nvidia-smi`
- launches each job in its own `screen`
- watches expected outputs
- retries OOM jobs up to the configured limit
- cleans stale screens whose Python process has already exited
- writes a continuous JSON state ledger

### Step 4: Monitor progress

Read the queue state file rather than guessing from shell output. The main state machine is:

- `pending`
- `running`
- `completed`
- `failed_oom`
- `stuck`

Use `/monitor-experiment` to summarize the queue state if you want a friendlier readout.

### Step 5: Summarize results

When the queue is done, preserve:

- the manifest
- the queue state file
- the queue log
- the experiment outputs
- a short summary of success, retries, and stuck jobs

## Key Rules

- Do not blindly fill GPUs without checking free memory.
- Keep one clear state file that can be resumed after interruption.
- Expected outputs should be explicit; otherwise completion detection is too fragile.
- Prefer queueing over manual relaunching once the batch is large enough.

## Integration Points

- `/run-experiment` should hand off to this skill when the request is clearly a large batch.
- `/monitor-experiment` should read queue state files when present.
