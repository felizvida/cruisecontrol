#!/usr/bin/env python3
"""Compatibility entry point for experiment-queue manifest generation.

The canonical helper lives with the skill that owns it:
    .opencode/skills/experiment-queue/scripts/build_manifest.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
REAL = REPO_ROOT / ".opencode" / "skills" / "experiment-queue" / "scripts" / "build_manifest.py"


def main() -> int:
    if not REAL.is_file():
        sys.stderr.write(
            f"ERROR: canonical build_manifest.py not found at {REAL}.\n"
            "       Expected it under .opencode/skills/experiment-queue/scripts/.\n"
        )
        return 1
    os.execv(sys.executable, [sys.executable, str(REAL), *sys.argv[1:]])
    return 0


if __name__ == "__main__":
    sys.exit(main())
