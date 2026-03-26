---
name: auto-paper-improvement-loop
description: "Autonomously improve a generated paper via review → implement fixes → recompile, for 2 rounds. Prefer paperreview.ai as the external review backend when configured; otherwise fall back to the local Codex/OpenCode reviewer route. Default route is pure Codex; pure OpenCode is opt-in. Use when user says \"改论文\", \"improve paper\", \"论文润色循环\", \"auto improve\", or wants to iteratively polish a generated paper."
argument-hint: [paper-directory]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent
---

# Auto Paper Improvement Loop: Review Opinion + Score → Fix → Recompile

Autonomously improve the paper at: **$ARGUMENTS**

## Context

This skill is designed to run **after** Workflow 3 (`/paper-plan` → `/paper-figure` → `/paper-write` → `/paper-compile`). It takes a compiled paper and iteratively improves it through fresh review passes.

Unlike `/auto-review-loop` (which iterates on **research** — running experiments, collecting data, rewriting narrative), this skill iterates on **paper quality** using an explicit review opinion and score — fixing theoretical inconsistencies, softening overclaims, adding missing content, improving presentation, and preserving a traceable score progression.

## Constants

- **MAX_ROUNDS = 2** — Two rounds of review→fix→recompile. Empirically, Round 1 catches structural issues (4→6/10), Round 2 catches remaining presentation issues (6→7/10). Diminishing returns beyond 2 rounds for writing-only improvements.
- **WORKFLOW_ROUTE = `codex`** — Default route. Override inline with `route: opencode`.
- **REVIEW_BACKEND = `paperreview.ai` when configured** — Preferred external paper reviewer for this loop. The service currently needs a submission email for upload, but later review retrieval is token-based. If we can supply a submission email, use `paperreview.ai`; otherwise fall back to the route-local fresh review pass.
- **LOCAL_FALLBACK_REVIEWER = route-dependent fresh review pass** — Use Codex when `WORKFLOW_ROUTE=codex`; use the configured OpenCode model when `WORKFLOW_ROUTE=opencode`.
- **REVIEW_LOG = `PAPER_IMPROVEMENT_LOG.md`** — Cumulative log of all rounds, stored in paper directory.
- **ROUND_REVIEWS = `review/ROUND_REVIEWS.md`** — Serialized round-by-round review ledger. Each round `N+1` must be driven by the criticisms recorded for round `N`.
- **FINAL_REVIEW_OPINION = `review/REVIEW_OPINION.md`** — Final structured review opinion, stored in the project root.
- **FINAL_SCORECARD = `review/review_scorecard.json`** — Final machine-readable score summary, stored in the project root.

## Inputs

1. **Compiled paper** — `paper/main.pdf` + LaTeX source files
2. **All section `.tex` files** — concatenated for review prompt
3. **Project root** — create `review/` if it does not already exist
4. **External review config** — prefer explicit user input, then `PAPERREVIEW_EMAIL`, then project `AGENTS.md` `## External Review`; after submission, treat the saved token as the primary retrieval credential

## State Persistence (Compact Recovery)

If the context window fills up mid-loop, Claude Code auto-compacts. To recover, this skill writes `PAPER_IMPROVEMENT_STATE.json` after each round:

```json
{
  "current_round": 1,
  "last_score": 6,
  "status": "in_progress",
  "timestamp": "2026-03-13T21:00:00"
}
```

**On startup**: if `PAPER_IMPROVEMENT_STATE.json` exists with `"status": "in_progress"` AND `timestamp` is within 24 hours, read it + `PAPER_IMPROVEMENT_LOG.md` to recover context, then resume from the next round. Otherwise (file absent, `"status": "completed"`, or older than 24 hours), start fresh.

**After each round**: overwrite the state file. **On completion**: set `"status": "completed"`.

## Workflow

### Step 0: Preserve Original

```bash
cp paper/main.pdf paper/main_round0_original.pdf
```

