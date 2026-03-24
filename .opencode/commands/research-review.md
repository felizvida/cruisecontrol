---
description: Request a deep research review of ideas, results, or drafts.
---
Load and follow the `research-review` skill from `.opencode/skills/research-review/SKILL.md`.

Use `$ARGUMENTS` as the review scope.
Default review route: `codex`. For a pure OpenCode review pass, append `route: opencode` to `$ARGUMENTS`.
If `$ARGUMENTS` includes an explicit save path or asks you to save the review to a file, you must write the final review to that exact path before replying.
Write review outputs to local project files only. Never invent external GitHub repositories or URLs as output targets.
