# OpenCode Port Rules

This repo is an OpenCode-native packaging of the ARIS research workflow.

## Layout

- Skills live in `.opencode/skills/`
- Command wrappers live in `.opencode/commands/`
- Sample OpenCode config lives in `opencode.jsonc`
- A reusable target-project template lives in `templates/project-AGENTS.md`

## MCP Compatibility

Several upstream skills embed Claude-style tool names such as `mcp__codex__codex` and `mcp__codex__codex-reply`. In this repo, interpret those as references to the MCP server named `codex`.

If you rename that server in `opencode.jsonc`, update the copied skills or keep a server alias named `codex`.

## Project Metadata

Some skills expect the active research project to expose metadata in `AGENTS.md`, especially:

- `## Paper Library`
- `## Remote Server`
- `## Local Environment`
- `## Paper Defaults`

If you are using these skills from another repo, create that repo's `AGENTS.md` from [project-AGENTS.md](templates/project-AGENTS.md).

## Command Behavior

The command files in `.opencode/commands/` are thin wrappers. They exist to recreate the upstream slash-command UX. The actual workflow logic remains in the skill files.

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
