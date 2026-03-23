# Lessons Learned: Stabilizing `codex` MCP in OpenCode on This Machine

This note documents a real setup failure we hit while trying to run the ARIS workflow natively in OpenCode with a local `codex` MCP server.

It is written as a technical lessons-learned document rather than a marketing summary. The goal is simple: if the same failure shows up again, we should not have to rediscover the fix from scratch.

## Executive Summary

The short version is that `codex` itself was installed and working, but OpenCode's MCP integration was unstable because the launched `codex mcp-server` process inherited problematic global Codex state.

The stable fix was:

1. stop calling `codex mcp-server` directly from OpenCode
2. launch it through a repo-local wrapper
3. give that wrapper an isolated `CODEX_HOME`
4. reuse only the working auth file from `~/.codex/auth.json`
5. define the workflow-specific profiles we actually needed
6. increase OpenCode's MCP timeout for long-running review and literature calls

That is the setup currently encoded in:

- [scripts/codex-mcp-local.sh](../../scripts/codex-mcp-local.sh)
- [opencode.jsonc](../../opencode.jsonc)

## The Symptom Pattern

The failure did not present as one clean error. It came through a sequence of misleading signals:

### Symptom 1: `codex` looked installed, but MCP still stalled

From a shell, the basic checks worked:

```bash
/opt/homebrew/bin/codex --version
/opt/homebrew/bin/codex mcp-server --help
```

That ruled out a missing binary and a totally broken install.

### Symptom 2: the model hallucinated remote-server debugging advice

At one point the runtime produced advice about:

- `codex.mcp.internal`
- `curl https://codex.mcp.internal/health`
- `systemctl status codex`
- `/var/log/codex/server.log`

That was a red herring.

In this repo, `codex` is configured as a **local stdio MCP process**, not as a remote daemon. Anything that assumes a managed service on a host like `codex.mcp.internal` is diagnosing the wrong architecture.

### Symptom 3: the visible failure looked like a network timeout

The most concrete failure looked like this:

```text
CodexError(code="E_NETWORK_TIMEOUT", message="Connection to codex.mcp.internal:443 timed out after 30s")
```

That message was easy to misread.

What it actually meant in practice was not "OpenCode is trying to reach some MCP server you should ping." It meant:

1. OpenCode successfully launched the local `codex` MCP process
2. that `codex` process then tried to reach its own backend
3. the launched process was doing so in a broken local state/config environment

So the network-looking error was downstream of a local process-launch problem.

## What Was Actually Broken

The real issue was not one thing. It was a stack of smaller problems:

### 1. OpenCode was inheriting global Codex state

When OpenCode launched `codex mcp-server` directly, the process inherited the user's normal Codex home and configuration.

That meant the MCP server was not running in a controlled, repo-specific environment.

### 2. The global Codex state was noisy and partially broken

The inherited global state included:

- unrelated Codex-side MCP configuration
- extra integrations that were irrelevant to this repo
- a broken or stale Codex state database

In practice, that made the launched MCP server much less predictable than the simple command line suggested.

### 3. The workflow expected named profiles that were not guaranteed to exist globally

The ARIS/OpenCode workflow depends on profile-like behavior for tasks such as:

- `research-lit`
- `idea-discovery`
- `research-review`
- `research-pipeline`
- `paper-writing`

Even after isolating the runtime, missing or inconsistent profile definitions were still causing friction.

### 4. Long-running MCP calls were timing out too aggressively

Even once the process could start cleanly, literature and review calls were still vulnerable to timeouts because the default MCP timeout was too short for this workflow.

## The Fix We Shipped

The stable fix has two parts: a wrapper and an OpenCode config change.

### Part 1: isolate `CODEX_HOME`

The wrapper at [scripts/codex-mcp-local.sh](../../scripts/codex-mcp-local.sh) now:

1. creates a repo-local Codex home under `.local_runtime/codex-home`
2. checks that `~/.codex/auth.json` exists
3. symlinks only that auth file into the isolated runtime
4. writes a fresh `config.toml` with the profiles this repo needs
5. launches `/opt/homebrew/bin/codex mcp-server` with that isolated `CODEX_HOME`

This is the key design decision: **reuse working auth, but do not reuse the rest of the user's global Codex runtime state**.

### Part 2: point OpenCode at the wrapper, not the raw binary

The `codex` entry in [opencode.jsonc](../../opencode.jsonc) now uses:

