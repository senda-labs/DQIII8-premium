# DQIII8 — Review Report (adversarial) — 2026-06-10

Revisión post-transformación. Método: leer el código real, ejecutar probes empíricos,
verificar cada claim del `DQIII8_TRANSFORMATION_REPORT_2026-06-10.md` contra el artefacto
vivo (DB, systemd, suite, CLI). Cada hallazgo lleva evidencia y estado.

---

## 1. Hallazgos del ataque de lógica

### CRÍTICO

**C1 — La consolidación de DB rompió silenciosamente la lane de relevancia de hybrid_search.**
- Evidencia: `temporal_memory.py` apunta a `database/dqiii8.db` pero `facts`,
  `fact_access_log` y `vector_chunks` solo existen ya en `dqiii8_history.db` (readonly).
  Probe en vivo: `query_facts` → `OperationalError: no such table: facts`;
  `compute_relevance` → `no such table: vector_chunks`. `hybrid_search._apply_relevance`
  capturaba la excepción por resultado y devolvía `final_score=base` — degradación
  silenciosa en producción, pagando un try/except por resultado.
- Estado: **FIJADO** (por archivado): `temporal_memory.py` y `memory_decay.py` movidos a
  `bin/tools/_archived/`; ahora el import falla una vez y `_apply_relevance` retorna
  por la vía rápida documentada. Test de contrato nuevo:
  `test_apply_relevance_degrades_without_temporal_memory`.
- Deuda registrada: si se quiere re-ranking por frecuencia de acceso, debe reconstruirse
  sobre `vec_knowledge` + una tabla de accesos en el SSOT (decisión de schema → owner).

### ALTO

**A1 — `_detect_entity` devolvía el verbo imperativo inicial como entidad.**
- Evidencia (probe v1.0): `"Analiza el rendimiento…"` → entity=`'Analiza'`;
  `"Corrige el error…"` → `'Corrige'`; `"Can you fix…"` → `'Can'`. Los prompts tier-3 en
  producción llevaban frases sin sentido tipo *"the question Analiza must answer"* dentro
  del bloque `[EXECUTION PLAN]` — degradaba la credibilidad del bloque inyectado.
- Fix: `_ENTITY_STOPWORDS` = stopwords + auxiliares + todas las keywords mono-palabra de
  `_PATTERN_KEYWORDS` (normalizadas). Verificado: `"Planifica la migracion del bot de
  Telegram"` → `Telegram`. compiler_version → **1.1**. Estado: **FIJADO** + 1 test.

**A2 — Sin normalización de acentos en `_infer_pattern`.**
- Evidencia: `"qué es un webhook"` clasificaba como **integrate** (keyword `webhook`)
  porque `"qué es"` no matcheaba la keyword `"que es"`. Fix: `_norm()` (NFD + strip
  combining marks). Ahora → **explain**. Estado: **FIJADO** + 1 test.

**A3 — El score 95/100 del health check no era reproducible: métrica de telemetría mal diseñada.**
- Evidencia: re-ejecución en vivo → **79/100** con `telemetry_alive_rate_7d: 0.36`.
  La métrica usaba `confidence > 0` como proxy de "telemetría viva", pero `confidence=0.0`
  es legítimo (prompt sin keyword de intent → fallback `explain`). El 95 del reporte se
  midió justo después de que los tests E2E llenaran `amplification_log` con filas de
  confidence alta — datos sesgados. Riesgo: falsas alertas <70 con tráfico normal.
- Fix: aliveness = filas con el set completo de columnas del INSERT corregido
  (`intent_pattern`/`routing_method`/`tier_selected` NOT NULL) — mide exactamente lo que
  el fix B4 de `_log_amplification` debía garantizar. Score honesto post-fix: **95/100**
  (rate 1.0 sobre 246 filas reales de 7d; −5 por 4 errores sin resolver).
  Estado: **FIJADO**.

**A4 — El hook `dq_compile_hook.py` es código muerto con doble candado.**
- Evidencia: no está registrado en `.claude/settings.json` (verificado), de modo que
  `DQ_COMPILE_HOOK=1` **no tiene ningún efecto** — el opt-in documentado es inoperante.
