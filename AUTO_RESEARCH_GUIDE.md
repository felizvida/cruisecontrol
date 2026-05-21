# Auto Research Guide

This guide is the “what does it actually feel like?” version of the docs.

Instead of listing commands in isolation, it follows one concrete story: you sit down with a rough research direction, the workflow helps shape it into a testable idea, and the repo keeps turning that idea into a more serious research project.

From this point forward, the default story in this guide uses the **pure Codex** route. A pure OpenCode route still exists by explicit choice; see [WORKFLOW_ROUTES.md](WORKFLOW_ROUTES.md).

## The Setup

Imagine it is Monday morning.

You do not have a polished proposal. You do not have a paper outline. You do not even know whether your direction is novel enough to be worth a week of work.

What you do have is a question:

> Can we make test-time adaptation practical for battery-constrained quadruped robots?

That is exactly the kind of starting point this repo is built for.

If you choose the pure OpenCode route, [opencode.jsonc](opencode.jsonc) pins the OpenCode backend model on this machine:

```json
{
  "model": "amazon-bedrock/amazon.nova-premier-v1:0",
  "small_model": "amazon-bedrock/amazon.nova-premier-v1:0"
}
```

That pure OpenCode route stays entirely inside OpenCode. The default Codex route instead uses Codex end to end for critique, planning, writing, and paper-improvement passes.

Whichever route you choose, the paper-writing side now defaults to [classic-biology-prose](.opencode/skills/classic-biology-prose/SKILL.md): question first, claim early, evidence doing the work, a calmer closing cadence, and no slipping back into project-report or workflow-diary prose.

Two newer upstream-style finishing tools are worth knowing early:

- [figure-spec](.opencode/skills/figure-spec/SKILL.md) for deterministic architecture or workflow figures
- [paper-claim-audit](.opencode/skills/paper-claim-audit/SKILL.md) plus [citation-audit](.opencode/skills/citation-audit/SKILL.md) for the submission-assurance pass at the end

## Act I: Start With A Direction, Not A Thesis

Start with the broadest useful command:

```text
/idea-discovery "test-time adaptation for battery-constrained quadruped robots"
```

If you explicitly want the pure OpenCode route for the same stage, use:

```text
/idea-discovery "test-time adaptation for battery-constrained quadruped robots — route: opencode"
```

This is the right entry point when the direction is still fuzzy.

Behind the scenes, the workflow chains together:

- `research-lit`
- `idea-creator`
- `novelty-check`
- `research-review`

In practice, that means the system will:

- scan literature and map the landscape
- generate multiple concrete ideas instead of overcommitting to the first one
- eliminate ideas that are obviously derivative
- ask a fresh reviewer pass to be skeptical before you sink effort into implementation

This is the first mindset shift of “auto research”:

You are not asking the system to magically invent a paper.
You are asking it to reduce the cost of getting from vague curiosity to a disciplined shortlist.

## What A Good First Result Looks Like

After the `idea-discovery` run, you should expect a report that feels like a research lead, not a final answer.

The report should contain things like:

- a short landscape summary
- 2-5 candidate ideas, ranked
- novelty warnings or confidence levels
- a pilot plan that is small enough to run soon
- reviewer objections that force sharper framing

A healthy output sounds like this:

```markdown
# Idea Discovery Report

## Direction
Test-time adaptation for battery-constrained quadruped robots

## Landscape Summary
- Many adaptation methods assume compute or latency budgets that do not transfer well to mobile robots.
- Robotics papers often optimize control quality, but rarely optimize adaptation under explicit energy constraints.
- The strongest opportunity may be to frame adaptation as a budgeted systems problem rather than a pure accuracy problem.

## Top Ideas

### 1. Budgeted Episodic Adapter
Adapt only when uncertainty crosses a threshold and enforce a strict per-episode compute budget.

### 2. Distilled Recovery Head
Do heavy adaptation offline, then distill corrections into a lightweight online module.

## Reviewer Concerns
- Novelty will depend on whether the energy budget is measured, not just asserted.
- A compelling pilot needs reward, latency, and energy per episode.
- The story is stronger if the method occasionally refuses to adapt when cost is too high.

## Recommended Next Step
Pilot Idea 1 on a small terrain-shift benchmark with explicit energy logging.
```

That is the sweet spot.

Not “here is your perfect paper.”
Not “here are ten generic AI ideas.”
Instead: one promising path, one skeptical read, one practical next move.

## Act II: Turn The Best Idea Into A Harder Question

Now the temptation is to start coding immediately.

Usually, the better move is to pressure-test the idea one more time:

```text
/research-review "Budgeted episodic adapter for battery-constrained quadruped test-time adaptation"
```

This is where the system becomes useful in a different way.

The first stage helps generate possibilities.
This stage helps remove self-deception.

The review should tell you things like:

- what claim is currently too strong
- what experiment would actually convince a reviewer
- whether your framing sounds like a systems paper, an ML paper, or an awkward hybrid
- what the minimum evidence package looks like

If the review comes back harsh, that is a good sign.
It means the system is doing research triage rather than motivational theater.

## Act III: Run The First Real Experiment

Once you have one idea worth trying, move to execution:

```text
/run-experiment "pilot Budgeted Episodic Adapter with 3 terrain shifts, 3 seeds, and energy logging"
```

If you are using these skills inside a real project repo, this works best when that project has an `AGENTS.md` derived from [templates/project-AGENTS.md](templates/project-AGENTS.md), because the workflow can then find:

- your SSH target
- your conda environment
- your code directory
- your paper defaults

Then check progress:

```text
/monitor-experiment "your-server-or-session-name"
```

What matters here is not just whether the run finishes.

