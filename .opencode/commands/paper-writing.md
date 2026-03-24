---
description: Run the full paper-writing pipeline from narrative report to a review-improved paper package.
---
Load and follow the `paper-writing` skill from `.opencode/skills/paper-writing/SKILL.md`.

Use `$ARGUMENTS` as the narrative report path or paper topic.
Default workflow route: `codex`. If the user explicitly wants the pure OpenCode route, honor that or use `/paper-writing-opencode`.
Auto-proceed through checkpoints unless the user explicitly asked to review each phase.
Write papers, figures, and supporting artifacts to local project files only. Never invent external GitHub repositories or URLs as destinations.
Do not stop at `paper/main.pdf` if the improvement loop can run; persist the score-driven revision artifacts too.
