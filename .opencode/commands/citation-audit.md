---
description: Audit a paper's references for existence, metadata correctness, and claim-context fit.
---
Load and follow the `citation-audit` skill from `.opencode/skills/citation-audit/SKILL.md`.

Use `$ARGUMENTS` as the paper directory or bibliography path.
Default workflow route: `codex`. If the user explicitly wants the pure OpenCode route, honor that with `route: opencode`.
Write the audit artifacts into the local paper directory only.