### Step 1: Collect Paper Text

Concatenate all section files into a single text block for the review prompt:

```bash
# Collect all sections in order
for f in paper/sections/*.tex; do
    echo "% === $(basename $f) ==="
    cat "$f"
done > /tmp/paper_full_text.txt
```

### Step 1.5: Resolve Review Backend

Resolve the paper-review backend before the first round:

1. If `paperreview.ai` is configured with a submission email, use it.
2. Otherwise, use the local route reviewer (`codex` or `opencode`).

For `paperreview.ai`, remember the current service constraints:
- PDF only
- max `10MB`
- first `15` pages analyzed
- calibrated numeric score exposed only for `ICLR`

If `paperreview.ai` is selected, use the `paperreview-ai-review` skill and its bundled script:

```bash
python3 .opencode/skills/paperreview-ai-review/scripts/paperreview_client.py submit-and-wait ...
```

Save the returned token locally. Do not rely on the email notification alone; the token is enough to retrieve the finished review later.

### Step 2: Round 1 Review

Preferred path: submit `paper/main_round0_original.pdf` to `paperreview.ai` and wait for the review.

Save:
- `review/round00_paperreview_submission.json`
- `review/round00_paperreview_response.json`
- `review/round00_review.md`
- `review/round00_scorecard.json`

If `paperreview.ai` is unavailable or not configured, launch a fresh local review pass and give it:

- the full paper text
- venue context
- instructions to act as a senior reviewer
- instructions to return: score, confidence, summary, strengths, weaknesses, actionable fixes, missing references, and verdict

Focus either backend’s review on:
- theoretical rigor
- claims vs evidence alignment
- writing clarity
- self-containedness
- notation consistency

Immediately append the full structured review to `review/ROUND_REVIEWS.md` under a `## Round 0 Review` heading, because Round 1 fixes must be auditable as responses to that exact criticism set.

### Step 3: Implement Round 1 Fixes

Parse the review and implement fixes by severity:

**Priority order:**
1. CRITICAL fixes (assumption mismatches, internal contradictions)
2. MAJOR fixes (overclaims, missing content, notation issues)
3. MINOR fixes (if time permits)

**Common fix patterns:**

| Issue | Fix Pattern |
|-------|-------------|
| Assumption-model mismatch | Rewrite assumption to match the model, add formal proposition bridging the gap |
| Overclaims | Soften language: "validate" → "demonstrate practical relevance", "comparable" → "qualitatively competitive" |
| Missing metrics | Add quantitative table with honest parameter counts and caveats |
| Theorem not self-contained | Add "Interpretation" paragraph listing all dependencies |
| Notation confusion | Rename conflicting symbols globally, add Notation paragraph |
| Missing references | Add to `references.bib`, cite in appropriate locations |
| Theory-practice gap | Explicitly frame theory as idealized; add synthetic validation subsection |

### Step 4: Recompile Round 1

```bash
cd paper && latexmk -C && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf main_round1.pdf
```

Verify: 0 undefined references, 0 undefined citations.

### Step 5: Round 2 Review

Preferred path: submit `paper/main_round1.pdf` to `paperreview.ai` and wait for a fresh review.

Save:
- `review/round01_paperreview_submission.json`
- `review/round01_paperreview_response.json`
- `review/round01_review.md`
- `review/round01_scorecard.json`

If `paperreview.ai` is unavailable or not configured, launch a fresh local review pass. Do not rely on hidden thread state. Pass:

- the prior round review
- the fixes implemented since that review
- the updated paper text

Ask for the same structured output:
- Score
- Confidence
- Summary
- Strengths
- Weaknesses
- Actionable fixes
- Verdict

Append the new full review to `review/ROUND_REVIEWS.md` under `## Round 1 Review`, explicitly listing:

- paper reviewed
- score
- verdict
- main criticisms
- required fixes for the next round

