---
description: Iteratively improve a generated paper with external review and recompilation.
---
Load and follow the `auto-paper-improvement-loop` skill from `.opencode/skills/auto-paper-improvement-loop/SKILL.md`.

Use `$ARGUMENTS` as the paper directory or scope.
Default review route: `codex`. For a pure OpenCode loop, append `route: opencode` to `$ARGUMENTS`.
Default external paper review backend: `paperreview.ai` when configured via `PAPERREVIEW_EMAIL` or project `AGENTS.md`; otherwise fall back to the route-local reviewer.
Keep round-to-round continuity in saved review artifacts rather than hidden reviewer state.
