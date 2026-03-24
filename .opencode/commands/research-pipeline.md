---
description: Run the end-to-end research pipeline from direction to a review-improved paper package.
---
Load and follow the `research-pipeline` skill from `.opencode/skills/research-pipeline/SKILL.md`.

Use `$ARGUMENTS` as the research direction.
Default workflow route: `codex`. If the user explicitly wants the pure OpenCode route, honor that or use `/research-pipeline-opencode`.
Auto-proceed through checkpoints unless the user explicitly asked to approve each stage.
Keep every artifact, checkpoint, and summary in the current local repository. Never invent external GitHub repositories or URLs for outputs.
Expect the paper stage to continue past compilation into scored review-and-revision rounds.
