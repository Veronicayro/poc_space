# credit-bureau-adapter-api — Credit Bureau Integration Adapter

**Layer:** Support | **External System:** Bureau de Crédito (Equifax/TransUnion/Experian)

## Overview

Adaptador que abstrae la integración con el bureau de crédito externo. Implementa caché Redis TTL 24h (Cache-Aside), circuit breaker y retry para garantizar resiliencia y reducir costos de consulta.

## Endpoints

| Método | Path | Descripción |
|--------|------|-------------|
| GET | `/v1/credit-reports/{customerId}` | Obtener reporte (cache-aside) |
| POST | `/v1/credit-reports/query` | Consulta detallada con parámetros |
| DELETE | `/v1/credit-reports/{customerId}/cache` | Invalidar caché manualmente |

## Caché Redis — TTL 24h

```
HIT:  Redis → score, historial, deudas, blacklist_status (< 10ms)
MISS: Bureau API externa → Redis SET TTL 24h → respuesta (200-800ms)
FAIL Redis: Consulta directa al bureau (fallback)
```

## Resiliencia

- **Circuit Breaker:** Abre si 5 fallos en 30s; cierra tras recuperación del bureau
- **Retry:** Hasta 3 reintentos con backoff exponencial (100ms, 200ms, 400ms)
- **Timeout:** 800ms por request al bureau externo

## NFR

- Cache hit: < 10ms | Cache miss: < 800ms
- Métricas: `bureau_cache_hit_rate`, `bureau_api_calls_total` en Prometheus
