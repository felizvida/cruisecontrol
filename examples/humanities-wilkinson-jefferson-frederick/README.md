# Humanities Example: Wilkinson, Jefferson, and Frederick

This folder is a complete humanities-paper example for the repo.

## Topic

**James Wilkinson, Thomas Jefferson, and the way Frederick, Maryland turned political protection into legal procedure**

## Outcome

The paper argues that Wilkinson did not survive because Jefferson trusted him as a simple friend.

He survived because:

1. he remained useful to Jefferson in the western theater
2. Jefferson publicly and privately supported him at key moments during the Burr crisis while still allowing formal inquiry
3. Frederick became one of the places where that protection was converted into venue, legal procedure, witness management, and finally acquittal

## Key Artifacts

- [NARRATIVE_REPORT.md](NARRATIVE_REPORT.md)
- [SOURCE_NOTES.md](SOURCE_NOTES.md)
- [LITERATURE_REVIEW_EXPANDED.md](LITERATURE_REVIEW_EXPANDED.md)
- [LITERATURE_GAP_AUDIT.md](LITERATURE_GAP_AUDIT.md)
- [ARCHIVAL_SOURCE_HUNT.md](ARCHIVAL_SOURCE_HUNT.md)
- [DISCOVERY_MEMO.md](DISCOVERY_MEMO.md)
- [code/README.md](code/README.md)
- [data/README.md](data/README.md)
- [data/curated_corpus.json](data/curated_corpus.json)
- [data/corpus_inventory.json](data/corpus_inventory.json)
- [data/evidence_traceability.json](data/evidence_traceability.json)
- [results/event_timeline.csv](results/event_timeline.csv)
- [results/theme_counts.csv](results/theme_counts.csv)
- [results/network_edges.csv](results/network_edges.csv)
- [results/sensitivity_checks.json](results/sensitivity_checks.json)
- [results/summary_metrics.json](results/summary_metrics.json)
- [code/environment_versions.json](code/environment_versions.json)
- [paper/main.pdf](paper/main.pdf)
- [paper/main_round0_original.pdf](paper/main_round0_original.pdf)
- [paper/main_round1.pdf](paper/main_round1.pdf)
- [paper/main_round2.pdf](paper/main_round2.pdf)
- [paper/main_round28.pdf](paper/main_round28.pdf)
- [paper/main_round29.pdf](paper/main_round29.pdf)
- [paper/main_round30.pdf](paper/main_round30.pdf)
- [paper/main_round31.pdf](paper/main_round31.pdf)
- [paper/main_round32.pdf](paper/main_round32.pdf)
- [paper/main_round33.pdf](paper/main_round33.pdf)
- [paper/main_round34.pdf](paper/main_round34.pdf)
- [paper/main_round35.pdf](paper/main_round35.pdf)
- [paper/main_round37.pdf](paper/main_round37.pdf)
- [paper/main_round14.pdf](paper/main_round14.pdf)
- [paper/main_round1_complete_package.pdf](paper/main_round1_complete_package.pdf)
- [paper/PAPER_IMPROVEMENT_LOG.md](paper/PAPER_IMPROVEMENT_LOG.md)
- [figure_assets/README.md](figure_assets/README.md)
- [review/ROUND_REVIEWS.md](review/ROUND_REVIEWS.md)
- [review/ROUND_REVIEWS_LIVE_15_28.md](review/ROUND_REVIEWS_LIVE_15_28.md)
- [review/REVIEW_OPINION.md](review/REVIEW_OPINION.md)
- [review/review_scorecard.json](review/review_scorecard.json)
- [review/round36_review.md](review/round36_review.md)
- [review/round36_scorecard.json](review/round36_scorecard.json)

## Core Historical Claim

The paper's main claim is a local and interpretive one:

- Jefferson and Wilkinson had a relationship of utility, protection, and retrospective esteem
- it was not merely intimate friendship
- Frederick mattered because it was repeatedly useful to Wilkinson's survival
  as a Maryland foothold, as a military-logistical site, and as the place where his 1811-1812 crisis was given venue, witnesses, interrogatories, judgment, and official settlement

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
- `paper/main_round29.pdf` — literature-expansion editorial revision after the source-building pass; not yet rereviewed
- `paper/main_round30.pdf` — Frederick procedural-chain revision after adding new 1811 War Department and interrogatory records; not yet rereviewed
- `paper/main_round31.pdf` — historiographical integration revision after adding military-justice, War Department, and Frederick legal-context scholarship; not yet rereviewed
- `paper/main_round32.pdf` — archival-source integration revision after adding the court-martial pamphlet lead, Frederick newspaper abstract route, and stronger Taney/Frederick sourcing; not yet rereviewed
- `paper/main_round33.pdf` — local-newspaper integration revision after folding the Thomas/Frederick-Town Herald evidence into the Frederick legal-culture argument; not yet rereviewed
- `paper/main_round34.pdf` — source-packet integration revision after adding the 1800 Frederick Town War Department receipt, Jefferson's January 1808 inquiry message, and stronger repository guidance for the Jefferson papers and Frederick print record; not yet rereviewed
- `paper/main_round35.pdf` — thesis-reframing revision after recentering the paper on Frederick as the place where executive protection became procedure
- `review/round36_review.md` — external `paperreview.ai` review of `paper/main_round35.pdf`, returned `Accept` and asked for stronger auditability, small robustness checks, and a clearer proceedings note
- `paper/main_round37.pdf` — response revision after `round36`, adding full corpus inventory and traceability files, sensitivity checks, environment capture, and a stronger note on the formal proceedings; not yet rereviewed
- `paper/main.pdf` — current version, equal to `paper/main_round37.pdf`
- `review/ROUND_REVIEWS.md` — reconstructed round-by-round review opinions for rounds 0--14
- `review/ROUND_REVIEWS_LIVE_15_28.md` — live round-by-round review opinions for rounds 15--28

The older [paper/main_round1_complete_package.pdf](paper/main_round1_complete_package.pdf) snapshot is preserved as a legacy freeze from the earlier one-shot package build.