- Decisión: mantener SIN registrar (el benchmark v3 muestra latencia 2-3× y 3/12 timeouts;
  el propio reporte recomienda opt-in). `.claude/settings.json` y `.claude/hooks/` son
  rutas protegidas en esta sesión → el registro queda documentado aquí para el owner:

  ```json
  // .claude/settings.json → "hooks" → "UserPromptSubmit", añadir:
  { "hooks": [ { "type": "command",
                 "command": "bash .claude/hooks/run.sh dq_compile_hook.py" } ] }
  ```
  Y exportar `DQ_COMPILE_HOOK=1` en la sesión. Estado: **DOCUMENTADO** (pendiente del owner).

### MEDIO

**M1 — Comentario engañoso del threshold del hook.** `confidence < 0.34` excluye también
los prompts de 1 hit (1 hit = 0.333), no "<1 keyword hit" como dice el comentario. El
comportamiento (exigir ≥2 hits) es razonable; el comentario es falso. Hook no editable en
esta sesión → corregido vía test que fija el contrato:
`test_single_keyword_hit_confidence_is_below_hook_threshold`. Estado: **PINNED EN TEST**.

**M2 — Empate de patrones resuelto por orden de dict.** `"Escribe un test para…"` →
`generate` (no `test`) porque con score empatado gana el primero del dict. Heurística
aceptable pero arbitraria. Estado: **DOCUMENTADO** (no fijado — cambiarlo altera
clasificaciones existentes sin evidencia de mejora; medir antes).

**M3 — En el wiring tier-3, `dq_compile(original, intent_pattern=intent_action)` fuerza
`confidence=1.0`** aunque el amplifier haya detectado la acción con un prefijo débil
(`t.startswith(kw[:5])`). El gating por confianza del compiler nunca aplica en la ruta de
producción. Mitigado porque `intent_action=""` (sin match) pasa `None` → inferencia.
Estado: **DOCUMENTADO** (deuda menor).

**M4 — Test vacuo en E2E.** `test_confidence_gate_blocks_low_score_tier_b` solo
comprobaba `isinstance(result, bool)` ("no crashea"). Reemplazado por
`test_confidence_gate_tier_b_blocks_generic_passes_specific`, que fija las 3 ramas reales
de la Rule 4 (definicional → block; 2 indicadores → block; 3 indicadores → pass).
Estado: **FIJADO**.

**M5 — Los "6 fallos pre-existentes" tenían una sola causa raíz: faltaba el plugin async
de pytest.** No eran inofensivos: 3 de ellos eran `test_bot_auth_update` — la suite de
autenticación del bot de Telegram llevaba sin ejecutarse desde que se escribieron.
Fix: `apt-get install python3-anyio` + fixture `anyio_backend="asyncio"` en `conftest.py`
(trio no está instalado). Los 7 tests de bot_auth ahora **pasan**. Los 3 de bee_swarm se
archivaron junto al módulo (ver §4). Estado: **FIJADO**.

### BAJO

**B1 — `dqiii8.db` fantasma de 0 bytes en la raíz del repo** (`/root/dqiii8/dqiii8.db`,
27-may). El SSOT es `database/dqiii8.db`; el fichero raíz confunde (esta misma revisión
tropezó con él). Es ruta write-blocked → **no se toca**; el owner decide si borrarlo.

**B2 — `health_check` con `total=0` da rate 1.0** (25 pts gratis sin datos en 7d).
Defendible como cron-safe; anotado, sin cambio.

**B3 — CLI `dq_compile` verificado al completo**: stdin ✓, `--json` ✓ (round-trip
parseado), `--pattern` ✓ (confidence 1.00), pattern desconocido → exit 1 con mensaje ✓,
prompt vacío → error ✓, `--pattern` sin valor → exit 2 ✓. Sin hallazgos.

**B4 — Los 14 templates NO son skeletons.** Leídos los 14 completos: cada uno tiene
4-5 fases con exit-criteria verificables, pseudocódigo con asserts, 4 items de audit
específicos del patrón (no genéricos), 2 validation tests y ≥1 invariante propio + 4
compartidos portados de Orchestrator v4 (phase_guard/RIL/idempotencia). El render es
escaffolding de proceso, no boilerplate RAG. Claim del reporte: **VERIFICADO**.

