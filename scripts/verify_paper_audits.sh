#!/usr/bin/env bash
# verify_paper_audits.sh
#
# Lightweight submission-assurance verifier for this OpenCode/Codex port.
# It checks the mandatory paper audit artifacts, validates their basic schema,
# verifies the recorded input hashes, and reports whether the paper is ready to
# be called submission-ready at the requested assurance level.

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  bash scripts/verify_paper_audits.sh <paper-dir> [--assurance draft|submission] [--json-out <path>]

Defaults:
  --assurance: read from <paper-dir>/.aris/assurance.txt if present, else draft
  --json-out:  <paper-dir>/.aris/audit-verifier-report.json
EOF
}

paper_dir=""
assurance=""
json_out=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --assurance)
      assurance="${2:?--assurance requires a value}"
      shift 2
      ;;
    --json-out)
      json_out="${2:?--json-out requires a value}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --*)
      echo "unknown option: $1" >&2
      exit 2
      ;;
    *)
      if [[ -z "$paper_dir" ]]; then
        paper_dir="$1"
      else
        echo "unexpected positional argument: $1" >&2
        exit 2
      fi
      shift
      ;;
  esac
done

if [[ -z "$paper_dir" ]]; then
  usage >&2
  exit 2
fi

if [[ ! -d "$paper_dir" ]]; then
  echo "paper directory not found: $paper_dir" >&2
  exit 2
fi

paper_dir="$(cd "$paper_dir" && pwd)"

if [[ -z "$assurance" ]]; then
  if [[ -f "$paper_dir/.aris/assurance.txt" ]]; then
    assurance="$(tr -d '[:space:]' < "$paper_dir/.aris/assurance.txt")"
  else
    assurance="draft"
  fi
fi

case "$assurance" in
  draft|submission) ;;
  *)
    echo "invalid assurance level: $assurance" >&2
    exit 2
    ;;
esac

if [[ -z "$json_out" ]]; then
  json_out="$paper_dir/.aris/audit-verifier-report.json"
fi

mkdir -p "$(dirname "$json_out")"

python3 - "$paper_dir" "$assurance" "$json_out" <<'PY'
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

paper_dir = Path(sys.argv[1]).resolve()
assurance = sys.argv[2]
json_out = Path(sys.argv[3]).resolve()

mandatory = [
    ("PAPER_CLAIM_AUDIT.json", "paper-claim-audit"),
    ("CITATION_AUDIT.json", "citation-audit"),
]

allowed_verdicts = {"PASS", "WARN", "FAIL", "NOT_APPLICABLE", "BLOCKED", "ERROR"}
blocking_verdicts = {"FAIL", "BLOCKED", "ERROR"}
required_fields = {
    "audit_skill",
    "verdict",
    "reason_code",
    "summary",
    "audited_input_hashes",
    "trace_path",
    "thread_id",
    "reviewer_model",
    "reviewer_reasoning",
    "generated_at",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_artifact(path: Path, expected_skill: str) -> tuple[str, str, bool, list[str]]:
    issues: list[str] = []
    verdict = ""
    stale = False

    if not path.exists():
        if assurance == "submission":
            return "MISSING", verdict, stale, [f"missing_artifact:{path.name}"]
        return "MISSING_DRAFT_OK", verdict, stale, []

    try:
        data = json.loads(path.read_text())
    except Exception as exc:  # noqa: BLE001
        return "INVALID", verdict, stale, [f"cannot_parse_json:{exc}"]

    missing_fields = sorted(required_fields - set(data))
    for field in missing_fields:
        issues.append(f"missing_field:{field}")

    verdict = str(data.get("verdict", ""))
    if verdict not in allowed_verdicts:
        issues.append(f"invalid_verdict:{verdict}")

    audit_skill = data.get("audit_skill")
    if audit_skill and audit_skill != expected_skill:
        issues.append(f"wrong_audit_skill:{audit_skill}")

    hashes = data.get("audited_input_hashes", {})
    if not isinstance(hashes, dict):
        issues.append("audited_input_hashes_not_dict")
    else:
        for rel_path, recorded in hashes.items():
            recorded_value = str(recorded)
            if recorded_value.startswith("sha256:"):
                recorded_value = recorded_value.split(":", 1)[1]
            target = Path(rel_path)
            if not target.is_absolute():
                target = paper_dir / rel_path
            if not target.exists():
                stale = True
                issues.append(f"stale:file_missing:{rel_path}")
                continue
            if sha256(target) != recorded_value:
                stale = True
                issues.append(f"stale:hash_mismatch:{rel_path}")

    trace_path = str(data.get("trace_path", ""))
    if trace_path:
        trace = Path(trace_path)
        if not trace.is_absolute():
            trace = paper_dir / trace_path
        if not trace.exists():
            issues.append(f"trace_missing:{trace_path}")
        elif trace.is_dir():
            if not any(trace.iterdir()):
                issues.append(f"trace_empty:{trace_path}")
        elif trace.stat().st_size == 0:
            issues.append(f"trace_empty:{trace_path}")
    else:
        issues.append("missing_trace_path")

    if issues:
        return "PROBLEM", verdict, stale, issues
    return "OK", verdict, stale, issues


results = []
blocking = False

for artifact_name, expected_skill in mandatory:
    status, verdict, stale, issues = verify_artifact(paper_dir / artifact_name, expected_skill)
    if stale and assurance == "submission":
        blocking = True
    if assurance == "submission" and (status in {"MISSING", "INVALID"}):
        blocking = True
    if verdict in blocking_verdicts and assurance == "submission":
        blocking = True
    results.append(
        {
            "audit": expected_skill,
            "artifact": artifact_name,
            "status": status,
            "verdict": verdict,
            "stale": stale,
            "issues": issues,
        }
    )

report = {
    "paper_dir": str(paper_dir),
    "assurance": assurance,
    "ok": not blocking,
    "audits": results,
}

json_out.write_text(json.dumps(report, indent=2))

print(json.dumps(report, indent=2))
raise SystemExit(0 if not blocking else 1)
PY
