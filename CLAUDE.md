# DQIII8 — System Identity

Autonomous AI orchestration on VPS (Ubuntu, SSH-only).
Routes queries through a multi-tier LLM pipeline with domain knowledge enrichment.
Primary UI: Telegram bot (@JARVISCONTROL3BOT).

## Architecture

- **Entry points:** Telegram `/cc` → DQ Pipeline → tiered LLM router → response
- **DQ Pipeline (8 steps):** domain_classifier → subdomain → hierarchical_router → agent_selector → knowledge_enricher → confidence_gate → intent_amplifier → stream_response
- **Tiers:** C (ollama/qwen2.5-coder:7b) → B (groq/llama-3.3-70b) → B+ (github/deepseek) → A (anthropic/sonnet-4-6) → S (anthropic/opus-4-6)
- **Escalation rule:** auto-escalate if domain ≠ applied_sciences and Tier C fails
- **DB:** SQLite — `database/dqiii8.db` (79 tables) + `database/dqiii8_metrics.db`
- **Hooks:** 12 lifecycle hooks (`.claude/hooks/`)
- **Skills:** 17 slash commands (`.claude/skills/`)
- **Agents:** 9 active + 18 archived (`.claude/agents/`)

## Tiering Rules (STRICT — never pay when free works)

| Tier | Provider | Model | Cost | Use when |
|---|---|---|---|---|
| C | Ollama (local) | qwen2.5-coder:7b | $0 | Code, git, pipeline tasks |
| B | Groq | llama-3.3-70b-versatile | $0 | Research, analysis, writing, domain knowledge |
| B+ | GitHub Models | deepseek-v3 / codestral | $0 | Fallback, long-context, code review |
| A | Anthropic | claude-sonnet-4-6 | ~$0.03 | Finance, orchestration, architecture decisions |
| S | Anthropic | claude-opus-4-6 | ~$0.20 | Multi-agent coordination, system design only |

**RULE:** Always start at the cheapest tier. Escalate only on explicit task-type match or tier failure. Never use Tier A/S for tasks Tier B can handle.

## Hook Execution Order

Every Claude Code tool call passes through hooks in this order:
1. `pre_tool_use.py` — PermissionAnalyzer v3 (APPROVE/DENY/ESCALATE) + dynamic rules injection + output truncation
2. *(tool executes)*
3. `post_tool_use.py` — records action to DB, estimates cost

Session lifecycle:
- `session_start.py` — injects project context, last 5 lessons, audit state
- `stop.py` — auto-commit uncommitted changes, extract lessons, write session metrics

**DO NOT modify hook behavior without understanding the downstream DB effects.** Every DENY/ESCALATE is logged to `agent_actions`. Budget checks read from `session_events`.

## Dynamic Database — Modification Rules

`database/dqiii8.db` is the live operational database. Rules for modifying it:

- **Schema changes:** edit `database/schema_v2.sql` only. Run `python3 -m database.apply_migrations`. Never alter the live DB directly via `sqlite3` unless it's a one-time data fix.
- **`instincts` table:** append-only via `bin/tools/auto_learner.py`. Never manually delete rows — confidence decay handles stale instincts.
- **`agent_actions` table:** read-only from application code. `purge_transient_errors.py` handles cleanup. Never mass-DELETE without WHERE.
- **`model_performance` table:** written by `openrouter_wrapper.py` after every LLM call. Do not manually edit scores — they affect routing decisions.

## Key Files

- `bin/core/openrouter_wrapper.py` — DQ pipeline + multi-provider LLM router
- `bin/ui/dqiii8_bot.py` — Telegram bot (23 commands, async, rate-limited)
- `bin/director.py` — Intent parser: instincts fast-path + LLM classification + keyword fallback
- `bin/orchestrator.py` — `/cc` and `/auto` Telegram command handler
- `bin/j.sh` — CLI entry: `j cc`, `j loop`, `j status`, `j dq`
- `.claude/hooks/pre_tool_use.py` — PermissionAnalyzer v3 + rules_dispatcher
- `.claude/hooks/session_start.py` — Project context + lessons injection
- `.claude/hooks/stop.py` — Auto-commit + lessons extraction + session close
- `config/domain_agent_map.json` — Domain → agent routing table (5 domains)
- `database/schema_v2.sql` — DB schema (idempotent, source of truth)
- `tasks/lessons.md` — Learned lessons (append-only)
- `knowledge/` — 5 domain indexes (bge-m3, 1024d embeddings)
- `RULE` — Project directives (always read at session start)

## Projects

Each project lives in `my-projects/{name}/` with its own `PROJECT.md`.
To discover active projects:
```
ls my-projects/*/PROJECT.md
```
Read `PROJECT.md` before working on any project. Never hardcode project lists here.

## Inviolable Rules

- **RULE file** — always read at session start, directives take precedence
- **Cheapest tier first** — C→B→A→S, never skip tiers without justification
- **Never edit** `.env`, `CLAUDE.md`, `.credentials.json`, `database/schema_v2.sql` from generated code
- **Auto-commit** on session close via `stop.py` — do not suppress
- **PermissionAnalyzer** — every tool use gets APPROVE/DENY/ESCALATE; DENY is final
- **No API key in source** — all keys via `os.environ.get("VAR_NAME")` only
- **ANTHROPIC_API_KEY must be `""` in subprocess env** when using Claude Code OAuth — never export it

## Plugins (Claude Code)

**Permanent:** superpowers, episodic-memory, frontend-design, firecrawl, hookify, semgrep, context7, code-review, skill-creator, figma, code-simplifier, pr-review-toolkit, claude-md-management

**On-demand:** Tier 3 auto-install via `PROJECT.md "Plugins:"` field
Available: playwright, greptile, pyright-lsp, superpowers-lab

Config: `config/claude_settings_template.json`, `bin/plugin_manager.py`

## Workspace

Yazi file browser: `yazi /root/dqiii8` (config: `~/.config/yazi/yazi.toml`)
tmux layouts in `bin/workspace/` — aliases: `workspace`, `beeswarm`, `monitor`
See `.claude/rules/workspace.md` for when to suggest each layout.

## PROTOCOLO CERO COMPLACENCIA (Global)

- **Cero falso éxito:** Validate the real final artifact (DOCX, API response, deployed service) — not just automated tests. No dopamine from green CI alone.
- **Rigor y Raíz:** Resolve ambiguities with the most robust option. Attack the root cause, not symptoms.
- **Gatekeeper:** If an error repeats, instrument a structural QA check on the final artifact that blocks delivery until resolved.
