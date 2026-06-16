# Zone I — Ops
> Updated: 2026-06-16

---

## What it covers
Operational files: sessions, uploads, examples, tests.

---

## sessions/

Session handover notes and logs.

```bash
ls -t sessions/           # most recent sessions first
cat sessions/SESSION-{date}.md
```

Recent:
- `2026-06-16_session_1.md` — untracked commits, health timer, vault update
- `2026-06-12_session_1.md` — plan_compiler + tests + security fixes
- `2026-06-11_session_2.md`
- `2026-06-11_session_1.md`
- `2026-06-09_session_4.md`

---

## uploads/

User-uploaded files for processing. Gitignored.

```bash
ls uploads/
```

---

## examples/

Example prompts, responses, and usage patterns for the pipeline.

---

## tests/

Test scripts and test fixtures.

```bash
ls tests/
python -m pytest tests/      # run test suite
```

---

## Gitignore Note

`sessions/` and `uploads/` are gitignored. Within `tasks/`, only specific subpaths are ignored (e.g. `tasks/results/`, `tasks/nightly-report.md`, `tasks/status.md`, `tasks/audit_pending.flag`) — `tasks/audit/` and others stay tracked.
Canonical ignore rules live in the repo-root `.gitignore` (also covers `*.db`, `.env`, `__pycache__/`, `.venv/`).

---

## Cross-zone Links
- Session outputs → [[zone_G_tasks]] (results/)
- Current handover → `[[SESSION]]` (zones/SESSION.md)
