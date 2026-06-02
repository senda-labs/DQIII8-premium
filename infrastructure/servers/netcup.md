---
tags: [dqiii8, servidor, infraestructura, activo]
project: dqiii8
server: netcup
status: active
updated: 2026-05-29
---
# Servidor Netcup — activo

## Identidad
- hostname: `v2202605362581464202`
- IP: `[REDACTED-VPS-IP]`
- OS: Debian 13 (trixie)
- Python: 3.13.5
- CPU: 8 vCores
- RAM: 16 GB DDR5 (15 GiB usable)
- Disco: 503 GB NVMe (~23 GB usados)
- SSH alias: `netcup`

## Rol
Servidor principal activo desde 2026-05-29.
Sustituyó a [[server-hostinger]] (migración completa).

## Claude Code
- Versión: 2.1.156
- Ruta: `~/.local/bin/claude`
- Auth: **pendiente de setup-token** — ver `~/.bashrc` (export comentado)

## Rutas clave
- dqiii8: `/root/dqiii8`
- intl-reports venv: `/root/dqiii8/my-projects/intl-reports/.venv`
- DOCXs: `/root/dqiii8/my-projects/intl-reports/companies/` (546 archivos)

## Aliases disponibles
`ll` · `la` · `l` · `dqa` · `dqo` · `workspace` · `beeswarm` · `monitor`

## Notas de migración
- rsync DOCXs completado: 546 archivos en 278 empresas (2026-05-29)
- git no inicializado (rsync-only desde Hostinger)
- `.venv` de intl-reports funcional (`core.cli OK`)