**B5 — systemd timer activo de verdad**: `dqiii8-health.timer` loaded/enabled/active,
próximo disparo 07:30 CEST. Claim: **VERIFICADO**.

**B6 — INSERT de `_log_amplification` escribe los 17 campos**: verificado con SELECT
sobre filas reales del 2026-06-10 (3.203 filas; `routing_method`, `confidence`,
`knowledge_used` poblados). Claim: **VERIFICADO**. El fallback del wiring tier-3
(`except: pass`, nunca bloquea el prompt) es correcto y está testeado.

---

## 2. Estado real de integración OSS

| Fuente | Claim del reporte | Estado real verificado | Acción de esta revisión |
|---|---|---|---|
| **Odysseus** | 3 patrones DISCARD | Correcto técnicamente. Scheduler = daemon+queue+4 tablas vs cron/systemd existente ✓. Memoria ChromaDB es vector-only 384-dim vs hybrid RRF (vector+FTS5+graph) 1024-dim bge-m3 — adoptarla sería un downgrade ✓. hwfit no tiene inputs en un VPS mono-Ollama ✓. | Ninguna. Micro-notas válidas (`compute_next_run`, latch `_http_embed_down`) quedan contingentes a medición. |
| **opencode** | No mencionado | `opencode` (anomalyco/sst) es el **motor de agente** sobre el que Odysseus construye su modo "Agent" — un harness de coding agent tipo Claude Code, más el gateway de modelos "OpenCode Zen" (`opencode.ai/zen`). No está instalado en el VPS. Para DQIII8 es un **sustituto** del harness, no un componente integrable: DQIII8 está anclado a Claude Code por OAuth Max, hooks PermissionAnalyzer y las reglas inviolables (`ANTHROPIC_API_KEY=""`). Integrarlo añadiría un segundo agente residente sin problema medido que resolver. | **DESCARTADO con justificación** (este doc). |
| **MoneyPrinterTurbo** | ADAPT deferred | El plan de adaptación del doc es bueno y concreto (stock_sourcer + crosspost, sin runtime MPT). **El deferred es CORRECTO hoy**: `.env` no contiene `PEXELS_API_KEY` ni `PIXABAY_API_KEY` (verificado por nombre, sin leer valores) → una integración hoy sería inverificable E2E, violando cero-autocomplacencia. content-automation está en producción con visuales generativas; el stock track es additivo, no urgente. | Ninguna. Precondición documentada: conseguir API key Pexels (free tier) ANTES de portar `material.download_videos` → `src/stock_sourcer.py`. |
| **Hermes** | Footprint Ladder = INTEGRATE (doc-only) | **Documentado pero NO aplicado**: cero menciones de "footprint" en `.claude/` o `bin/`. Exactamente la brecha "documentado vs aplicado" que preguntaba el owner. | **APLICADO**: sección "Capability Footprint Ladder" añadida a `.claude/rules/03_tiering_and_routing.md` (6 peldaños + corolarios, cross-ref al research doc). |

Resumen honesto: de los 10 patrones, 8 descartes son técnicamente sólidos (verificados
contra el código clonado en `/tmp/oss-research/`), 1 ADAPT está correctamente diferido
por falta de credencial, y 1 INTEGRATE estaba solo en papel — ya está aplicado.

---

## 3. Acciones ejecutadas

| # | Acción | Ficheros |
|---|---|---|
| 1 | Fix entity-verbo + acentos + version 1.1 | `bin/agents/plan_compiler.py` |
| 2 | Fix métrica telemetría + campo `amplification_rows_7d` | `bin/tools/health_check.py` |
| 3 | Test vacuo → 3 asserts de comportamiento pinneado | `tests/test_e2e_compile_pipeline.py` |
| 4 | 3 tests de regresión v1.1 (entidad, acentos, threshold hook) | `tests/test_plan_compiler.py` |
| 5 | Fixture `anyio_backend` + `python3-anyio` (apt) → bot_auth 7/7 | `tests/conftest.py` |
| 6 | Split de coverage vector/hybrid antes de archivar (5 tests, incl. contrato de degradación) | `tests/test_vector_hybrid_search.py` (nuevo) |
| 7 | Archivado de fósiles (git mv, historia preservada) | `bin/tools/_archived/{bee_swarm.py, test_bee_swarm.py, launch_beeswarm.sh, temporal_memory.py, memory_decay.py, test_temporal_memory.py}` |
| 8 | Limpieza de referencias a fósiles | `bin/monitoring/health_watchdog.py`, `zones/zone_A_core_pipeline.md` |
| 9 | Footprint Ladder aplicado como doctrina | `.claude/rules/03_tiering_and_routing.md` |
| 10 | Este reporte | `docs/DQIII8_REVIEW_REPORT_2026-06-10.md` |

