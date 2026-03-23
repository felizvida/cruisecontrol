# ARIS for OpenCode

OpenCode-native port of [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) at upstream commit `e8ab30fdd01cfce03bd1695de9943f629849b792`.

## Attribution

This repository is a derivative packaging of the original ARIS work by the upstream authors at `wanshuiyin/Auto-claude-code-research-in-sleep`.

- Original project: [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)
- Upstream snapshot used here: `e8ab30fdd01cfce03bd1695de9943f629849b792`
- Original license: MIT, preserved in [LICENSE](LICENSE)
- Port-specific changes in this repo: OpenCode command wrappers, OpenCode config scaffolding, repo-level `AGENTS.md`, and compatibility edits for OpenCode paths

See [NOTICE.md](NOTICE.md) and [UPSTREAM.md](UPSTREAM.md) for the exact provenance.

This repo keeps the upstream research skills, ports the few Claude-specific file paths that would break in OpenCode, and adds native OpenCode commands in `.opencode/commands/`.

## What is included

- `.opencode/skills/` — 18 upstream research skills copied from ARIS
- `.opencode/commands/` — OpenCode command wrappers matching the upstream slash commands
- `AGENTS.md` — repo-level instructions for using the port in OpenCode
- `opencode.jsonc` — sample MCP configuration with `codex` enabled by default
- `scripts/codex-mcp-local.sh` — repo-local Codex MCP wrapper that isolates OpenCode from global Codex state on this machine
- `templates/project-AGENTS.md` — project metadata template for GPU servers, paper libraries, and paper defaults
- `UPSTREAM.md` — upstream source snapshot and provenance reference

## Quick Start

1. Open this folder in OpenCode.
2. Review and edit [opencode.jsonc](opencode.jsonc). The `codex` reviewer server is enabled by default; on this machine it runs through `scripts/codex-mcp-local.sh`, which isolates OpenCode from any broken or unrelated global Codex MCP state. Optional `zotero` and `obsidian-vault` entries remain disabled until you configure them.
3. If you want GPU execution or local paper-library lookup in another repo, copy [templates/project-AGENTS.md](templates/project-AGENTS.md) into that project as `AGENTS.md` and fill in the relevant sections.
4. Run commands such as:
   - `/idea-discovery diffusion model efficiency`
   - `/auto-review-loop story draft in current repo`
   - `/paper-writing NARRATIVE_REPORT.md`
   - `/research-pipeline test-time adaptation for robotics`
5. For a step-by-step walkthrough with a concrete example, read [QUICKSTART.md](QUICKSTART.md).
6. For a narrative walkthrough of how the workflow feels in practice, read [AUTO_RESEARCH_GUIDE.md](AUTO_RESEARCH_GUIDE.md).

## Porting Notes

- Upstream `CLAUDE.md` references were changed to `AGENTS.md`.
- Upstream `~/.claude/feishu.json` references were changed to `~/.config/opencode/feishu.json`.
- Skills still mention Claude-style MCP tool handles such as `mcp__codex__codex`. In this port, treat those as instructions to use the `codex` MCP server configured in [opencode.jsonc](opencode.jsonc).
- The upstream repo did not ship actual command files. The command wrappers here are new and map one-to-one to the upstream workflow/skill names.
- For this machine, the `codex` MCP entry uses a repo-local wrapper instead of calling `codex mcp-server` directly. This avoids failures caused by global Codex MCP config and stale Codex state databases.

## Recommended MCP Setup

The original workflow assumes an external reviewer model accessible through a server named `codex`. This port keeps that convention so the copied skill text stays coherent. Optional integrations:

- `codex` — external reviewer for critical review loops
- `zotero` — literature search over a Zotero library
- `obsidian-vault` — note search over an Obsidian vault

`codex` is enabled by default in [opencode.jsonc](opencode.jsonc). This repo also sets `experimental.mcp_timeout` to give longer-running literature and review calls enough time to finish natively in OpenCode. `zotero` and `obsidian-vault` remain scaffolded but disabled by default.

## Community

- [CONTRIBUTING.md](CONTRIBUTING.md) — contribution expectations for docs, skills, and workflow changes
- [SUPPORT.md](SUPPORT.md) — how to ask for help effectively
- [SECURITY.md](SECURITY.md) — how to report security-sensitive issues
- GitHub issue templates and the PR template live under `.github/`

## Upstream

Source repo: [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)

Reference snapshot: [UPSTREAM.md](UPSTREAM.md)
