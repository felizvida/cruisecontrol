# Round 01 Review

Reviewed artifact: `paper/main_round1.pdf`

Score: `7.1 / 10`

Verdict: `Weak Borderline`

Main criticisms:

1. The alignment result is strong, but the paper still does not compare that alignment to a naive baseline implied by the underlying regional prevalence. A skeptical reader can still ask whether the marker panel is merely tracking the larger optic-tectum total.
2. Figure 3 hints at robustness, but the manuscript does not yet report the numeric leave-one-out range in the text.
3. The axis-level result would be easier to audit if the expected baseline fractions and observed lifts were written in a small table rather than only described in prose.
4. The results section still leans more on the exact-test headline than on the effect-size interpretation.

Required fixes for Round 02:

1. Compute the expected matched-region fractions under naive regional prevalence and report the observed lift over that baseline.
2. Add an axis-level table with observed alignment fractions, Wilson intervals, expected baseline fractions, and lift.
3. State the leave-one-out robustness range explicitly in the text.
4. Reframe the function-alignment subsection so the effect-size logic is at least as visible as the p-value.
