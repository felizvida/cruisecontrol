---
name: paper-claim-audit
description: "Verify that a paper's quantitative claims, comparisons, and scope language match the underlying result files. Use before submission or whenever you want an evidence-to-paper fidelity pass."
argument-hint: [paper-directory]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent
---

# Paper Claim Audit

Audit the manuscript claims for: **$ARGUMENTS**

This skill checks whether the paper reports its own evidence faithfully. It is not asking whether the science is interesting. It is asking whether the manuscript tells the numerical truth.

## What This Catches

- number inflation
- delta arithmetic errors
- best-run cherry-picking reported as an average
- config mismatches inside comparisons
- aggregation mismatches
- caption-content mismatches
- scope language that outruns the tested evidence

## Route And Reviewer Rules

- **WORKFLOW_ROUTE = `codex`** by default. Honor `route: opencode` if explicitly requested.
- **REVIEWER_MODE = fresh route-local review pass**. The auditor should not inherit the writer's hidden assumptions.
- **ZERO-CONTEXT POLICY = strong**. Give the reviewer the paper source and raw evidence files, not narrative summaries or earlier review memos.

## Outputs

Write these into the paper directory:

- `PAPER_CLAIM_AUDIT.md`
- `PAPER_CLAIM_AUDIT.json`

## Workflow

### Step 1: Collect paper source files

Read:

- `main.tex`
- `sections/*.tex`
- tables or figure snippets if they carry load-bearing claims

### Step 2: Collect raw evidence files

Look for raw evidence in places such as:

- `results/*.json`
- `results/*.csv`
- `results/*.tsv`
- `outputs/*.json`
- `outputs/*.csv`
- `**/metrics.json`
- `**/eval_results.json`
- config files used to establish fair comparisons

Exclude narrative summaries and review memos. The point is to compare the paper to the evidence, not the paper to another summary of the evidence.

### Step 3: Extract every quantitative or scope claim

For each claim, record:

- location
- exact paper wording
- value or comparison being asserted

This includes:

- absolute numbers
- relative improvements
- counts
- averages
- statements like "consistently outperforms", "across all settings", or "robustly improves"

### Step 4: Map each claim to evidence

For each extracted claim, identify:

- evidence file
- exact evidence value
- whether the mapping is direct, rounded, ambiguous, or unsupported

Use these claim-level statuses:

- `exact_match`
- `rounding_ok`
- `ambiguous_mapping`
- `missing_evidence`
- `config_mismatch`
- `aggregation_mismatch`
- `number_mismatch`
- `scope_overclaim`
- `unsupported_claim`

### Step 5: Emit the JSON artifact

Write `PAPER_CLAIM_AUDIT.json` using the assurance contract in:

```text
.opencode/skills/shared-references/assurance-contract.md
```

Recommended `details` payload:

```json
{
  "claims_checked": 18,
  "counts": {
    "exact_match": 11,
    "rounding_ok": 4,
    "ambiguous_mapping": 1,
    "number_mismatch": 1,
    "scope_overclaim": 1
  },
  "claims": [
    {
      "claim_id": 1,
      "location": "sections/3_results.tex:14",
      "paper_text": "Method A improves accuracy by 12.8%.",
      "paper_value": "12.8%",
      "evidence_file": "results/summary_metrics.json",
      "evidence_value": "12.76%",
      "status": "rounding_ok"
    }
  ]
}
```

### Step 6: Emit the human-readable report

Write `PAPER_CLAIM_AUDIT.md` with:

- overall verdict
- claim counts by status
- highest-priority fixes first
- exact corrections when the arithmetic is wrong

### Step 7: Apply safe corrections

Safe automatic fixes:

- numeric rounding corrections
- incorrect percentage deltas
- count corrections
- clarifying whether a number is mean, median, or best

Contentual fixes like rephrasing broad claims should still be surfaced explicitly, not quietly hidden.

## Output Semantics

Top-level verdicts:

- `PASS` if the claims are faithful and only trivial rounding edits remain
- `WARN` if there are fixable mismatches or scope statements that need tightening
- `FAIL` if the manuscript materially misstates the evidence
- `NOT_APPLICABLE` if the paper has no quantitative or scope-style empirical claims
- `BLOCKED` if claims exist but the raw evidence files are missing
- `ERROR` if the audit run failed

## Key Rules

- Fresh reviewer context every run.
- Compare against raw evidence, not downstream summaries.
- Always write `PAPER_CLAIM_AUDIT.json`, even for `NOT_APPLICABLE`, `BLOCKED`, or `ERROR`.
- If the paper changes after the audit, treat the audit as stale and rerun it before calling the paper submission-ready.

## Integration Points

- `/paper-writing` should run this at the submission-assurance stage.
- `scripts/verify_paper_audits.sh` checks freshness and blocking verdicts for this artifact.
- `/citation-audit` complements this skill by checking cited support rather than raw numeric fidelity.
