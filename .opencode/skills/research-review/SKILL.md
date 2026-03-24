---
name: research-review
description: Get a deep critical review of research. Default route is pure Codex; pure OpenCode is opt-in. Use when user says "review my research", "help me review", "get external review", or wants critical feedback on research ideas, papers, or experimental results.
argument-hint: [topic-or-scope]
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit, Agent
---

# Research Review
Get a multi-round critical review of research work from a fresh review pass.

## Constants

- WORKFLOW_ROUTE = `codex` (default). Override inline with `route: opencode`.
- REVIEWER_MODE = route-dependent fresh review pass. Use Codex when `WORKFLOW_ROUTE=codex`; use the configured OpenCode model when `WORKFLOW_ROUTE=opencode`.

## Context: $ARGUMENTS

All review outputs must be saved to local project files in the current repository. Do not invent external GitHub repositories, GitHub URLs, or remote destinations for deliverables.

## Workflow

### Step 1: Gather Research Context
Before launching the review pass, compile a comprehensive briefing:
1. Read project narrative documents (e.g., STORY.md, README.md, paper drafts)
2. Read any memory/notes files for key findings and experiment history
3. Identify: core claims, methodology, key results, known weaknesses

### Step 2: Initial Review (Round 1)
Launch a fresh review pass using the selected route and give it:

- full research context
- the specific questions you want answered
- instructions to act as a senior ML reviewer (NeurIPS/ICML level)
- instructions to identify logical gaps, missing experiments, narrative weaknesses, and venue readiness

Ask for:
- a score
- a verdict
- ranked weaknesses
- minimum fixes for each major weakness
- a self-contained review that can be saved directly to a local file

### Step 3: Iterative Dialogue (Rounds 2-N)
For each new round, launch a fresh review pass. Do not rely on hidden thread state. Instead, explicitly pass:

- the prior round review
- your responses to that review
- any new evidence, experiments, or rewritten claims

For each round:
1. **Respond** to criticisms with evidence/counterarguments
2. **Ask targeted follow-ups** on the most actionable points
3. **Request specific deliverables**: experiment designs, paper outlines, claims matrices

Key follow-up patterns:
- "If we reframe X as Y, does that change your assessment?"
- "What's the minimum experiment to satisfy concern Z?"
- "Please design the minimal additional experiment package (highest acceptance lift per GPU week)"
- "Please write a mock NeurIPS/ICML review with scores"
- "Give me a results-to-claims matrix for possible experimental outcomes"

### Step 4: Convergence
Stop iterating when:
- Both sides agree on the core claims and their evidence requirements
- A concrete experiment plan is established
- The narrative structure is settled

### Step 5: Document Everything
Save the full interaction and conclusions to a review document in the project root:
- Round-by-round summary of criticisms and responses
- Final consensus on claims, narrative, and experiments
- Claims matrix (what claims are allowed under each possible outcome)
- Prioritized TODO list with estimated compute costs
- Paper outline if discussed
- If the user supplied an explicit output path, write the review there exactly and verify the file exists before replying

Update project memory/notes with key review conclusions.

## Key Rules

- Use the strongest available reasoning mode for reviewer passes
- Send comprehensive context in Round 1 — the reviewer agent should not need to guess missing facts
- Be honest about weaknesses — hiding them leads to worse feedback
- Push back on criticisms you disagree with, but accept valid ones
- Focus on ACTIONABLE feedback — "what experiment would fix this?"
- Persist the raw review text so future rounds can reference it explicitly
- The review document should be self-contained (readable without the conversation)

## Prompt Templates

### For initial review:
"I'm going to present a complete ML research project for your critical review. Please act as a senior ML reviewer (NeurIPS/ICML level)..."

### For experiment design:
"Please design the minimal additional experiment package that gives the highest acceptance lift per GPU week. Our compute: [describe]. Be very specific about configurations."

### For paper structure:
"Please turn this into a concrete paper outline with section-by-section claims and figure plan."

### For claims matrix:
"Please give me a results-to-claims matrix: what claim is allowed under each possible outcome of experiments X and Y?"

### For mock review:
"Please write a mock NeurIPS review with: Summary, Strengths, Weaknesses, Questions for Authors, Score, Confidence, and What Would Move Toward Accept."
