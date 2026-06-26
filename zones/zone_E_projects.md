# Zone E — Projects
> Updated: 2026-06-20

---

## What it covers
All active projects under `my-projects/` and their entry points.

---

## Active Projects

| Project | Path | Status | Notes |
|---|---|---|---|
| intl-reports | `my-projects/intl-reports/` | ACTIVE | Pipeline v4, T2/T3/T4 running |
| football-value | `my-projects/football-value/` | ACTIVE | WC2026 betting — Dixon-Coles xG + player features + σ_λ bootstrap |
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

---

## football-value (WC2026 Betting Platform)

- **Fase actual:** Spec 001 completada — xG-adjusted DC + player features + σ_λ bootstrap + calibración
- **Live testing:** 14 apuestas WC2026 MD2 settladas — net +5.11u (ROI +5.7%)
- **Tests:** 233 passing
- **Entry points:**
  - Predicción: `python3 scripts/predict_match.py --home X --away Y [--bootstrap] [--context '{}']`
  - Pipeline diario: `python3 scripts/daily_capture.py [--skip-odds]`
  - Forma histórica: `python3 scripts/ingest_form_history.py --teams all`
  - P&L: `python3 scripts/paper_trading.py [place|settle|status]`
- **Gate obligatorio:** `python3 scripts/pre_match_invariant.py --home X --away Y` antes de toda predicción
- **DB:** `my-projects/football-value/database/football.db` (WAL mode)
- **Invariantes críticos:**
  - `*** VALUE ***` → `fair_edge > 0.05` (de-vigged, NO raw odds)
  - Bootstrap fallo: `n_bootstrap == 0` → NO apostar
  - Todas las predicciones WC2026: `neutral_venue=True`
  - FBRef rate limit: 4.5s mínimo entre requests
- **Módulos clave:**
  - `models/dixon_coles.py` — DC xG-adjusted, predict_from_lambdas, context modifiers
  - `models/uncertainty.py` — bootstrap σ_λ, UncertaintyResult, adjusted_kelly_fraction
  - `models/calibration.py` — Brier, log-loss, RPS, temperature scaling, CLV
  - `models/elo_priors.py` — priors Elo + Transfermarkt (0.7/0.3 blend)
  - `models/team_strength.py` — 14 features por-90, z-score scalar
  - `capture/sources/` — fbref, fifa_fdcp, the_odds_api, form_capture, transfermarkt
- **Fases pendientes:** 4b (rest_days/team_agg_features), 5 (scrapers avanzados), 6 (ML), 7 (value classification), 8 (stealth bet management)
- **Cross-zone:** [[zone_F_knowledge]] (ADRs de decisiones de modelado) · [[zone_C_database]] (football.db schema)
