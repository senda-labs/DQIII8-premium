# Zone D — Infrastructure
> Updated: 2026-06-02

---

## What it covers
VPS, SSH, Telegram bot, deployment, and external connectivity.

---

## Active Server

| Field | Value |
|---|---|
| Provider | Netcup RS 2000 G11 |
| IP | `[REDACTED-VPS-IP]` |
| SSH alias | `netcup` |
| OS | Debian 13 (trixie) |
| Python | 3.13.5 |
| CPU / RAM | 8 vCores · 16 GB DDR5 |
| Disk | 503 GB NVMe (~23 GB used) |
| Active since | 2026-05-29 |
| Repo path | `/root/dqiii8` |

Full details → `infrastructure/ACTIVE.md`
Server history → `infrastructure/servers/`

---

## Telegram Bot

| Item | Value |
|---|---|
| Bot | @JARVISCONTROL3BOT |
| Entry | `bin/ui/dqiii8_bot.py` |
| CLI shortcuts | `j cc` / `j loop` / `j status` |

---

## Key Files

| File | Role |
|---|---|
| `infrastructure/ACTIVE.md` | Current server — always read first for server state |
| `infrastructure/servers/` | Historical server configs |
| `bin/ui/dqiii8_bot.py` | Telegram bot |
| `bin/core/auth_watchdog.py` | OAuth / API key watchdog |
| `bin/core/notify.py` | Notification system |

---

## SSH Access

```bash
ssh netcup                    # connect to active server
ssh netcup 'j status'         # remote status check
```

---

## Claude Code

| Item | Value |
|---|---|
| Version | 2.1.156 |
| Path | `~/.local/bin/claude` |
| Auth | OAuth (Claude Max) — ANTHROPIC_API_KEY must be `""` in subprocesses |

---

## Cross-zone Links
- Bot routes to pipeline → [[zone_A_core_pipeline]]
- intl-reports venv on server → [[zone_E_projects]]
