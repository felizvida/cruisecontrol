---
name: citation-audit
description: "Verify that a paper's references are real, correctly described, and used in contexts the cited works actually support. Use before submission or whenever you want a bibliography integrity pass."
argument-hint: [paper-directory-or-bib-file] [--uncited] [--soft-only]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent
---

# Citation Audit

Audit the references for: **$ARGUMENTS**

This skill is the bibliography-integrity layer for the paper workflow. It is meant to catch three different failures:

1. the cited work does not exist as described
2. the metadata is wrong or incomplete
3. the citation is real, but the paper is using it to support the wrong claim

The point is not only to clean up formatting. The point is to keep the manuscript from leaning on citations that would embarrass the paper under close reading.

## When To Use It

Run this after the paper is already coherent and before you call it submission-ready.

Typical timing:

```text
/paper-plan -> /paper-figure -> /paper-write -> /paper-compile
-> /auto-paper-improvement-loop -> /paper-claim-audit -> /citation-audit
```

Do not spend time on this skill while the draft is still half placeholder text.

## Route And Reviewer Rules

- **WORKFLOW_ROUTE = `codex`** by default. Honor `route: opencode` if the user explicitly asks for it.
- **REVIEWER_MODE = fresh route-local review pass with web lookup**. The review context should be fresh for the audit run rather than inherited from the writing session.
- **WEB VERIFICATION = required**. Do not rely on memory alone for citation existence or metadata checks.

## Outputs

Write the audit artifacts into the paper directory:

- `CITATION_AUDIT.md`
- `CITATION_AUDIT.json`
- `.aris/citation-audit/contexts.txt`

If the paper directory is `paper/`, keep those files under `paper/`, not at repo root.

## Workflow

### Step 1: Discover the bibliography and citation contexts

Locate:

- `references.bib` or the active `.bib` file
- `main.tex`
- all cited section files, usually `sections/*.tex`

Extract every citation use as:

- cite key
- file
- line
- surrounding sentence or paragraph fragment

Save the extracted context list to:

```text
.aris/citation-audit/contexts.txt
```

Also record two sets:

- `cited_keys`: unique cite keys used in `\cite{...}` calls
- `bib_keys`: cite keys defined in the active bib file

By default, audit only `cited_keys`. If the user passes `--uncited`, also report `bib_keys - cited_keys` as a detect-only cleanup section. Do not let uncited entries change the top-level verdict.

### Step 2: Verify each entry on three axes

For each cited entry, verify:

1. **Existence**
   - Does the work exist at the claimed DOI, arXiv ID, PMID, journal page, conference record, or canonical web record?
2. **Metadata**
   - Are the title, authors, year, venue, and identifier materially correct?
3. **Context**
   - Does the cited work actually support the way the manuscript is using it?

For citation-context checks, evaluate the paper's wording, not just the bib entry.

### Step 3: Record per-entry verdicts

Use these per-entry verdicts:

- `KEEP`
- `FIX`
- `REPLACE`
- `REMOVE`

Use these per-use context flags:

- `SUPPORTS`
- `WEAK`
- `WRONG`
- `UNCERTAIN`

### Step 4: Write the machine-readable artifact

Write `CITATION_AUDIT.json` using the assurance contract in:

```text
.opencode/skills/shared-references/assurance-contract.md
```

At minimum include:

- `audit_skill`
- `verdict`
- `reason_code`
- `summary`
- `audited_input_hashes`
- `trace_path`
- `thread_id`
- `reviewer_model`
- `reviewer_reasoning`
- `generated_at`
- `details`

Recommended `details` payload:

```json
{
  "total_entries": 24,
  "counts": {
    "KEEP": 17,
    "FIX": 5,
    "REPLACE": 1,
    "REMOVE": 1
  },
  "per_entry": [
    {
      "key": "smith2024example",
      "verdict": "FIX",
      "axis_failures": ["METADATA"],
      "uses": [
        {
          "file": "sections/1_introduction.tex",
          "line": 18,
          "verdict": "SUPPORTS"
        }
      ]
    }
  ]
}
```

When `--uncited` is enabled, also include:

```json
{
  "uncited_entries": [
    {
      "key": "smith2020unused",
      "suggestion": "prune",
      "reason": "present in bibliography but not cited in the manuscript"
    }
  ]
}
```

### Step 5: Write the human-readable report

Write `CITATION_AUDIT.md` with:

- overall verdict
- counts by action type
- highest-priority repairs first
- clear file-level follow-up actions

The report should separate:

- metadata fixes
- wrong-context replacements
- hallucinated or unverifiable references
- uncited entries, when `--uncited` was requested

### Step 6: Apply safe fixes

Safe automatic fixes:

- title cleanup
- author list cleanup
- year correction
- DOI / URL correction
- venue correction

Do **not** automatically rewrite claim text or swap out a citation that changes the meaning of the sentence unless the user explicitly asked for auto-application.

If the user passes `--soft-only`, run the same verification pass but do not mutate the `.bib` file. Convert suggested metadata, replacement, or removal actions into explicit follow-up edits against the citing prose instead.

## Output Semantics

Top-level audit verdicts:

- `PASS` if everything is clean or only trivial metadata fixes remain
- `WARN` if the paper is usable but needs nontrivial citation repair
- `FAIL` if the bibliography contains fabricated or seriously wrong-context references
- `NOT_APPLICABLE` if the manuscript contains no citations
- `BLOCKED` if the paper cites references but the bibliography or source text is missing
- `ERROR` if the audit process itself failed

## Key Rules

- Use a fresh review context for the audit run.
- Check the real cited record, not a guess.
- Treat wrong-context citations as more serious than typos.
- Keep uncited-entry detection opt-in and non-blocking.
- Always emit `CITATION_AUDIT.json`, even when the verdict is `NOT_APPLICABLE`, `BLOCKED`, or `ERROR`.
- If the user asks for submission readiness, rerun this audit after any text edits that change the cited claims.

## Integration Points

- `/paper-writing` should run this as part of the submission-assurance finish line.
- `/auto-paper-improvement-loop` should rerun it after a review-driven revision if the paper is being prepared for submission.
- `scripts/verify_paper_audits.sh` treats this artifact as one of the mandatory pre-submission checks.