You want the experiment to produce artifacts that are reviewable:

- metrics saved to JSON or CSV
- logs that explain failure modes
- enough structure for follow-up analysis

The repo is most useful when it helps you produce a clean chain of evidence, not just a launched process.

## Act IV: Let The Reviewer Push Back

Once you have initial results, this repo gets more interesting.

Now you can hand the work back into the loop:

```text
/auto-review-loop "budgeted quadruped adaptation pilot"
```

This is the point where “auto research” becomes real.

The workflow will:

- summarize the current state of the work
- ask the reviewer to score it and identify the weakest points
- implement cheap, high-value fixes first
- run more analysis or experiments if needed
- repeat until the work looks stronger or the loop hits its stopping point

A realistic loop does not look heroic.
It looks methodical:

Round 1:
- the reviewer says the novelty claim is under-supported
- asks for a performance-per-joule table
- flags a missing baseline

Round 2:
- the system adds the table
- runs the missing baseline
- rewrites the framing to stop overclaiming

Round 3:
- the reviewer says the idea is now plausible, but still needs one ablation

This is where the repo saves time.
It keeps turning vague criticism into concrete next steps.

## What The Files Start To Mean

As you work, the repo will naturally accumulate a small local paper trail.

Common artifacts include:

- `IDEA_REPORT.md`
- `AUTO_REVIEW.md`
- `REVIEW_STATE.json`
- experiment logs and result tables
- later, `PAPER_PLAN.md` and `paper/`

These are not clutter.
They are the memory of the project.

When the workflow is working well, each file answers a different question:

- `IDEA_REPORT.md`: what should we try?
- `AUTO_REVIEW.md`: what is still weak?
- result tables: what actually happened?
- `PAPER_PLAN.md`: what is the story we can responsibly tell?

## Act V: Let The Pipeline Carry The Story Into A Paper

You can still run the writing stage directly:

```text
/paper-writing NARRATIVE_REPORT.md
```

But the stronger repo-level path is now:

```text
/research-pipeline "your research direction"
```

That single command is supposed to carry the work from idea discovery through review, then synthesize `NARRATIVE_REPORT.md`, then continue into paper generation without asking you to manually bridge the stages.

The paper workflow is strongest when you already know:

- the central claim
- the evidence for that claim
- which figures must exist
- which reviewer objections must be preempted

If one of those figures is a formal workflow or architecture figure, the cleaner route is now:

```text
/figure-spec "diagram description"
```

instead of improvising a one-off placeholder.

## Act VI: Treat Submission Readiness As A Separate Step

A polished paper and a submission-ready paper are not the same thing.

Once the writing and review loop are done, the repo now has a separate assurance pass:

```text
/paper-claim-audit "paper/"
/citation-audit "paper/"
```

Then:

```bash
bash scripts/verify_paper_audits.sh paper --assurance submission
```

That final check is useful because it asks different questions from the reviewer loop:

- do the numbers still match the evidence?
- are the citations real and honestly used?
- did later edits make the audit layer stale?

That is the last gate before calling the paper submission-ready.

The pipeline then helps convert that into:

- a paper plan
- figures and tables
- LaTeX sections
- a compiled PDF

At that stage the repo is not trying to sound "AI polished." It is trying to sound like a serious paper: clear, exact, and readable enough that another researcher would keep going rather than mentally editing every sentence.
- a scored paper-improvement loop

When the workflow is promoted to a complete final paper package in this repo, it should also leave behind:

- results generated from real executable computation
- code used to build or support the paper
- sample data or a source-data manifest
- a dedicated high-resolution figure folder
- `paper/main_round0_original.pdf`, `paper/main_round1.pdf`, and `paper/main_round2.pdf`
- `paper/PAPER_IMPROVEMENT_LOG.md`
- a detailed review opinion
- a score

That standard matters. A polished PDF without underlying computation is not treated as a finished paper here.
If the experiment is small, run it locally. If the experiment needs serious compute, move it to Biowulf, run it there, and package the resulting code and artifacts back into the repo.

The important point is that the writing stage is downstream of the research loop.
The workflow is not trying to hallucinate credibility into a weak result.
It is trying to preserve the logic of work you have already clarified.

## A Good End State

If the workflow is going well, the end of the day should feel like this:

You began with a direction.

You now have:

- one or two ideas worth defending
- a record of why weaker ideas were rejected
- an initial experiment package
- reviewer-generated pressure on the weak points
- a local trail of artifacts that make the next day easier
- and, in the end-to-end path, a complete paper package rather than only a compiled `paper/main.pdf`

That is already a win.

The value of this repo is not that it skips research.
The value is that it shortens the distance between:

- “this might be interesting”
- and
- “here is a claim, a test, a criticism, and the next move”

## The Smallest Useful Routine

If you want the shortest path to a productive session, use this sequence:

```text
/research-pipeline "your research direction"
```

That is the one-command path from fuzzy direction to a scored, revision-tracked paper package.
If you want more control, you can still break it back into the smaller workflow commands.

## How To Tell If You Are Using It Well

You are using the system well if:

- the prompts get more specific over time
- the reports become more falsifiable, not more grandiose
- the reviewer is finding things that genuinely change your next action
- you can point to a local file and say, “this is why we are doing the next experiment”

You are using it poorly if:

- every prompt is broad and generic
- every output sounds impressive but changes nothing
- the system keeps inventing claims faster than you can verify them
- you are writing paper sections before you know what the result means

## One Strong Habit

Treat every run as a research meeting with receipts.

At each stage, ask:

- What did we learn?
- What changed?
- What is the next cheapest thing that reduces uncertainty?

If the repo keeps helping you answer those three questions, it is doing its job.
