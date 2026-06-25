# ADR-LON-005: Caché de Reportes de Bureau de Crédito con Redis

**Status:** Accepted
**Date:** 2026-06-17
**Functionality:** LON — Sistema de Originación de Créditos
**Phase:** api-architecture-decisions / adr-generation

---

## Contexto

Las consultas al bureau de crédito tienen las siguientes características:
- **Costo unitario:** Cada consulta tiene un costo económico directo al banco
- **Latencia variable:** 200-800ms por consulta (API externa con SLA no garantizado)
- **Alta frecuencia de repetición:** El mismo reporte de un cliente puede ser consultado múltiples veces durante el proceso de evaluación (por el Analista, Gerente, Comité)
- **Ventana de validez:** Un reporte de bureau es válido por un período razonable (política interna: 24 horas) para el proceso de una misma solicitud

Sin caché, en un proceso donde 3 actores consultan el reporte del mismo cliente, el banco incurre en 3x el costo de consulta y latencia.

## Decisión

**Almacenar el reporte de bureau en Redis con TTL de 24 horas por cliente. Invalidar el caché manualmente si se requiere refresco.**

### Estrategia de caché:

```
Key:    bureau_report:{customerId}
Value:  {JSON serializado del reporte bureau}
TTL:    86400 segundos (24 horas)
Store:  Redis (instancia dedicada o compartida según política IT)
```

### Flujo de consulta (Cache-Aside Pattern):

```
risk-assessment-api.getBureauReport(customerId):
  1. GET Redis key "bureau_report:{customerId}"
  2. Si HIT → retornar reporte cacheado
  3. Si MISS → consultar Bureau API externa
  4. Si éxito → SET Redis key con TTL 24h → retornar reporte
  5. Si Bureau API falla → lanzar error (sin fallback a datos expirados)
```

### Invalidación manual:
- Endpoint privilegiado: `DELETE /v1/credit-reports/{customerId}/cache`
- Solo accesible por roles `RISK_ANALYST`, `CREDIT_MANAGER`
- Requiere justificación registrada en AuditLog

### Política de disponibilidad de Redis:
- Si Redis no disponible: **fallback a consulta directa al bureau**
- No bloquear el proceso por indisponibilidad del caché
- Registrar métrica de cache miss por fallo de Redis en Prometheus

## Consecuencias

**Positivas:**
- Reducción de costos de consulta al bureau (hasta 70% en escenarios de evaluación multi-actor)
- Latencia reducida para consultas repetidas (< 10ms vs 200-800ms externos)
- Riesgo de datos desactualizados mitigado por TTL corto (24h) — aceptable por política interna
- Fallback robusto: Redis no bloquea el flujo principal

**Negativas:**
- Dependencia de infraestructura Redis (pero no crítica — fallback disponible)
- Riesgo de datos desactualizados en ventana de 24h (aceptable por política crediticia)
- Política de invalidación requiere capacitación del equipo operativo
- Necesidad de monitorizar TTL expirations y hit rate del caché

## Configuración Redis Recomendada

```yaml
# Redis configuration para bureau cache
maxmemory-policy: allkeys-lru  # Evicción LRU cuando se alcanza el límite
maxmemory: 256mb               # Límite para reportes bureau
persistence: no                # Datos bureau no requieren persistencia en disco
replication: yes               # Replicación para disponibilidad
```

## Métricas a Monitorizar

```
bureau_cache_hit_rate          # Tasa de hits del caché
bureau_cache_miss_rate         # Tasa de misses
bureau_api_calls_total         # Total de llamadas al bureau externo
bureau_api_latency_p99         # Latencia P99 de llamadas al bureau
bureau_api_cost_savings        # Ahorro estimado por caché
```

## Alternativas Consideradas

| Alternativa | Razón de Rechazo |
|-------------|-----------------|
| Sin caché (consulta directa siempre) | Costo económico elevado; latencia inaceptable para UX |
| Caché en base de datos PostgreSQL | Mayor latencia que Redis; no es el propósito de una BD relacional |
| TTL de 1 hora | Demasiado corto; el proceso de evaluación puede durar más de 1 hora |
| TTL de 7 días | Riesgo de datos muy desactualizados; inaceptable para evaluación crediticia |
| Memcached | Menor funcionalidad que Redis; sin soporte nativo de TTL por clave |

## Referencias

- Source: `functionality/LON-AxetGaia-Sonnet46/input.yaml` → ADR-005, DDA-003
- BIAN: CustomerCreditRating — external credit agency report caching
- Pattern: Cache-Aside (Lazy Loading)
