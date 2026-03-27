# Workflow Routes

This repo supports two end-to-end execution routes.

Route selection and paper-review backend selection are separate:

- the route controls whether the workflow body runs through **Codex** or **OpenCode**
- the paper-improvement loop now prefers **paperreview.ai** as its external reviewer when configured, with local fallback if needed
- the default prose style is shared across both routes through [classic-biology-prose](.opencode/skills/classic-biology-prose/SKILL.md), unless the user explicitly asks for another voice

## Default: Pure Codex

This is the default route from this point forward.

Use it when you want the full research lifecycle to run through Codex for planning, critique, writing, and paper-improvement loops.

### In Codex

Open the repo in Codex and ask for the workflow directly, for example:

```text
Run the Codex research pipeline for: budgeted test-time adaptation for quadruped robots
```

or

```text
Run the Codex paper-writing workflow for: NARRATIVE_REPORT.md
```

### In OpenCode

The generic commands should default to Codex:

```text
/research-pipeline "topic"
/paper-writing "NARRATIVE_REPORT.md"
/paper-upgrade "https://arxiv.org/abs/.... — this is my paper"
```

If you want to be explicit, use:

```text
/research-pipeline-codex "topic"
/paper-writing-codex "NARRATIVE_REPORT.md"
/paper-upgrade-codex "paper-url — this is my paper"
```

## Optional: Pure OpenCode

Use this route when you want the workflow to stay entirely inside OpenCode and its configured backend model.

On this machine, that backend is pinned in [opencode.jsonc](opencode.jsonc):

```json
"model": "amazon-bedrock/amazon.nova-premier-v1:0",
"small_model": "amazon-bedrock/amazon.nova-premier-v1:0"
```

Use the explicit OpenCode wrappers:

```text
/research-pipeline-opencode "topic"
/paper-writing-opencode "NARRATIVE_REPORT.md"
/paper-upgrade-opencode "paper-url — this is my paper"
```

## Direct Review Commands

Lower-level commands default to Codex too:

```text
/research-review "scope"
/auto-review-loop "scope"
/auto-paper-improvement-loop "paper/"
```

If you need the pure OpenCode route for a lower-level command, append an inline override:

```text
/research-review "scope — route: opencode"
/auto-review-loop "scope — route: opencode"
/auto-paper-improvement-loop "paper/ — route: opencode"
```

## Practical Recommendation

- Use **Codex** when you care most about end-to-end research quality and paper quality.
- Use **OpenCode** when you want to validate the native OpenCode workflow itself.
- Be explicit in saved artifacts about which route produced them.
