# Assurance Contract

This repo now distinguishes between:

- **paper quality work**: planning, writing, review, revision
- **submission assurance**: verifying that the paper's claims and references can survive close inspection

The assurance layer is intentionally narrower than the full paper workflow. In this port, the mandatory submission-audit artifacts are:

- `PAPER_CLAIM_AUDIT.json`
- `CITATION_AUDIT.json`

## Assurance Levels

### `draft`

- audits are recommended
- missing audit artifacts do not block the workflow
- useful for exploratory writing and internal iteration

### `submission`

- both mandatory audit artifacts must exist
- both must have valid verdict payloads
- stale artifacts are treated as failures
- blocking verdicts prevent the paper from being called submission-ready

## Allowed Verdicts

- `PASS`
- `WARN`
- `FAIL`
- `NOT_APPLICABLE`
- `BLOCKED`
- `ERROR`

## Blocking Verdicts At Submission

- `FAIL`
- `BLOCKED`
- `ERROR`

`WARN` is non-blocking but should be surfaced.

## Required Artifact Fields

Every audit artifact must contain:

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

These fields are what `scripts/verify_paper_audits.sh` uses to judge whether the paper's assurance layer is complete and current.

## Hash Rules

`audited_input_hashes` should record SHA256 digests for every file the audit consumed.

- use paths relative to the paper directory for files inside the paper directory
- use absolute paths for files outside it

If any of those files change after the audit runs, the audit becomes stale and must be rerun before submission.

## Trace Rules

`trace_path` should point to a non-empty local trace artifact containing the audit prompt, response, or equivalent review evidence. The trace may live under a paper-local `.aris/` directory or another local project path, but it must remain inside the working repository.

## Verifier Contract

`scripts/verify_paper_audits.sh` is the single external check for whether the mandatory audit layer is present and fresh. In `submission` mode it should fail if:

- a mandatory audit artifact is missing
- a required field is missing
- a verdict is invalid
- an audited input hash no longer matches
- the trace path is missing or empty
- a mandatory audit returns `FAIL`, `BLOCKED`, or `ERROR`
