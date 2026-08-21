#!/usr/bin/env python3
"""Mark already-understood error_log categories as resolved.

Root-cause fix for the 2026-08-21 disaster-scenario sweep's "89 unresolved
error_log rows, no process ever closes the loop" finding: error_log grows
without bound because nothing ever revisits a row once its cause is
understood and accepted. This script is the reusable, idempotent mechanism
for that -- not a one-off UPDATE -- so the next already-explained category
(e.g. a future documented directive change) has a place to register a
pattern instead of silently accumulating in the backlog again.

Deliberately conservative: only resolves rows matching a hand-reviewed
pattern tied to a specific, cited, standing decision -- never a blanket
"mark everything resolved" pass. Run manually; not wired into any hook.
"""

import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent.parent / "database" / "dqiii8.db"

# Each entry: (error_type, message LIKE pattern, resolution note, citation)
KNOWN_EXPLAINED = [
    (
        "openrouter_wrapperError",
        "nim/%",
        "Expected under REGLA NIM Anthropic-only directive (2026-08-18): "
        "non-Anthropic providers non-operational since NIM 403 on 2026-08-16.",
        ".claude/rules/00_core_behavior.md #REGLA NIM",
    ),
    (
        "openrouter_wrapperError",
        "openrouter/%",
        "Expected under REGLA NIM Anthropic-only directive (2026-08-18): "
        "non-Anthropic providers non-operational since NIM 403 on 2026-08-16.",
        ".claude/rules/00_core_behavior.md #REGLA NIM",
    ),
]


def main() -> None:
    conn = sqlite3.connect(str(DB_PATH), timeout=30)
    total_resolved = 0
    for error_type, like_pattern, resolution, citation in KNOWN_EXPLAINED:
        cur = conn.execute(
            "UPDATE error_log SET resolved=1, resolution=? "
            "WHERE resolved=0 AND error_type=? AND error_message LIKE ?",
            (f"{resolution} ({citation})", error_type, like_pattern),
        )
        print(f"{error_type} LIKE '{like_pattern}': resolved {cur.rowcount} row(s)")
        total_resolved += cur.rowcount
    conn.commit()

    remaining = conn.execute("SELECT count(1) FROM error_log WHERE resolved=0").fetchone()[0]
    conn.close()
    print(f"total resolved this run: {total_resolved}")
    print(f"remaining unresolved: {remaining}")


if __name__ == "__main__":
    main()
