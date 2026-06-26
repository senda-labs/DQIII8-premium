# DQIII8 — Index Kernel
Autonomous AI orchestration (VPS, SSH-only). Servidor activo: → `infrastructure/ACTIVE.md`
UI: Telegram @JARVISCONTROL3BOT | CLI: `j cc` / `j loop` / `j status`

## Routing Tiers (Cost-First — STRICT)
C (Ollama/local $0) → B (Groq $0) → B+ (NIM $0, 40RPM, 1M ctx) → B++ (GitHub $0) → A (Sonnet ~$0.03) → S (Opus ~$0.20)
Start cheap. Escalate only on explicit task-type match or tier failure.
Full table + decision algorithm → `.claude/rules/03_tiering_and_routing.md`

## System Map
- DQ Pipeline (7 steps): Classify → Retrieve → Gate → Amplify → Route → Execute → Memory
- DB: `database/dqiii8.db` (46 tables + 20 views live; schema_v2.sql defines 65) + `dqiii8_metrics.db` | Schema: `database/schema_v2.sql`
- Hooks (14): `.claude/hooks/` | Skills (21): `.claude/skills/` | Agents (17): `.claude/agents/`
- Entry: `bin/core/openrouter_wrapper.py` | Director: `bin/director.py` | Bot: `bin/ui/dqiii8_bot.py`
- Dispatch (CC↔dqiii8): `bin/core/dispatch.py` | Skill: `/dispatch-agent` | Results: `tasks/results/`
- Infraestructura: `infrastructure/ACTIVE.md` (servidor activo) · `infrastructure/servers/` (historial)
- → Mapa completo y anotado: [[tasks/FULL_SYSTEM_MAP|Full System Map]] · Decisión arquitectónica: [[docs/architecture_decision_context_efficiency|ADR-001]]
- → Vault navigation: `zones/000_INDEX.md` (routing · zone map · decision tree) · `zones/SESSION.md` (handover state)

## Rule Engine — Read Before Acting

| Domain | Read this first |
|---|---|
| Any action | `.claude/rules/00_core_behavior.md` (always loaded — zero-complacency, scope, cost-first) |
| DB schema / SQL / sqlite3 | `.claude/rules/01_database_mutations.md` |
| Hooks or PermissionAnalyzer | `.claude/rules/02_hooks_and_permissions.md` |
| Tiering / routing / agent changes | `.claude/rules/03_tiering_and_routing.md` |
| Git / Bash safety | `.claude/rules_db/git-safety.md` |
| Error prevention (recurring) | `.claude/rules_db/dqiii8-error-prevention.md` |
| intl-reports pipeline | `my-projects/intl-reports/RULE` (reglas absolutas + pipeline) |

## Inviolable Rules
- NEVER write to `.env`, `CLAUDE.md`, `.credentials.json`, `database/schema.sql` from generated code.
- NEVER hardcode API keys — all keys via `os.environ.get("VAR")` only.
- NEVER commit `*.db` files — they are gitignored. Use `database/schema_v2.sql` for fresh installs.
- DENY from PermissionAnalyzer is final — do not retry or bypass.
- `ANTHROPIC_API_KEY` must be `""` in subprocess env when using Claude Code OAuth.
- Plans touching ≥3 modules OR with ambiguous scope → enter plan mode first, wait for confirmation.
- Destructive / irreversible actions (rm -rf, DROP, force-push, schema change) → STOP, notify user, wait.
- `tasks/audit/` path is hardcoded in red-team, blue-team, security-cycle skills — never rename it.

## Projects
Each lives in `my-projects/{name}/` with its own `PROJECT.md`. Scan before working:
`ls my-projects/*/PROJECT.md` → read `PROJECT.md` → read `RULE`.
Índice completo: [[my-projects/PROJECT|my-projects/PROJECT.md]] · Activos destacados: [[my-projects/intl-reports/PROJECT|intl-reports]] · [[my-projects/content-automation/PROJECT|content-automation]]

## New Project / Feature Creation
Use Spec-Driven Development (SDD) via spec-kit for any feature touching ≥3 modules or new architecture.
Skill: `/speckit` — covers installation, full cycle, and dqiii8 constraints (no git extension, no auto-push).
Reference implementation: `my-projects/pokemon-genesis-chaos/specs/001-tileforge-saas/`
