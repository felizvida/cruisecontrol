---
name: paperreview-ai-review
description: "Submit a paper PDF to paperreview.ai, wait for the external AI review, and save the returned review, score, token, and raw JSON as local artifacts. Use when the user mentions paperreview.ai or wants the paper-improvement loop to use that external review system."
argument-hint: [paper-pdf-path]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

# paperreview.ai Review Integration

Use this skill when a paper should be reviewed through `paperreview.ai` instead of an internal reviewer pass.

## Best Use Cases

- English-language AI or CS papers
- arXiv-heavy venues and literature
- paper-improvement loops where an external score or external critique is useful

## Current Service Constraints

- PDF only
- max file size: `10MB`
- only the first `15` pages are analyzed
- the numeric `1-10` calibrated score is shown only when the target venue is `ICLR`

These constraints come from the current public site and should be treated as operational limits, not assumptions.

## Required Configuration

The current service requires an email value on submission, but not for later retrieval once you have saved the token.

Resolve it in this order:
1. explicit user instruction
2. `PAPERREVIEW_EMAIL` environment variable
3. project `AGENTS.md` section `## External Review`

If no submission email can be resolved, stop and ask for it or let the caller fall back to a local review path.

## Artifacts To Save

Save all artifacts locally under `review/`:

- `roundNN_paperreview_submission.json`
- `roundNN_paperreview_response.json`
- `roundNN_review.md`
- `roundNN_scorecard.json`

Do not rely on the email notification alone. The current frontend returns the review token directly in the confirm-upload response; persist it in the submission JSON and use that token as the durable retrieval handle.

## Recommended Invocation

Use the bundled script:

```bash
python3 .opencode/skills/paperreview-ai-review/scripts/paperreview_client.py submit-and-wait \
  --pdf paper/main_round0_original.pdf \
  --email "$PAPERREVIEW_EMAIL" \
  --venue ICLR \
  --round-label "Round 00" \
  --artifact paper/main_round0_original.pdf \
  --submission-json review/round00_paperreview_submission.json \
  --review-json review/round00_paperreview_response.json \
  --review-md review/round00_review.md \
  --scorecard-json review/round00_scorecard.json
```

## Integration Notes

- If the target venue is not one of the site’s named venues, pass `Other`.
- If the service returns no numeric score, keep the review and treat the loop as criticism-driven rather than score-driven for that round.
- If you have a token already, you do not need the email again for retrieval.
- If the submission fails because of file size, non-English content, or service availability, let the caller fall back to the local Codex/OpenCode review path rather than fabricating a review.
