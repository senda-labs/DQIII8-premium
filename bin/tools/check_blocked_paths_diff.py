#!/usr/bin/env python3
"""
DQIII8 — Blocked-path diff scanner (Rango 1 residual, 2026-08-19 red-team audit).

The pre-push hook's gitleaks pass only catches secret-*shaped* content — a
committed empty/placeholder `id_rsa` or `.env` file has no secret shape but
still shouldn't leave the machine. Reuses `_blocked_path_hit()` from
permission_analyzer.py (the live BLOCKED_PATHS SSOT) instead of restating the
list here, per 02_hooks_and_permissions.md's no-duplication rule.

Usage: check_blocked_paths_diff.py <git-log-opts-range>
Exits 1 (blocks the push) if any changed path in that range matches
BLOCKED_PATHS; 0 otherwise.
"""

import subprocess
import sys
from pathlib import Path

_HOOKS_DIR = Path(__file__).resolve().parent.parent.parent / ".claude" / "hooks"
sys.path.insert(0, str(_HOOKS_DIR))
from permission_analyzer import _blocked_path_hit  # noqa: E402


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_blocked_paths_diff.py <git-log-opts-range>", file=sys.stderr)
        return 2
    log_opts = sys.argv[1]
    result = subprocess.run(
        ["git", "log", log_opts, "--name-only", "--pretty=format:"],
        capture_output=True,
        text=True,
        check=True,
    )
    paths = {line.strip() for line in result.stdout.splitlines() if line.strip()}

    hits = [(p, blocked) for p in paths if (blocked := _blocked_path_hit(p))]
    if hits:
        print(
            "[check-blocked-paths] BLOCKED_PATHS matched in the commits about to be pushed:",
            file=sys.stderr,
        )
        for path, blocked in hits:
            print(f"  {path}  (matches '{blocked}')", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
