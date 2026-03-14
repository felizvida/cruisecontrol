---
description: Run the multi-round autonomous research review loop.
---
Load and follow the `auto-review-loop` skill from `.opencode/skills/auto-review-loop/SKILL.md`.

Use `$ARGUMENTS` as the topic or scope.
Persist review state as the skill requires and stop at explicit approval gates.
Keep all review artifacts local to the current repository. Never invent external GitHub repositories or URLs as destinations for intermediate results.
