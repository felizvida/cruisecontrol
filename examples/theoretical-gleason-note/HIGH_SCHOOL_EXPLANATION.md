# High-School Explanation

This note is about a very simple question:

If a rule has to split nicely when we break something into pieces, how much freedom does that rule really have?

The answer turns out to be: not much.

## The Toy Version

Imagine a machine that gives a score to any number between `0` and `1`.

Call the score of `x` by the name `h(x)`.

Suppose the machine always obeys:

`h(x+y) = h(x) + h(y)` whenever `x+y <= 1`.

Also suppose the scores never blow up to infinity. They stay bounded.

Then the machine is forced to be a straight-line rule:

`h(x) = c x`

for some constant `c`.

Why?

1. `h(0)` has to be `0`, because `h(0)=h(0)+h(0)`.
2. If you cut `1` into `n` equal pieces, each piece must have score `h(1)/n`.
3. So every rational number already has the only score it could possibly have.
4. Boundedness prevents wild jumps between nearby numbers.
5. That means the rule on all real numbers must match the straight line that already works on the rationals.

That is the whole engine of the paper.

## The Three-Number Version

Now suppose a new rule `g` has the property that whenever three numbers add to `1`,

`g(a) + g(b) + g(c) = 1`.

Then `g` also has almost no freedom. It must look like

`g(t) = beta + alpha t`.

In plain language: once the rule has to behave nicely on every triple that fills up the whole amount `1`, it has to become an affine rule, meaning "constant plus slope times input."

## The Sphere Picture

On a sphere, take a fixed "north pole" direction `p`.

For any point `u` on the sphere, look at `(u dot p)^2`.

That number measures how much of `u` points toward the pole. It is like a squared shadow length.

Now take three perpendicular directions `u`, `v`, and `w`.

A basic geometry fact says:

`(u dot p)^2 + (v dot p)^2 + (w dot p)^2 = 1`.

So if a rule on the sphere only depends on this squared shadow length, and the three values for every perpendicular triple must add to `1`, then the rule has to be

`constant + slope * squared shadow length`.

That already looks a lot like the kind of formula that appears in quantum theory, but we reached it with only geometry and algebra.

## The Matrix Version

The paper then climbs one more step.

Instead of assigning numbers to points on a sphere, we assign numbers to certain matrices called effects. The rule must still split nicely over sums:

`f(E + F) = f(E) + f(F)`.

Once again, bounded additivity squeezes out almost all freedom.

The paper shows that the only possible rule is

`f(E) = tr(rho E)`.

You do not need to think of that as mysterious physics notation. It is just the matrix version of "the rule has to be linear."

## What Is New Here

This example does **not** claim a new proof of Gleason's original theorem.

What it does claim is:

1. a very simple one-variable core idea
2. a sphere version that is easy to picture
3. a clean matrix theorem proved without physics language

So the big message is:

Rigid splitting rules force straight-line behavior.

First for numbers.
Then for sphere shadows.
Then for matrices.
