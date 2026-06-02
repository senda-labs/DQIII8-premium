# Zone I — Ops
> Updated: 2026-06-02

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
- `2026-06-02_session_3.md` — vault reorganization
- `2026-06-02_session_2.md`
- `2026-06-02_session_1.md`
- `SESSION-20260529-netcup.md` — Netcup migration session

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

`sessions/`, `uploads/`, and `tasks/` are gitignored — none of this ops content is tracked in git.

---

## Cross-zone Links
- Session outputs → [[zone_G_tasks]] (results/)
- Current handover → `[[SESSION]]` (zones/SESSION.md)