### Step 6: Implement Round 2 Fixes

Same process as Step 3. Typical Round 2 fixes:
- Add controlled synthetic experiments validating theory
- Further soften any remaining overclaims
- Formalize informal arguments (e.g., truncation → formal proposition)
- Strengthen limitations section

### Step 7: Recompile Round 2

```bash
cd paper && latexmk -C && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf main_round2.pdf
```

### Step 8: Format Check

After the final recompilation, run a format compliance check:

```bash
# 1. Page count vs venue limit
PAGES=$(pdfinfo paper/main.pdf | grep Pages | awk '{print $2}')
echo "Pages: $PAGES (limit: 9 main body for ICLR/NeurIPS)"

# 2. Overfull hbox warnings (content exceeding margins)
OVERFULL=$(grep -c "Overfull" paper/main.log 2>/dev/null || echo 0)
echo "Overfull hbox warnings: $OVERFULL"
grep "Overfull" paper/main.log 2>/dev/null | head -10

# 3. Underfull hbox warnings (loose spacing)
UNDERFULL=$(grep -c "Underfull" paper/main.log 2>/dev/null || echo 0)
echo "Underfull hbox warnings: $UNDERFULL"

# 4. Bad boxes summary
grep -c "badness" paper/main.log 2>/dev/null || echo "0 badness warnings"
```

**Auto-fix patterns:**

| Issue | Fix |
|-------|-----|
| Overfull hbox in equation | Wrap in `\resizebox` or split with `\split`/`aligned` |
| Overfull hbox in table | Reduce font (`\small`/`\footnotesize`) or use `\resizebox{\linewidth}{!}{...}` |
| Overfull hbox in text | Rephrase sentence or add `\allowbreak` / `\-` hints |
| Over page limit | Move content to appendix, compress tables, reduce figure sizes |
| Underfull hbox (loose) | Rephrase for better line filling or add `\looseness=-1` |

If any overfull hbox > 10pt is found, fix it and recompile before documenting.

### Step 9: Document Results

Create `PAPER_IMPROVEMENT_LOG.md` in the paper directory:

```markdown
# Paper Improvement Log

## Score Progression

| Round | Score | Verdict | Key Changes |
|-------|-------|---------|-------------|
| Round 0 (original) | X/10 | No/Almost/Yes | Baseline |
| Round 1 | Y/10 | No/Almost/Yes | [summary of fixes] |
| Round 2 | Z/10 | No/Almost/Yes | [summary of fixes] |

## Round 1 Review & Fixes

<details>
<summary>Reviewer-Agent Review (Round 1)</summary>

[Full raw review text, verbatim]

</details>

### Fixes Implemented
1. [Fix description]
2. [Fix description]
...

## Round 2 Review & Fixes

<details>
<summary>Reviewer-Agent Review (Round 2)</summary>

[Full raw review text, verbatim]

</details>

### Fixes Implemented
1. [Fix description]
2. [Fix description]
...

## PDFs
- `main_round0_original.pdf` — Original generated paper
- `main_round1.pdf` — After Round 1 fixes
- `main_round2.pdf` — Final version after Round 2 fixes
```

Also write `review/ROUND_REVIEWS.md` in the project root if it does not already exist. This file is the serialized review ledger and is required whenever the loop contains more than one round. It must preserve the round `N` criticisms that directly drove the round `N+1` fixes.

Also write final review artifacts in the project root:

`review/REVIEW_OPINION.md`

```markdown
# Final Review Opinion

## Submission Snapshot
- Paper: `paper/main.pdf`
- Venue:
- Final round:

## Score
- Overall score: X/10
- Verdict: Weak Reject / Borderline / Weak Accept / Accept
- Confidence: 0.00

## Summary
[2-3 sentence reviewer summary]

## Strengths
- ...

## Weaknesses
- ...

## Improvements Across Rounds
- Round 0 → 1:
- Round 1 → 2:

## Remaining Risks Before Submission
- ...
```

