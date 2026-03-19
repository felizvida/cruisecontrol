# Contributing

Thanks for contributing to this OpenCode port of ARIS.

## What Kinds Of Changes Fit Best

This repo is primarily a prompt, workflow, and documentation package. The most valuable contributions usually fall into one of these buckets:

- improve workflow clarity in `.opencode/commands/` or `.opencode/skills/`
- tighten MCP setup and troubleshooting guidance
- improve onboarding docs such as `README.md`, `QUICKSTART.md`, and `AUTO_RESEARCH_GUIDE.md`
- fix repo polish issues in `.github/` and release metadata

## Before You Open A PR

Please make sure your change:

- keeps upstream attribution intact
- stays compatible with the repo's OpenCode-first structure
- does not introduce unrelated generated artifacts into version control
- updates docs when behavior or setup changes

## Local Checks

Before opening a PR:

1. Read the affected docs end to end for consistency.
2. Check `git status` to make sure no local artifacts are included by accident.
3. If you changed setup behavior, verify the commands in the docs still match `opencode.jsonc`.

## Pull Request Notes

- Keep PRs focused and small when possible.
- Explain user-facing impact in plain language.
- Call out machine-specific assumptions explicitly.
- If your change affects release polish, mention whether README, quickstart, release notes, or GitHub metadata were updated.

## Attribution

This repo is a derivative port of the upstream ARIS project. Please preserve existing attribution in `README.md`, `NOTICE.md`, and `UPSTREAM.md`.
