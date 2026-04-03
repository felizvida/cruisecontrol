# Data Package

This humanities example uses a curated source corpus rather than an experimental dataset.

## Included Files

- [curated_corpus.json](curated_corpus.json)
  Hand-built corpus of primary and local-history records used for the paper's computational coding.

- [source_manifest.json](source_manifest.json)
  Machine-readable list of primary and local sources plus generated outputs.

- [corpus_inventory.json](corpus_inventory.json)
  Complete 24-record inventory with stable source URLs and repository identifiers.

- [evidence_traceability.json](evidence_traceability.json)
  Full audit trail preserving the exact excerpts and summaries used in coding.

- [../results/event_timeline.csv](../results/event_timeline.csv)
  Generated event timeline from the corpus.

- [../results/theme_counts.csv](../results/theme_counts.csv)
  Generated lexicon counts for Wilkinson and Jefferson excerpts.

- [../results/network_edges.csv](../results/network_edges.csv)
  Generated weighted network edges from coded source connections.

## Method Note

The numeric outputs in this package do not replace reading the sources. They are reproducible aids for:

1. source coding
2. timeline construction
3. theme counting
4. network visualization

The interpretive claims in the paper remain historical arguments built from those coded sources.

The quickest audit route is:

1. `curated_corpus.json` for the working records
2. `corpus_inventory.json` for the compact citable inventory
3. `evidence_traceability.json` for the exact text snippets used in analysis
