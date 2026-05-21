#!/usr/bin/env python3
"""Compatibility entry point for the FigureSpec renderer.

The canonical helper lives with the skill that owns it:
    .opencode/skills/figure-spec/scripts/figure_renderer.py

This shim keeps older docs and project-local invocations working while avoiding
two divergent renderer implementations in the repo.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
REAL = REPO_ROOT / ".opencode" / "skills" / "figure-spec" / "scripts" / "figure_renderer.py"


def main() -> int:
    if not REAL.is_file():
        sys.stderr.write(
            f"ERROR: canonical figure_renderer.py not found at {REAL}.\n"
            "       Expected it under .opencode/skills/figure-spec/scripts/.\n"
        )
        return 1
    os.execv(sys.executable, [sys.executable, str(REAL), *sys.argv[1:]])
    return 0


if __name__ == "__main__":
    sys.exit(main())