No ejecutado (rutas protegidas, correcto según reglas): edición de
`.claude/hooks/dq_compile_hook.py` (comentario M1) y registro en `settings.json` (A4) —
ambos documentados arriba con el snippet exacto.

---

## 4. Estado de fósiles

| Fósil | Verificación de uso | Decisión | Ejecutado |
|---|---|---|---|
| `bin/bee_swarm.py` | `agent_actions`: 32 refs, TODAS dev-edits (bash/edit/read/write), última 2026-03-29. 0 invocaciones de producción. Sin imports externos. | **ARCHIVAR** | ✓ → `bin/tools/_archived/` + launcher + tests |
| `temporal_memory.py` + `memory_decay.py` | 6 facts en toda su vida (en history readonly); roto contra el SSOT (C1); memory_decay jamás tuvo cron (`crontab -l` vacío). hybrid_search degrada limpio sin ellos (testeado). | **ARCHIVAR** | ✓ → `bin/tools/_archived/`; coverage de vector/hybrid preservada en test nuevo |
| `instincts` table | 22 filas, TODAS confidence=0.5 — el fast-path del director exige >0.7, así que **nunca dispara**. 1 fila con times_applied=2. | **MANTENER, no resetear.** El problema no son los datos sino que falta el loop de actualización de confianza (ninguna fila ha subido de 0.5). Resetear destruiría la única señal acumulada sin arreglar nada. Deuda: instrumentar promoción/decay de confidence en `instinct_evolver.py`, o bajar el threshold tras validar precision. | ✓ (decisión documentada) |
| `bin/tools/benchmark_dq.py` | 0 refs en agent_actions. Pero NO está sustituido: mide el valor del RAG (resultado −0.5 que justifica `confidence_gate`); `benchmark_compile.py` mide el delta del compiler (+2.62). Son la base empírica de dos decisiones distintas. | **MANTENER** (harness histórico/reproducibilidad) | ✓ |

---

## 5. Tests añadidos o mejorados

- Suite: **239 passed, 0 failed, 0 errors** (antes: 6 failed).
- Nuevos: 3 regresiones v1.1 en `test_plan_compiler.py`; 5 en
  `test_vector_hybrid_search.py` (4 portados + 1 contrato de degradación nuevo).
- Mejorados: test vacuo del confidence gate → 3 asserts deterministas.
- Reparados: 7 de `test_bot_auth_update.py` (causa raíz: plugin async ausente).
- Archivados: 16 de bee_swarm + 11 de temporal (con sus módulos).
- Delta neto de cobertura honesta: la suite ya no contiene ningún assert
  "no crashea" en los entregables de la transformación.

## 6. Score de calidad post-revisión: **82/100**

Justificación:
- **+** Núcleo de la transformación es real y sólido: templates ricos (verificado línea a
  línea), wiring B4 correcto con fallback no bloqueante, telemetría escribiendo 17 campos,
  timer activo, CLI completo, benchmark con metodología decente. Suite 239/0.
- **−10** El claim 95/100 del health check no era reproducible (métrica sesgada por datos
  de test); corregido, pero un claim cuantitativo del reporte de transformación era falso
  en el momento de publicarse.
- **−5** La consolidación de DB rompió una feature de producción (relevance lane) y nadie
  lo detectó porque la degradación era silenciosa — exactamente el patrón que el protocolo
  cero-autocomplacencia existe para evitar.
- **−3** El "INTEGRATE" de Hermes y el opt-in del hook eran papel: documentados como
  hechos, inoperantes en el sistema vivo.
- El compilador genera ahora bloques sin entidades absurdas y clasifica español acentuado;
  la latencia 2-3× del modo ON sigue siendo la razón válida para mantener el hook opt-in
  (y des-registrado) hasta acotarla.
