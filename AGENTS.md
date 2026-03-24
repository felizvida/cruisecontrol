# OpenCode Port Rules

This repo packages the ARIS research workflow for both OpenCode and Codex.

## Layout

- Skills live in `.opencode/skills/`
- Command wrappers live in `.opencode/commands/`
- Sample OpenCode config lives in `opencode.jsonc`
- A reusable target-project template lives in `templates/project-AGENTS.md`

## Workflow Routes

This repo supports two explicit execution routes:

- **Pure Codex route** — default. Use Codex end to end for planning, critique, writing, and paper-improvement loops.
- **Pure OpenCode route** — opt-in. Use the OpenCode model configured in `opencode.jsonc` for those same phases.

If the user does not explicitly choose a route, use **Codex**.

When the user is inside OpenCode:

- generic workflow commands such as `/research-pipeline`, `/paper-writing`, `/paper-upgrade`, `/research-review`, `/auto-review-loop`, and `/auto-paper-improvement-loop` should default to the Codex route
- explicit `-opencode` command variants select the pure OpenCode route
- explicit `-codex` command variants force the pure Codex route even when running from OpenCode
- inline overrides like `route: opencode` or `route: codex` should be honored when present

Optional MCP integrations such as Zotero or Obsidian are allowed, but they are not required for either core route.

## Project Metadata

Some skills expect the active research project to expose metadata in `AGENTS.md`, especially:

- `## Paper Library`
- `## Remote Server`
- `## Local Environment`
- `## Paper Defaults`

If you are using these skills from another repo, create that repo's `AGENTS.md` from [project-AGENTS.md](templates/project-AGENTS.md).

## Command Behavior

The command files in `.opencode/commands/` are thin wrappers. They exist to recreate the upstream slash-command UX. The actual workflow logic remains in the skill files.

Unless a wrapper explicitly says otherwise, the generic command name should mean the **Codex-default** route.

## Artifact Destinations

All intermediate artifacts, reports, notes, figures, and state files must stay in the current local working repository unless the user explicitly asks to publish or push them elsewhere.

Never invent external GitHub repositories, GitHub URLs, organization names, or remote destinations for outputs. If a skill needs to save something, write it to a local file in the current project root or its existing local subdirectories.

## Paper Evidence Standard

Any paper presented as a final paper package in this repo must be backed by real executable computation that generated the reported results.

- Do not rely on hand-authored benchmark numbers, cosmetic result tables, or placeholder empirical claims for a final paper.
- Use local compute for lightweight pilots, smoke tests, and small simulations.
- Use Biowulf when the work needs serious CPU or GPU capacity. Keep requests moderate and do not exceed one node unless the user explicitly asks for that.
- A complete final paper package still includes the finished PDF and source, round-by-round paper-improvement artifacts, code, data or a source-data manifest, high-resolution figure assets, a detailed review opinion, and a score.
- Do not stop at `paper/main.pdf` if the paper-improvement loop is available. Persist the review opinion, scorecard, and revision history.

## Biowulf Operational Rules

When using Biowulf from this repo:

- never run heavy programs on the frontend node
- use the frontend only to inspect queues, start jobs, and manage files
- load modules inside the compute allocation
- request and use scratch for large transient datasets, caches, checkpoints, and temp outputs
- do not store large datasets or bulky experiment outputs in `$HOME`

## Feishu

This port uses `~/.config/opencode/feishu.json` as the user-level Feishu config path.
