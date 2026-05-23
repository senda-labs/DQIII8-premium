# DQIII8 — Dynamic Rules (RAG)

## REGLA UNIVERSAL — API KEY Y OAUTH

PROHIBIDO modificar o exportar ANTHROPIC_API_KEY en producción.
Siempre OAuth (Claude Max). Subprocess: env={"ANTHROPIC_API_KEY": ""}
Si "Credit balance too low": verificar que ANTHROPIC_API_KEY="" en subprocess.

Rules contextuales inyectadas por rules_dispatcher.py (llamado desde pre_tool_use.py).
Mecanismo: tool_name + tool_input → alias → carga 1-3 archivos de .claude/rules_db/ (~200–800 tokens).
NUNCA carga los 20+ archivos completos en un mismo turno. Ver 02_hooks_and_permissions.md §Rules Dispatcher.
PROHIBIDO: episodic-memory (consume 48K tokens sin valor).
Estado empresa: python3 -m core.cli status --slug {SLUG}

## SPEC-KIT / SDD (nuevo proyecto o feature)

Skill: `/speckit` — leer antes de arrancar cualquier feature no trivial.
Instalación: `source $HOME/.local/bin/env && uv tool install specify-cli --from git+https://github.com/github/spec-kit.git`
Init: `echo "y" | specify init --here --integration claude`
CRÍTICO post-init: borrar `.specify/extensions/git/` + skills `speckit-git-*` + `speckit-taskstoissues`
Ciclo: `/speckit-constitution` → `/speckit-specify` → `/speckit-plan` → `/speckit-tasks` → implementar manualmente
Referencia: `my-projects/pokemon-genesis-chaos/specs/001-tileforge-saas/`

## INTL-REPORTS (resumen ejecutivo)

Entry point: python3 -m core.cli run --slug {SLUG}   ← SOLO desde tmux externo
Resume tras interrupción: python3 -m core.cli resume --slug {SLUG}
Status: python3 -m core.cli status --slug {SLUG}
Pipeline: Orchestrator v4 (SQLite WAL DAG, asyncio.Semaphore(3), SHA256 fingerprint)
Waves: W-2(crawler auto if dossier>30d) → W-1(implications_brief) → W0(strategic+diag_intro+diag_areas×6 parallel) → W1(market_signals_layer+diag_conclusions) → W2(org+financial) → W3(gov+entry) → W4(marketing) → W5(markets+recommendations)
QA loop: INTEGRADO en v4 (max 2 retries, non-actionable errors skipped)
ACIS gate (core/preflight.py): bloquea pre-run si completeness<85 o source_integrity<50.
  Remediación: python3 -m tools.intel.session --slug {SLUG}   ← Chrome human-in-the-loop
  Batch: python3 -m tools.intel.web_presence_runner --slug-list {file}   ← Playwright sin operador
  scripts/batch_crawl.py: DEPRECADO (no existe en repo).
implications_brief.txt: OBLIGATORIO antes de cualquier run (scripts/batch_brief.py --slug)
NUNCA lanzar run/resume desde Claude Code (CLAUDECODE=1 bloquea con error explícito)
