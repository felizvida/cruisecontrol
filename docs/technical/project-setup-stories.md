# Setup Stories From Shipping This Repo

This document is a companion to the more surgical MCP write-up in [codex-mcp-lessons-learned.md](codex-mcp-lessons-learned.md).

That other note answers the question, "What exactly broke in the `codex` MCP setup?"

This one answers a different question:

What did it actually feel like to get this project into a shape where it could be trusted?

The lessons below are all technical, but they are easier to remember in story form because that is how they were learned.

## Story 1: The README Promised A Rocket Ship, The Skill Files Described The Engine

At the beginning, the upstream repository looked deceptively simple.

The README made the system feel almost magical. It suggested a smooth path from idea to experiments to paper, with the kind of confidence that makes you think the only missing ingredient is your own ambition.

Then the actual work started.

The first useful pause came from reading the skill files instead of the front-page pitch. The README was aspirational. The `SKILL.md` files were operational. They told the truth about where the workflow actually stopped, what artifacts it expected, and where humans were still assumed to intervene.

That changed the project immediately.

Instead of asking, "Why is the repo failing to do what it said on the tin?" the better question became, "Which layer is describing the real system?"

The answer was: the skill files.

That sounds obvious in hindsight, but it mattered. It kept the port grounded. It meant that when the repo said "single-command pipeline" in one place and "stop after review" in another, the fix was not to argue with the docs. The fix was to promote the actual workflow logic until the docs became true.

The lesson was simple:

In prompt-driven systems, the glossy README is often marketing, but the embedded workflow text is architecture.

## Story 2: A Binary That Worked Perfectly Was Still Part Of A Broken System

One of the more annoying moments in this setup was the stage where `codex` looked fine.

From a shell, it answered politely.

```bash
/opt/homebrew/bin/codex --version
/opt/homebrew/bin/codex mcp-server --help
```

Those commands worked. Which made it tempting to say: good, Codex is installed, let's move on.

But OpenCode kept stalling.

This is the kind of bug that wastes time because it offers the wrong kind of reassurance. The binary was healthy enough to pass a basic smoke test, but the integrated system was still sick. OpenCode was not launching "a binary." It was launching a process inside a live runtime with inherited state, timing assumptions, and extra baggage.

That was the moment the setup stopped looking like a CLI problem and started looking like an application-runtime problem.

Once that mental shift happened, the fix became much clearer:

- pin the path
- isolate the runtime home
- reuse only the auth that was known-good
- define the profiles locally

The deeper lesson was that tooling bugs often survive basic smoke tests because smoke tests usually prove the least interesting thing.

They prove that a command can start.
They do not prove that the surrounding system can trust it.

## Story 3: The Scariest Error Message Was Mostly Theater

There was a moment when the failure trail drifted into remote-host fantasy.

The system started talking about:

- `codex.mcp.internal`
- remote health checks
- service logs
- daemon status

For a minute, that kind of language changes the emotional temperature of the problem. It makes a local setup issue feel like hidden infrastructure, enterprise networking, or a private backend you are not allowed to see.

But the repo was not using a remote MCP service. It was using a local stdio MCP process.

That was the turning point: stop respecting the drama of the error message more than the actual architecture.

Once the architecture won, the fake complexity fell away. There was no mysterious server to ping. There was only a local process being launched with the wrong surrounding state.

This lesson was worth writing down because it generalizes well.

Some failures sound sophisticated because the message leaks vocabulary from a deeper layer of the stack. That does not mean the real bug lives there.

If the architecture says "local process," start local. Every time.

## Story 4: The Best Fix Was To Reuse Less, Not More

A lot of setup work begins with a reasonable instinct: if the user already has a global configuration that mostly works, try to reuse it.

That instinct was wrong here.

The global Codex home was not a neat little bundle of "the useful stuff." It was a messy attic. It contained working auth, yes, but also unrelated integrations, state that had nothing to do with this repo, and the kind of old runtime residue that only becomes visible when another tool inherits it.

The winning move was not full reuse.
It was selective reuse.

Keep the auth file.
Throw away the rest.

That felt almost too simple, but it worked because it respected the difference between identity and environment. Auth is identity. Everything else is behavior. The repo needed the first and mistrusted the second.

That is a pattern worth keeping.

When integrating local tools into a repo-scoped workflow, it is often cleaner to import just enough of the user's existing world to prove identity, then rebuild the runtime around that from scratch.

## Story 5: The Project Became Easier Once Local Trash Had A Home

There is a phase in every automation-heavy repo where the output starts to feel like sprawl.

Reports show up at the root.
Generated files mingle with hand-written ones.
Demo artifacts sit next to docs.
Runtime state turns into accidental source control bait.