`review/review_scorecard.json`

```json
{
  "paper_path": "paper/main.pdf",
  "venue": "ICLR",
  "round0_score": 5.8,
  "round1_score": 6.6,
  "round2_score": 7.1,
  "final_score": 7.1,
  "verdict": "Weak Accept",
  "confidence": 0.72,
  "status": "submission_ready_with_known_risks"
}
```

The review opinion and scorecard should reflect the **final** round while the improvement log preserves the full round-by-round history.

### Step 10: Summary

Report to user:
- Score progression table
- Number of CRITICAL/MAJOR/MINOR issues fixed per round
- Final page count
- Remaining issues (if any)

### Feishu Notification (if configured)

After each round's review AND at final completion, check `~/.config/opencode/feishu.json`:
- **After each round**: Send `review_scored` — "Round N: X/10 — [key changes]"
- **After final round**: Send `pipeline_done` — score progression table + final page count
- If config absent or mode `"off"`: skip entirely (no-op)

## Output

```
paper/
├── main_round0_original.pdf    # Original
├── main_round1.pdf             # After Round 1
├── main_round2.pdf             # After Round 2 (final)
├── main.pdf                    # = main_round2.pdf
└── PAPER_IMPROVEMENT_LOG.md    # Full review log with scores

review/
├── ROUND_REVIEWS.md                # Serialized review chain: round N criticism → round N+1 fixes
├── round00_review.md               # Round 0 review text (paperreview.ai or local fallback)
├── round00_scorecard.json          # Round 0 machine-readable score summary
├── round01_review.md               # Round 1 review text (paperreview.ai or local fallback)
├── round01_scorecard.json          # Round 1 machine-readable score summary
├── round00_paperreview_*.json      # If using paperreview.ai: submission and raw response for round 0
├── round01_paperreview_*.json      # If using paperreview.ai: submission and raw response for round 1
├── REVIEW_OPINION.md               # Final review opinion for the completed paper
└── review_scorecard.json           # Final machine-readable score summary
```

## Key Rules

- **Preserve all PDF versions** — user needs to compare progression
- **Each round must be review-driven** — do not invent extra rounds that are not tied to the immediately previous round's criticisms
- **Persist the serialized review chain** — `review/ROUND_REVIEWS.md` is mandatory for multi-round examples
- **Prefer paperreview.ai when configured** — use the external review backend for paper rounds unless file-size, language, or service constraints force a fallback
- **Save FULL raw review text** — do not summarize or truncate reviewer-agent responses
- Use a fresh review pass for every round; continuity must come from the saved round review ledger
- **Save the token locally** when paperreview.ai returns it
- **Always recompile after fixes** — verify 0 errors before proceeding
- **Do not fabricate experimental results** — synthetic validation must describe methodology, not invent numbers
- **Respect the paper's claims** — soften overclaims rather than adding unsupported new claims
- **Global consistency** — when renaming notation or softening claims, check ALL files (abstract, intro, method, experiments, theory sections, conclusion, tables, figure captions)

## Typical Score Progression

Based on end-to-end testing on a 9-page ICLR 2026 theory paper:

| Round | Score | Key Improvements |
|-------|-------|-----------------|
| Round 0 | 4/10 (content) | Baseline: assumption-model mismatch, overclaims, notation issues |
| Round 1 | 6/10 (content) | Fixed assumptions, softened claims, added interpretation, renamed notation |
| Round 2 | 7/10 (content) | Added synthetic validation, formal truncation proposition, stronger limitations |
| Round 3 | 5→8.5/10 (format) | Removed hero fig, appendix, compressed conclusion, fixed overfull hbox |

**+4.5 points across 3 rounds** (2 content + 1 format) is typical for a well-structured but rough first draft. Final: 8 pages main body, 0 overfull hbox, ICLR-compliant.
