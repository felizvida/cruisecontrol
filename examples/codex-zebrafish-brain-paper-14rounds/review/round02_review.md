# Round 02 Review

Reviewed artifact: `paper/main_round2.pdf`

Score: `7.5 / 10`

Verdict: `Weak Accept`

Main criticisms:

1. The prevalence-baseline comparison is a real improvement, but the argument is still dominated by count-weighted summaries. A careful reviewer can still ask whether large tectal families such as myosin are carrying most of the alignment story.
2. The paper still does not say explicitly that every curated marker family favors its expected region.
3. The comparison between proteoform-level overlap and protein-level overlap is present in Table 1 but is not yet interpreted as one of the note's substantive takeaways.
4. The appendix still lacks a compact audit trail for the family-level robustness quantities.

Required fixes for Round 03:

1. Add an unweighted family-level consistency analysis, including the fraction of marker families that favor their expected region and a simple sign-style significance check.
2. Report the minimum family-level matched share so the reader can see the weakest case, not only the weighted aggregate.
3. Interpret the protein-versus-proteoform overlap contrast directly in the text.
4. Expose the family-level robustness file more explicitly in the reproducibility appendix.
