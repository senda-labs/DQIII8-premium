# DQIII8 — Dynamic Rules (RAG)

## REGLA UNIVERSAL — API KEY Y OAUTH

PROHIBIDO modificar o exportar ANTHROPIC_API_KEY en producción.
Siempre OAuth (Claude Max). Subprocess: env={"ANTHROPIC_API_KEY": ""}
Si "Credit balance too low": verificar que ANTHROPIC_API_KEY="" en subprocess.

Rules contextuales inyectadas por pre_tool_use.py → .claude/rules_db/
PROHIBIDO: episodic-memory (consume 48K tokens sin valor).
Estado empresa: python3 scripts/generate_company.py --slug {SLUG} --phase status

## INTL-REPORTS (resumen ejecutivo)

Entry point: python3 -m core.cli run --slug {SLUG}   ← SOLO desde tmux externo
Resume tras interrupción: python3 -m core.cli resume --slug {SLUG}
Status: python3 -m core.cli status --slug {SLUG}
Pipeline: Orchestrator v4 (SQLite WAL DAG, asyncio.Semaphore(3), SHA256 fingerprint)
Waves: W0(strategic) → W1(diag×7+markets) → W2(diag_conclusions) → W3(org+financial) → W4(gov+entry) → W5(marketing) → W6(recommendations)
QA loop: INTEGRADO en v4 (max 2 retries, non-actionable errors skipped)
implications_brief.txt: OBLIGATORIO antes de cualquier run (scripts/batch_brief.py --slug)
NUNCA lanzar run/resume desde Claude Code (CLAUDECODE=1 bloquea con error explícito)
