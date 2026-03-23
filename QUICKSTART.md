# Quick Start

Use this if you want the shortest path from clone to first useful result.

## 1. Open the repo

```bash
git clone https://github.com/felizvida/cruisecontrol
cd cruisecontrol
opencode
```

## 2. Confirm Codex is wired in

This repo expects a local MCP server named `codex`.

Check [opencode.jsonc](opencode.jsonc). On this machine it should point to:

```json
"command": ["/bin/bash", "/Users/liux17/codex/autoresearch/scripts/codex-mcp-local.sh"]
```

That wrapper keeps OpenCode's `codex` server isolated from your global Codex MCP config and stale local Codex state.

## 3. Run one command

In OpenCode, start with:

```text
/idea-discovery "test-time adaptation for battery-constrained quadruped robots"
```

## 4. What you should get

A good first run gives you:

- a local `IDEA_REPORT.md`
- 2-5 ranked ideas
- novelty warnings
- one recommended next step

If you want to see a sample artifact set first, read [examples/end-to-end-sample/README.md](examples/end-to-end-sample/README.md).

## 5. Keep going

If the report looks promising, the next command is usually:

```text
/auto-review-loop "best idea from IDEA_REPORT.md"
```

If you want the full workflow story instead of the minimal path, read [AUTO_RESEARCH_GUIDE.md](AUTO_RESEARCH_GUIDE.md).

## 6. If it fails

Check these first:

- `codex` is installed at `/opt/homebrew/bin/codex`
- the `codex` MCP server is visible in OpenCode
- OpenCode picked up the repo's `opencode.jsonc`, including `experimental.mcp_timeout`
- you are not missing project-specific setup in `AGENTS.md` when running against another repo

If you want to use these skills inside a different research repo, copy [templates/project-AGENTS.md](templates/project-AGENTS.md) into that repo as `AGENTS.md`.
