#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
RUNTIME_HOME="$REPO_ROOT/.local_runtime/codex-home"
SOURCE_AUTH="$HOME/.codex/auth.json"
TARGET_AUTH="$RUNTIME_HOME/auth.json"
CONFIG_FILE="$RUNTIME_HOME/config.toml"

mkdir -p "$RUNTIME_HOME"

if [ ! -f "$SOURCE_AUTH" ]; then
  echo "Missing Codex auth at $SOURCE_AUTH. Run 'codex login' first." >&2
  exit 1
fi

if [ -L "$TARGET_AUTH" ] || [ -f "$TARGET_AUTH" ]; then
  rm -f "$TARGET_AUTH"
fi
ln -s "$SOURCE_AUTH" "$TARGET_AUTH"

cat > "$CONFIG_FILE" <<EOF
model = "gpt-5.4"
model_reasoning_effort = "xhigh"

[projects."$REPO_ROOT"]
trust_level = "trusted"

[features]
multi_agent = true

[profiles.research-lit]
model = "gpt-5.4-mini"
model_reasoning_effort = "medium"
search = true

[profiles.idea-creator]
model = "gpt-5.4-mini"
model_reasoning_effort = "medium"
search = true

[profiles.idea-discovery]
model = "gpt-5.4-mini"
model_reasoning_effort = "medium"
search = true

[profiles.novelty-check]
model = "gpt-5.4"
model_reasoning_effort = "high"
search = true

[profiles.research-review]
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
search = true

[profiles.auto-review-loop]
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
search = true

[profiles.research-pipeline]
model = "gpt-5.4"
model_reasoning_effort = "high"
search = true

[profiles.run-experiment]
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
search = true

[profiles.monitor-experiment]
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
search = true

[profiles.analyze-results]
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
search = true

[profiles.paper-plan]
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
search = true

[profiles.paper-write]
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
search = true

[profiles.paper-figure]
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
search = true

[profiles.paper-compile]
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
search = true

[profiles.paper-writing]
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
search = true

[profiles.auto-paper-improvement-loop]
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
search = true

[profiles.feishu-notify]
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
search = true

[profiles.pixel-art]
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
search = true
EOF

exec env CODEX_HOME="$RUNTIME_HOME" /opt/homebrew/bin/codex mcp-server "$@"
