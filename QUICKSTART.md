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
/research-pipeline "test-time adaptation for battery-constrained quadruped robots"
```

## 4. What you should get

A good full run gives you:

- `IDEA_REPORT.md`
- `AUTO_REVIEW.md`
- `NARRATIVE_REPORT.md`
- `paper/main.pdf`
- `paper/PAPER_IMPROVEMENT_LOG.md`

That is the paper-draft stage. In this repo, a **complete** final paper package should also include:

- results generated from real executable computation
- code used to build or support the paper
- sample data or a source-data manifest
- a dedicated high-resolution figure folder
- a detailed review opinion
- a score

If the claimed results need more compute than this machine can provide, move the heavy run to Biowulf and bring the resulting artifacts back into the local paper package.

If you want to see a sample artifact set first, read [examples/end-to-end-sample/README.md](examples/end-to-end-sample/README.md).
If you want the full sample ending in a complete paper package, read [examples/full-paper-sample/README.md](examples/full-paper-sample/README.md).
If you want to start from an existing paper on the internet instead of a fresh research direction, use `/paper-upgrade "paper-url — this is my paper"` and see [examples/paper-upgrade-sample/README.md](examples/paper-upgrade-sample/README.md).
If you want a concrete linked-paper upgrade that ends in a completed package, read [examples/paper-upgrade-1802-02532/README.md](examples/paper-upgrade-1802-02532/README.md).

## 5. Keep going

If you want the full workflow story instead of the minimal path, read [AUTO_RESEARCH_GUIDE.md](AUTO_RESEARCH_GUIDE.md).

## 6. If it fails

Check these first:

- `codex` is installed at `/opt/homebrew/bin/codex`
- the `codex` MCP server is visible in OpenCode
- OpenCode picked up the repo's `opencode.jsonc`, including `experimental.mcp_timeout`
- you are not missing project-specific setup in `AGENTS.md` when running against another repo

If you want to use these skills inside a different research repo, copy [templates/project-AGENTS.md](templates/project-AGENTS.md) into that repo as `AGENTS.md`.
