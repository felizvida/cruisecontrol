# Upstream Reference

- Repository: [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)
- Cloned on: 2026-03-13
- Commit: `e8ab30fdd01cfce03bd1695de9943f629849b792`
- Latest upstream HEAD checked: 2026-05-21 at `b32635e1e9a53d6ff75ef50fd14220cc2c5df4e2`

Cherry-picked ideas from the newer upstream line that are now integrated locally include:

- `citation-audit`
- `paper-claim-audit`
- `figure-spec`
- `experiment-queue`
- a lightweight paper-audit verifier
- skill-local helper ownership for `figure-spec` and `experiment-queue`, with top-level compatibility shims

Notable upstream ideas reviewed but not wholesale imported into this port:

- `render-html`, `paper-talk`, `slides-polish`, `resubmit-pipeline`, and `kill-argument` are useful but need route-aware Codex/OpenCode adaptation before vendoring.
- The upstream Codex/Claude/Copilot install chains are intentionally not copied wholesale; this repo keeps a smaller OpenCode/Codex surface.

During porting, a local upstream clone was used for comparison and updates. That working directory is not included in normal clones of this repository.
