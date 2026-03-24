# Humanities Example: Wilkinson, Jefferson, and Frederick

This folder is a complete humanities-paper example for the repo.

## Topic

**James Wilkinson's personal relationship with Thomas Jefferson and the political mechanics of his survival, with special attention to Frederick, Maryland**

## Outcome

The paper argues that Wilkinson did not survive because Jefferson trusted him as a simple friend.

He survived because:

1. he remained useful to Jefferson in the western theater
2. Jefferson publicly and privately supported him at key moments during the Burr crisis
3. Frederick became one of the places where scandal could be converted into procedure, legal defense, and finally acquittal

## Key Artifacts

- [NARRATIVE_REPORT.md](NARRATIVE_REPORT.md)
- [SOURCE_NOTES.md](SOURCE_NOTES.md)
- [DISCOVERY_MEMO.md](DISCOVERY_MEMO.md)
- [code/README.md](code/README.md)
- [data/README.md](data/README.md)
- [data/curated_corpus.json](data/curated_corpus.json)
- [results/event_timeline.csv](results/event_timeline.csv)
- [results/theme_counts.csv](results/theme_counts.csv)
- [results/network_edges.csv](results/network_edges.csv)
- [results/summary_metrics.json](results/summary_metrics.json)
- [paper/main.pdf](paper/main.pdf)
- [paper/main_round0_original.pdf](paper/main_round0_original.pdf)
- [paper/main_round1.pdf](paper/main_round1.pdf)
- [paper/main_round2.pdf](paper/main_round2.pdf)
- [paper/main_round28.pdf](paper/main_round28.pdf)
- [paper/main_round14.pdf](paper/main_round14.pdf)
- [paper/main_round1_complete_package.pdf](paper/main_round1_complete_package.pdf)
- [paper/PAPER_IMPROVEMENT_LOG.md](paper/PAPER_IMPROVEMENT_LOG.md)
- [figure_assets/README.md](figure_assets/README.md)
- [review/ROUND_REVIEWS.md](review/ROUND_REVIEWS.md)
- [review/ROUND_REVIEWS_LIVE_15_28.md](review/ROUND_REVIEWS_LIVE_15_28.md)
- [review/REVIEW_OPINION.md](review/REVIEW_OPINION.md)
- [review/review_scorecard.json](review/review_scorecard.json)

## Core Historical Claim

The paper's main claim is a local and interpretive one:

- Jefferson and Wilkinson had a relationship of utility, protection, and retrospective esteem
- it was not merely intimate friendship
- Frederick mattered because it was repeatedly useful to Wilkinson's survival
  as a Maryland foothold, as a military-logistical site, and as the venue where his 1811-1812 crisis became survivable

## Computation Role

This example includes real computation even though it is a humanities study.

The scripts:

1. code a curated corpus of primary and local-history sources
2. build a reproducible event timeline
3. count thematic language in the surviving excerpts
4. generate a weighted relationship network
5. render the paper tables and figures from those outputs
6. compute an explicit evidence ladder showing how much of the Frederick claim rests on direct documentary records versus contextual local sources

The computations support the historical argument. They do not replace source reading.

## Review Loop Refresh

This example now preserves two linked review-improvement histories:

- `paper/main_round0_original.pdf` — original package before the refresh pass
- `paper/main_round1.pdf` through `paper/main_round14.pdf` — the first serialized improvement pass, with its reconstructed review chain in `review/ROUND_REVIEWS.md`
- `paper/main_round15.pdf` through `paper/main_round28.pdf` — the new live continuation loop, with fresh round-by-round reviews in `review/ROUND_REVIEWS_LIVE_15_28.md`
- `paper/main.pdf` — final version, equal to `paper/main_round28.pdf`
- `review/ROUND_REVIEWS.md` — reconstructed round-by-round review opinions for rounds 0--14
- `review/ROUND_REVIEWS_LIVE_15_28.md` — live round-by-round review opinions for rounds 15--28

The older [paper/main_round1_complete_package.pdf](paper/main_round1_complete_package.pdf) snapshot is preserved as a legacy freeze from the earlier one-shot package build.
