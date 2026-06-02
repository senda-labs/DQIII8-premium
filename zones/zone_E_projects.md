# Zone E — Projects
> Updated: 2026-06-02

---

## What it covers
All active projects under `my-projects/` and their entry points.

---

## Active Projects

| Project | Path | Status | Notes |
|---|---|---|---|
| intl-reports | `my-projects/intl-reports/` | ACTIVE | Pipeline v4, T2/T3/T4 running |
| content-automation | `my-projects/content-automation/` | ACTIVE | — |
| pokemon-genesis-chaos | `my-projects/pokemon-genesis-chaos/` | ACTIVE | TileForge, Essentials v21.1 |
| accounting-erp | `my-projects/accounting-erp/` | ACTIVE | pl-global invoices |
| automatic-nutrition | `my-projects/automatic-nutrition/` | ACTIVE | — |
| manos-poker | `my-projects/manos-poker/` | ACTIVE | — |
| mejorapoker-src | `my-projects/mejorapoker-src/` | ACTIVE | — |
| ouroboros-q-eml | `my-projects/ouroboros-q-eml/` | ACTIVE | — |
| global-media-org | `my-projects/global-media-org/` | ACTIVE | — |

## Archived Projects
`my-projects/archived-projects/` — hult-finance, math-image-generator, sentiment-jobsearch, auto-report.tar.gz, python-for-analyst

---

## Before Working on a Project

```bash
ls my-projects/*/PROJECT.md       # scan all projects
cat my-projects/{name}/PROJECT.md # read project state
```

Each project has its own `PROJECT.md` with current state, pipeline, and rules.

---

## intl-reports (Primary Active)

- Pipeline: Orchestrator v4 (SQLite WAL DAG, asyncio)
- Entry: `python3 -m core.cli --phase generate --slug {slug}` (from external tmux ONLY)
- Vault: `my-projects/intl-reports/vault/000_INDEX.md` (full navigation layer)
- venv: `/root/dqiii8/my-projects/intl-reports/.venv`
- **NEVER run from inside Claude Code** (`CLAUDECODE=1` raises RuntimeError)

---

## Project Index Files

| File | Role |
|---|---|
| `my-projects/PROJECT.md` | Master project index |
| `my-projects/README.md` | Overview |
| `my-projects/{name}/PROJECT.md` | Per-project state |

---

## Cross-zone Links
- intl-reports vault → self-contained, see `my-projects/intl-reports/vault/000_INDEX.md`
- Project ADRs → [[zone_F_knowledge]]
- Server paths → [[zone_D_infrastructure]]
