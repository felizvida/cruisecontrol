# Paper Upgrade Sample

This folder documents the intended artifact layout for the linked-paper upgrade workflow.

## Example Invocation

```text
/paper-upgrade "https://arxiv.org/abs/2401.12345 — this is my paper"
```

## Expected Outputs

- `SOURCE_PAPER_NOTES.md`
- `SOURCE_PAPER_REVIEW.md`
- `PRIOR_ART_UPDATE.md`
- `PUBLICATION_DECISION.md`
- `BREAKTHROUGH_PLAN.md`
- `IMPROVEMENT_DIFF.md`
- `NARRATIVE_REPORT.md`
- `UPGRADE_SUMMARY.md`
- `paper/main.pdf`
- `paper/PAPER_IMPROVEMENT_LOG.md`
- `code/`
- `data/`
- `figure_assets/`
- `review/`

## Workflow Promise

The workflow is supposed to do more than polish the prose.

It should:

1. read the linked paper
2. identify what blocks acceptance
3. find a defensible new contribution path
4. refuse to proceed if the result would only be a facelift
5. generate a new polished paper and a clear improvement memo

For a concrete tracked example of this workflow carried all the way to a completed paper package, see [../paper-upgrade-1802-02532/README.md](../paper-upgrade-1802-02532/README.md).

## Guardrail

If the linked paper is not the user's own work, the workflow must not generate a near-copy. It should instead create a clearly new manuscript that cites the source paper and documents what is genuinely new.
