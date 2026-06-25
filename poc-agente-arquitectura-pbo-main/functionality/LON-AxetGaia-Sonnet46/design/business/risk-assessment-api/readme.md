# risk-assessment-api — Credit Risk Assessment

**Layer:** Business | **BIAN SD:** Underwriting (semantic_alignment) + CustomerCreditRating | **Release:** 14.0.0

## Overview

El `risk-assessment-api` gestiona la evaluación de riesgo crediticio del solicitante. Orquesta la consulta al bureau de crédito externo (con caché Redis TTL 24h), calcula el DTI ratio, y produce la evaluación que determina si la solicitud debe ser aprobada por el gerente o escalada al comité.

## BIAN Alignment

| Campo | Valor |
|-------|-------|
| Primary SD | Underwriting |
| Secondary SD | CustomerCreditRating |
| Control Record | UnderwritingAssessment |
| Adoption Level | Semantic Alignment |
| BIAN Baseline | `architecture/cache/bian/release14.0.0/oas3/yamls/Underwriting.yaml` |

## Endpoints

| Método | Path | Operación BIAN | Descripción |
|--------|------|----------------|-------------|
| POST | `/v1/Underwriting/Initiate` | Initiate | Iniciar evaluación de riesgo |
| GET | `/v1/Underwriting/{id}/Retrieve` | Retrieve | Consultar evaluación existente |
| PUT | `/v1/Underwriting/{id}/Update` | Update | Actualizar evaluación |
| PUT | `/v1/Underwriting/{id}/Exchange` | Exchange | Intercambiar reporte bureau |

## Risk Decision Logic

```
score >= umbral_aprobacion_alto  AND dti <= dti_max  → APPROVE (CREDIT_MANAGER)
score >= umbral_aprobacion_bajo  AND riesgo <= MEDIUM → APPROVE (CREDIT_MANAGER)
score < umbral_aprobacion_bajo                        → REJECT (auto-suggest)
monto > limite_gerente OR riesgo IN [HIGH, CRITICAL]  → ESCALATE (CREDIT_COMMITTEE)
```

## Use Cases Cubiertos

| UC | Título | Actor |
|----|--------|-------|
| UC-LON-003 | Evaluar riesgo crediticio | RISK_ANALYST |
| UC-LON-002 | (bureau trigger automático al submit) | System |

## Dependencies

| Servicio | Propósito | Tipo |
|----------|-----------|------|
| credit-bureau-adapter-api | Score + reporte crediticio (caché Redis 24h) | Síncrono |

## NFR

- SLA: < 1000ms (incluyendo tiempo de bureau en caché)
- Caché Redis TTL 24h para reducir costos de bureau
- Fallback: consulta directa al bureau si Redis no disponible
