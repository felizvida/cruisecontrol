# Quick Start

Use this if you want the shortest path from clone to first useful result.

## 1. Open the repo

Default route from this point forward: **Pure Codex**.

```bash
git clone https://github.com/felizvida/cruisecontrol
cd cruisecontrol
```

## 2. Choose a route

### Default: Pure Codex

Open the repo in Codex and ask for the workflow directly:

```text
Run the Codex research pipeline for: test-time adaptation for battery-constrained quadruped robots
```

### Optional: Pure OpenCode

If you want the OpenCode-native route, start OpenCode:

```bash
opencode
```

Then check [opencode.jsonc](opencode.jsonc). On this machine it should pin the native OpenCode model:

```json
"model": "amazon-bedrock/amazon.nova-premier-v1:0",
"small_model": "amazon-bedrock/amazon.nova-premier-v1:0"
```

The pure OpenCode route does not require a reviewer MCP server. Optional `zotero` and `obsidian-vault` integrations stay disabled unless you configure them.

## 3. Run one command

For the default Codex route in Codex itself:

```text
Run the Codex research pipeline for: test-time adaptation for battery-constrained quadruped robots
```

If you are in OpenCode and still want the default Codex route:

```text
/research-pipeline "test-time adaptation for battery-constrained quadruped robots"
```

For the explicit OpenCode route:

```text
/research-pipeline-opencode "test-time adaptation for battery-constrained quadruped robots"
```

For structured workflow or architecture figures later in the paper process:

```text
/figure-spec "workflow from narrative report to reviewed paper package"
```

## 4. What you should get

A good full run gives you:

- `IDEA_REPORT.md`
- `AUTO_REVIEW.md`
- `NARRATIVE_REPORT.md`
- `paper/main.pdf`
- `paper/main_round0_original.pdf`
- `paper/main_round1.pdf`
- `paper/main_round2.pdf`
- `paper/PAPER_IMPROVEMENT_LOG.md`
- `review/REVIEW_OPINION.md`
- `review/review_scorecard.json`

That is the review-improved paper stage, not just the first compiled draft. In this repo, a **complete** final paper package should also include:

- results generated from real executable computation
- code used to build or support the paper
- sample data or a source-data manifest
- a dedicated high-resolution figure folder
- the detailed review opinion and score shown above

If the claimed results need more compute than this machine can provide, move the heavy run to Biowulf and bring the resulting artifacts back into the local paper package.

By default, the paper-writing route now uses [classic-biology-prose](.opencode/skills/classic-biology-prose/SKILL.md), so the manuscript should read like an authoritative human paper rather than a workflow transcript, project report, or set of homework notes.

If you want the paper treated as submission-ready, run the assurance layer after the last revision:

```text
/paper-claim-audit "paper/"
/citation-audit "paper/"
```

Then verify:

```bash
bash scripts/verify_paper_audits.sh paper --assurance submission
```

If you want to see a sample artifact set first, read [examples/end-to-end-sample/README.md](examples/end-to-end-sample/README.md).
If you want the full sample ending in a complete paper package, read [examples/full-paper-sample/README.md](examples/full-paper-sample/README.md).
If you want to start from an existing paper on the internet instead of a fresh research direction, use `/paper-upgrade "paper-url — this is my paper"` and see [examples/paper-upgrade-sample/README.md](examples/paper-upgrade-sample/README.md).

For route details and explicit command variants, read [WORKFLOW_ROUTES.md](WORKFLOW_ROUTES.md).

## 5. Keep going

If you want the full workflow story instead of the minimal path, read [AUTO_RESEARCH_GUIDE.md](AUTO_RESEARCH_GUIDE.md).

## 6. If it fails

Check these first:

- OpenCode picked up the repo's `opencode.jsonc`
- the configured `model` and `small_model` are available on this machine
- any optional MCP server you enabled is visible in OpenCode
- you are not missing project-specific setup in `AGENTS.md` when running against another repo

If you want to use these skills inside a different research repo, copy [templates/project-AGENTS.md](templates/project-AGENTS.md) into that repo as `AGENTS.md`.
