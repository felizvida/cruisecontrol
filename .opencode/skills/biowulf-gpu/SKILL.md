---
name: biowulf-gpu
description: Obtain and correctly use a moderate GPU allocation on NIH Biowulf through the frontend node. Use when the user mentions Biowulf, asks for a GPU allocation, wants to check Biowulf GPU availability, needs module-loading help, or wants a reusable one-node GPU workflow with scratch-disk staging.
argument-hint: [request-description]
allowed-tools: Bash(*), Read, Grep, Glob, Edit, Write, Agent
---

# Biowulf GPU

Request and verify a GPU allocation on NIH Biowulf: $ARGUMENTS

## Workflow

### Step 1: Read project metadata if present

Read the active repo's `AGENTS.md` first. Look for:

- Biowulf SSH entry
- preferred GPU type
- module setup
- conda setup
- scratch / staging rules
- expected code directory
- budget or queue constraints

If the project metadata is missing, default to the known-good frontend:

- SSH host: `biowulf.nih.gov`

### Step 2: Check current GPU availability

Run the frontend query through a login shell so Slurm tools are on `PATH`:

```bash
ssh -o BatchMode=yes biowulf.nih.gov 'bash -lc "freen | grep -E \"Partition|----|gpu|quick|forgo\" | sed -n \"1,40p\""'
```

Key rule: stay moderate and do not exceed **one node**.

### Step 3: Choose a request

Default allocation rules:

- never request more than one node: `-N1`
- prefer a moderate GPU count
- request local scratch when the workload needs large inputs, checkpoints, caches, or temporary outputs
- prefer shorter time limits for smoke tests
- if day-time queues are busy, expect waits up to roughly two hours
- late-night waits may be closer to one hour or less

Good default smoke-test request:

```bash
ssh -tt -o BatchMode=yes biowulf.nih.gov "bash -lc 'srun --partition=gpu --gres=gpu:p100:2,lscratch:50 --cpus-per-task=14 --mem=32g --time=01:00:00 -N1 -n1 bash -lc \"hostname; echo LSCRATCH=/lscratch/\\\$SLURM_JOB_ID; nvidia-smi --query-gpu=index,name,memory.total --format=csv,noheader\"'"
```

Adjust the GPU type if `freen` shows a better one-node option.

### Step 4: Handle pending jobs

If the request queues, capture the job id and poll it:

```bash
ssh -o BatchMode=yes biowulf.nih.gov "bash -lc 'squeue -j <jobid> -o \"%.18i %.10T %.12M %.12l %.30R\"'"
```

Do not start a second queued GPU request unless the user asks. If a strategy change is needed, cancel the old job first.

### Step 5: Enter the compute environment correctly

All real workloads belong on the allocated compute node, not on `biowulf.nih.gov`.

Use the frontend only to:

- check availability with `freen`
- submit or start allocations with `srun`, `sinteractive`, or `sbatch`
- inspect queue state with `squeue`
- stage small control files

Once inside the allocation:

- load modules there
- activate conda there
- stage large data there
- run the actual training / evaluation / preprocessing there

Module-loading pattern:

```bash
module purge
module spider python
module spider pytorch
module load python/<version>
module load pytorch/<version>
module list
```

If the project metadata already records exact modules, use those instead of guessing.
If conda is needed, initialize and activate it inside the compute shell after `module load`.

### Step 6: Use scratch for large data

Do not store large datasets, model checkpoints, caches, or temporary outputs in `$HOME`.

Preferred pattern:

- request local scratch as part of the allocation, for example `--gres=gpu:p100:2,lscratch:50`
- stage heavy inputs into `/lscratch/$SLURM_JOB_ID`
- point caches, temp files, and large intermediate outputs there
- copy final results back to persistent project storage before the job exits

Useful compute-node checks:

```bash
echo "$SLURM_JOB_ID"
echo "/lscratch/$SLURM_JOB_ID"
df -h "/lscratch/$SLURM_JOB_ID"
```

If the project has a persistent data location such as `/data/...` or another shared filesystem, treat that as the durable home for large inputs and final outputs. Treat `$HOME` as configuration / code / small-file storage, not bulk experiment storage.

### Step 7: Verify the allocation

A successful allocation should report:

- compute-node hostname, not `biowulf.nih.gov`
- expected GPU count/type from `nvidia-smi`
- scratch path for the job when requested

Minimum verification:

```bash
hostname
echo "/lscratch/$SLURM_JOB_ID"
nvidia-smi --query-gpu=index,name,memory.total --format=csv,noheader
```

### Step 8: Record the working recipe

Report back:

- frontend host used
- chosen partition / GPU type / GPU count
- CPUs, memory, and time limit
- scratch request and scratch path
- module / conda setup used inside the allocation
- job id
- allocated node
- exact verification output

If the user asks for reuse, turn the successful recipe into project metadata or a skill update.

## Important Rules

- Always use `bash -lc` on the remote side; otherwise Slurm tools may not be on `PATH`
- Keep requests on a single node
- Start moderate; scale only if the user asks
- Prefer `srun` for a deterministic one-shot verification and `sinteractive` when the user explicitly wants an interactive shell
- Never run training, preprocessing, or evaluation on the Biowulf frontend node
- Load modules inside the compute allocation, not as a substitute for getting an allocation
- Request and use `lscratch` for large transient datasets, caches, checkpoints, and intermediate outputs
- Never use `$HOME` as the place for large datasets or large experiment outputs
- Never claim a GPU allocation succeeded without `nvidia-smi` output from the compute node

## Known-Good Example

This repo successfully verified the following one-node request:

```bash
ssh -tt -o BatchMode=yes biowulf.nih.gov "bash -lc 'srun --partition=gpu --gres=gpu:p100:2 --cpus-per-task=14 --mem=32g --time=01:00:00 -N1 -n1 bash -lc \"hostname; nvidia-smi --query-gpu=index,name,memory.total --format=csv,noheader\"'"
```

That allocation landed on a compute node and returned:

- node: `cn2369`
- GPUs:
  - `Tesla P100-PCIE-16GB`
  - `Tesla P100-PCIE-16GB`

When converting that smoke test into a real workload, add `lscratch` to the allocation and move the actual program, module loads, caches, and large data staging into the compute shell.
