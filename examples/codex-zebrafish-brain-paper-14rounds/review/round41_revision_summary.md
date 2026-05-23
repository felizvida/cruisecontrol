# Round 41 Revision Summary

Route: pure Codex

Skills applied: updated local `paper-write` guidance plus the default `classic-biology-prose` voice.

This round rewrote the current Zebrafish example paper as a direct biological manuscript rather than as a workflow-flavored reanalysis note. The central claim set is unchanged: adult zebrafish telencephalon and optic tectum have sharply distinct intact-proteoform profiles; the marker direction follows known regional biology; and the acetylation asymmetry remains provisional after detectability-sensitive checks.

Main edits:

- Retitled the manuscript to `Distinct Proteoform Profiles Mark Adult Zebrafish Telencephalon and Optic Tectum`.
- Rewrote the abstract without citations and with the headline evidence in a tighter biological order.
- Rebuilt the introduction around the scientific question, identifier granularity, and regional function.
- Reframed methods around source material, exact accession-plus-proteoform identity, robustness checks, and the bounded acetylation analysis.
- Tightened results prose while preserving all numerical claims and their source-derived metrics.
- Rewrote the discussion and conclusion for a calmer, clearer biological interpretation.
- Compressed the technical appendix into the formulas, detectability checks, marker rules, acetylation model, and public-file limits needed to audit the paper.

Compiled artifact:

- `paper/main.pdf`
- `paper/main_round41.pdf`

Validation:

- LaTeX build succeeded with `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`.
- PDF total: 11 pages.
- References start on page 9.
- No undefined-reference, undefined-citation, overfull-box, or `[VERIFY]` markers were found in the build checks.
- All fonts reported by `pdffonts` are embedded.