That phase happened here too.

The fix was not glamorous. It was mostly about containment:

- `.local_artifacts/`
- `.local_runtime/`
- example folders with their own paper-local `.gitignore`

Once those existed, the repo got calmer. It became much easier to tell the difference between:

- a local scratch run
- a tracked example
- real shipped workflow logic

That calm mattered more than expected. It made iteration less emotionally expensive. You could run things, learn from them, and decide later whether they deserved to become first-class examples.

The lesson was that repository hygiene is not just aesthetic. In an automation-heavy project, it is what keeps experimentation from feeling like vandalism.

## Story 6: A PDF Is Not A Finished Paper

There was a stretch where the pipeline could produce a paper PDF, and that felt like the finish line.

It was not.

The moment the question shifted from "Can it write a paper?" to "Would I trust this as a complete final paper package?" the standard changed.

A real paper package needed more than the PDF:

- the source
- the code that generated the paper-side assets
- the data or source-data manifest
- high-resolution figure exports
- a review opinion
- a score

That change improved the repo in a way the PDF alone never could. It forced the examples to become inspectable, rebuildable, and honest about what they were.

It also exposed a subtle truth: pipelines love to stop at the most photogenic artifact. Humans should not.

The PDF is the easiest thing to point at. It is not necessarily the most complete thing to ship.

## Story 7: The Honest Paper Was Usually The Better Paper

One of the strongest moments in the linked-paper workflow came when the right answer was not "polish harder."

The source paper was real. The ownership was valid. It would have been easy to drift into a glossy rewrite and call that an upgrade.

But the honest read was that a straight empirical refresh would be weak. The better path was a conceptual pivot: reinterpret the older work as an early precursor to a now-active design space, and write a different kind of paper.

That decision felt slower at first, because it meant refusing the most obvious path.

But it produced the better result.

This happened more than once in miniature too. Every time the repo had to choose between:

- a more flattering claim
- and a more defensible one

the defensible one aged better.

That is a setup lesson as much as a writing lesson, because it changes what the automation should optimize for. A research workflow should not be rewarded for producing the most impressive-looking artifact. It should be rewarded for producing the strongest artifact that remains true.

## Story 8: Round Snapshots Turned The Repo From Magic Into Process

The first time a paper compiled cleanly, it was tempting to replace the old draft and move on.

Keeping the round snapshots instead turned out to be the better decision.

Files like:

- `main_round0_original.pdf`
- `main_round1.pdf`
- `main_round2.pdf`
- `main_round3_complete_package.pdf`

made the process legible. You could see the paper becoming less noisy, more honest, more complete.

That did something important to the project. It reduced the sense that the workflow was a black box that somehow emitted polished artifacts. The repo started showing its work.

That matters for trust.

When automation produces something good, people naturally ask: was that luck, hidden manual work, or a reproducible process?

Round snapshots are one of the cleanest answers to that question.

## Story 9: Placeholder Figures Were Better Than Fake Polish

There was a fork in the road around figures.

One option was to fabricate glossy-looking visuals that implied an experimental backend the repo did not actually have.

The other was to keep the placeholders explicit, then elevate them into proper assets:

- standalone source
- vector PDF
- SVG
- high-resolution PNG

The second option was less flashy and much more useful.

It preserved honesty while still making the package feel finished. The figures were no longer pretending to be real experimental diagrams, but they also were not trapped inside the paper source as throwaway boxes. They became deliberate artifacts.

That was a useful reminder that polish does not have to mean illusion.

Sometimes the most professional-looking choice is the one that states the limitation clearly and then packages that limitation well.

## Story 10: The Project Got Better When It Optimized For The Next Person

There is a hidden threshold in projects like this.

At first, success means "I can make it work on my machine."

Then, if the project survives long enough, success changes meaning.
It becomes:

"If someone opens this repo later, can they tell what happened, why it works, and how to rerun it without guessing?"

That threshold changed a lot of decisions here:

- writing technical notes instead of relying on memory
- promoting local demos into tracked examples
- adding manifests and review packets
- linking the docs so the repo tells one coherent story

Once the project started optimizing for the next person, it also became easier to trust for the current person.

That may be the most durable lesson in the whole setup.

The fastest path to a more reliable local workflow is often to package it as though you were about to hand it to somebody else.

## Closing Thought

None of these stories are dramatic in isolation.

They are mostly stories about choosing structure over convenience, truth over polish, and explicit packaging over ambient assumptions.

But that is exactly why they matter.

This project got better every time it became less magical and more inspectable.

That is the kind of lesson worth keeping.
