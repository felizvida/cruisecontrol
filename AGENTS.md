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

If you are using these skills from another repo, create that repo's `AGENTS.md` from [project-AGENTS.md](/Users/liux17/codex/autoresearch/templates/project-AGENTS.md).

## Command Behavior

The command files in `.opencode/commands/` are thin wrappers. They exist to recreate the upstream slash-command UX. The actual workflow logic remains in the skill files.

## Artifact Destinations

All intermediate artifacts, reports, notes, figures, and state files must stay in the current local working repository unless the user explicitly asks to publish or push them elsewhere.

Never invent external GitHub repositories, GitHub URLs, organization names, or remote destinations for outputs. If a skill needs to save something, write it to a local file in the current project root or its existing local subdirectories.

## Feishu

This port uses `~/.config/opencode/feishu.json` as the user-level Feishu config path.