```json
"command": ["/bin/bash", "/Users/liux17/codex/autoresearch/scripts/codex-mcp-local.sh"]
```

and the repo also sets:

```json
"experimental": {
  "mcp_timeout": 600000
}
```

That did two things:

- removed dependence on ambient global Codex state
- gave long-running MCP calls enough time to complete

## Why The Wrapper Helped So Much

The wrapper fixed more than one class of problem at once.

### It made the runtime deterministic

Before the wrapper, OpenCode was effectively saying "run whatever `codex` means in the current environment."

After the wrapper, it became:

1. use this binary
2. use this isolated home
3. use this auth
4. use these profiles

That turned a vague integration into a reproducible local subsystem.

### It reduced accidental dependency on unrelated MCP integrations

If the user's normal Codex environment has extra MCP integrations configured, those may be useful globally but they are not part of this repo's runtime contract.

The wrapper prevents those unrelated integrations from interfering with OpenCode's use of `codex` for this workflow.

### It gave the repo a place to encode workflow-specific profiles

The research workflow is not a generic chat setup. Some stages want:

- lower latency
- web search enabled
- different reasoning effort

Encoding those decisions in the wrapper's generated `config.toml` made the runtime consistent with the commands and skills shipped in the repo.

## Practical Debugging Heuristics

These were the most useful lessons during diagnosis.

### 1. Separate "can the binary start?" from "can the workflow run?"

These are different questions.

This check only answers the first:

```bash
/opt/homebrew/bin/codex mcp-server --help
```

It does **not** prove that the launched MCP process will behave correctly inside OpenCode.

### 2. Treat remote-host advice skeptically when the MCP server is local

If your config says:

```json
"type": "local"
```

then debugging should start with:

- process launch
- local config inheritance
- auth
- timeout behavior

not with `systemctl`, daemon logs, or remote health endpoints.

### 3. Prefer absolute paths for GUI-launched tools

On macOS, GUI app launches often do not inherit the same `PATH` that an interactive shell sees.

Using absolute paths for:

- the `codex` binary
- the wrapper script

removes one whole class of ambiguity.

### 4. Isolate auth from state

Authentication state is useful.
Everything else may be accidental coupling.

Reusing `auth.json` while rebuilding the runtime around it turned out to be the cleanest compromise.

### 5. Long-running review loops need explicit timeout budgeting

Research-literature and review calls are not tiny request/response interactions.

If the toolchain is expected to support those workflows, timeout configuration must reflect that.

## Current Known-Good Setup

On this machine, the known-good pattern is:

1. `opencode.jsonc` launches the wrapper
2. the wrapper launches `/opt/homebrew/bin/codex mcp-server`
3. `CODEX_HOME` is isolated under `.local_runtime/codex-home`
4. auth is reused from `~/.codex/auth.json`
5. workflow profiles are generated locally by the wrapper
6. OpenCode uses a raised MCP timeout

That setup has already been used to run native OpenCode flows successfully in this repo.

## Operational Checklist

If the MCP setup breaks again, check these in order:

1. Does `/opt/homebrew/bin/codex --version` work?
2. Does `/opt/homebrew/bin/codex mcp-server --help` work?
3. Does `~/.codex/auth.json` exist?
4. Does [opencode.jsonc](../../opencode.jsonc) still point at [scripts/codex-mcp-local.sh](../../scripts/codex-mcp-local.sh)?
5. Does `.local_runtime/codex-home/config.toml` get generated correctly after launch?
6. Did anyone revert `experimental.mcp_timeout` to a shorter value?
7. Is the failure coming from local launch, auth, or backend timeout? Do not collapse those into one bucket.

## What We Would Do Differently Next Time

If starting from scratch, the better setup path would have been:

1. assume global Codex state is not safe to inherit
2. isolate `CODEX_HOME` immediately
3. use a wrapper from day one
4. set explicit research workflow profiles up front
5. validate with a native `opencode run --command research-lit ...` smoke test early

That would have saved time and avoided several rounds of misleading diagnosis.

## Bottom Line

The main lesson is not "Codex MCP is flaky."

The lesson is that local MCP integrations become much more reliable when they are treated like application runtime dependencies rather than ambient CLI conveniences.

In practice, that means:

- pin the binary path
- isolate runtime state
- reuse only the auth you need
- encode the profiles the workflow actually expects
- budget timeout explicitly

That is the difference between "it works in a shell sometimes" and "the repo can rely on it."
