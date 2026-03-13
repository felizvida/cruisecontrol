# Quickstart User Guide

This guide gets a first-time user from clone to a working research workflow in OpenCode with one concrete example.

## What You Need

- OpenCode installed
- `codex` installed and available on your `PATH`
- This repo cloned locally

The review skills in this repo assume an MCP server named `codex`. That server is already enabled by default in [opencode.jsonc](/Users/liux17/codex/autoresearch/opencode.jsonc).

## 5-Minute Setup

1. Clone the repo:

   ```bash
   git clone https://github.com/felizvida/cruisecontrol
   cd cruisecontrol
   ```

2. Verify the MCP config:

   ```bash
   cat opencode.jsonc
   ```

   You should see:

   ```json
   {
     "mcp": {
       "codex": {
         "type": "local",
         "enabled": true,
         "command": ["codex", "mcp-server"]
       }
     }
   }
   ```

3. Optional: if you are using these skills inside a real research repo, copy the project template and fill in your local paper library or GPU server details:

   ```bash
   cp templates/project-AGENTS.md /path/to/your/project/AGENTS.md
   ```

4. Start OpenCode in this repo:

   ```bash
   opencode
   ```

5. In the OpenCode chat, verify that the `codex` MCP server is visible:

   ```text
   /mcp
   ```

   Or from a shell:

   ```bash
   opencode mcp list
   ```

## First Example

Use `idea-discovery` for the first run. It is the easiest end-to-end workflow because it goes from vague research direction to ranked ideas and a pilot plan.

Sample research idea:

```text
/idea-discovery "test-time adaptation for battery-constrained quadruped robots"
```

What this command should do:

- scan related work
- brainstorm several concrete ideas
- check novelty
- ask the external reviewer for critical feedback
- return a ranked idea report with next steps

## Sample Output

Actual output will vary by model and available tools. A typical good result should look roughly like this:

```markdown
# Idea Discovery Report

## Research Direction
Test-time adaptation for battery-constrained quadruped robots

## Landscape Summary
- Existing test-time adaptation methods usually assume server-class GPUs or long online optimization windows.
- Mobile robotics papers often optimize control latency, but not adaptation cost per watt.
- There appears to be room for methods that trade a small amount of asymptotic performance for predictable energy use.

## Recommended Ideas (ranked)

### Idea 1: Budgeted Episodic Adapter
Use a tiny episodic memory with a hard per-episode update budget. Adapt only when uncertainty crosses a threshold.

- Why it may matter: matches real robot energy constraints
- Main risk: adaptation signal may be too weak in short horizons
- Minimum pilot: compare no adaptation vs full adaptation vs budgeted adaptation on 3 terrain shifts

### Idea 2: Distilled Recovery Policy
Run a heavy adaptation policy offline, distill its corrections into a lightweight online recovery head.

- Why it may matter: pushes most cost offline
- Main risk: distilled policy may fail under unseen shifts

## Novelty Check
- No direct match found for "energy-budgeted test-time adaptation for quadruped locomotion"
- Closest papers study either test-time adaptation or low-power control, but not their joint optimization
- Confidence: medium

## Reviewer Feedback
- Strongest angle: compute-aware adaptation as a systems constraint
- Weakest point: novelty claim will depend on a clear baseline story and measured energy budget
- Required experiment: show performance-per-joule, not only reward or success rate

## Suggested Execution Order
1. Pilot Idea 1 with a strict update budget
2. Log adaptation gain, latency, and watt-hours
3. If gains are real, expand to additional terrain and payload shifts

## Next Steps
- Create a small pilot benchmark
- Add a metric table with reward, latency, and energy per episode
- Run `/auto-review-loop` after the first pilot results land
```

## After the First Run

Typical next commands:

- `/research-review "Idea 1 from the last report"`
- `/run-experiment "pilot Idea 1 with 3 terrain shifts and energy logging"`
- `/auto-review-loop "budgeted quadruped adaptation pilot"`
- `/paper-writing NARRATIVE_REPORT.md`

## What Success Looks Like

A successful first session usually leaves you with:

- a ranked idea report
- one idea with a cheap pilot experiment
- a short list of reviewer-requested evidence
- a clear next command

If the output is vague or generic, tighten the prompt. Example:

```text
/idea-discovery "test-time adaptation for battery-constrained quadruped robots — focus on ideas that can be piloted in under 8 GPU-hours and evaluated with latency plus energy metrics"
```

## Common Failure Modes

- `codex` MCP server not available: review and novelty-check steps will be weaker or fail
- no project `AGENTS.md`: experiment-launch skills will not know your server or paper-library setup
- overbroad topic: the system returns generic ideas instead of executable pilots

## Minimal Working Loop

If you only want the smallest useful workflow, use this:

```text
/idea-discovery "your topic"
/auto-review-loop "best idea from the report"
```

That gives you one discovery pass and one adversarial review loop without forcing you into paper generation.
