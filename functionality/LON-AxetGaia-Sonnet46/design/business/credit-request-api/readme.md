# credit-request-api — Loan Credit Request Management

**Layer:** Business | **BIAN SD:** CustomerOffer (semantic_alignment) | **Release:** 14.0.0

## Overview

El `credit-request-api` es la API central del sistema LON. Gestiona el ciclo de vida completo de las solicitudes de crédito bancario, desde el registro inicial hasta la aprobación o rechazo, implementando una state machine explícita de 12 estados con transiciones controladas por rol y nivel de atribución.

## BIAN Alignment

| Campo | Valor |
|-------|-------|
| Service Domain | CustomerOffer |
| Control Record | CustomerOffer |
| Adoption Level | Semantic Alignment |
| BIAN Baseline | `architecture/cache/bian/release14.0.0/oas3/yamls/CustomerOffer.yaml` |

**Adaptaciones respecto al SD BIAN:**
- La state machine de 12 estados es una extensión del CR CustomerOffer (BIAN no define explícitamente todos los estados LON)
- El escalado multinivel (gerente → comité) es una extensión de dominio bancario
- El DTI ratio se agrega como campo de evaluación no definido en BIAN CustomerOffer

## Endpoints

| Método | Path | Operación BIAN | Descripción |
|--------|------|----------------|-------------|
| POST | `/v1/CustomerOffer/Initiate` | Initiate | Crear solicitud (→ DRAFT) |
| GET | `/v1/CustomerOffer/{id}/Retrieve` | Retrieve | Consultar solicitud |
| PUT | `/v1/CustomerOffer/{id}/Update` | Update | Actualizar datos (solo DRAFT) |
| PUT | `/v1/CustomerOffer/{id}/Exchange` | Exchange | Ejecutar transición de estado |
| GET | `/v1/CustomerOffer` | Query | Listar solicitudes con filtros |

## State Machine

```
DRAFT
  └─[submit: CREDIT_OFFICER]──► SUBMITTED
                                    └─[assign: RISK_ANALYST]──► UNDER_REVIEW
                                                                    └─[assess]──► RISK_ASSESSED
                                                                                    └─[auto]──► PENDING_APPROVAL
                                                                                                    ├─[approve within limit]──► APPROVED ──► PENDING_DISBURSEMENT ──► DISBURSED
                                                                                                    ├─[reject]──► REJECTED
                                                                                                    └─[escalate / exceeds limit]──► PENDING_COMMITTEE
                                                                                                                                         ├─[approve]──► APPROVED
                                                                                                                                         └─[reject]──► REJECTED
```

**Estados terminales:** REJECTED, CANCELLED, EXPIRED, DISBURSED

## Use Cases Cubiertos

| UC | Título | Actor |
|----|--------|-------|
| UC-LON-001 | Registrar solicitud de crédito | CREDIT_OFFICER |
| UC-LON-002 | Enviar solicitud para evaluación | CREDIT_OFFICER |
| UC-LON-004 | Aprobar solicitud | CREDIT_MANAGER |
| UC-LON-005 | Rechazar solicitud | CREDIT_MANAGER, CREDIT_COMMITTEE |
| UC-LON-006 | Escalar al Comité | CREDIT_MANAGER |
| UC-LON-008 | Consultar estado de solicitud | Todos los roles |

## Data Model (summary)

| Entidad | Tabla | Descripción |
|---------|-------|-------------|
| CreditRequest | credit_requests | Solicitud principal con estado |
| CreditDecision | credit_decisions | Decisiones con trazabilidad |
| CreditDocument | credit_documents | Referencias DMS de documentos |
| AuditLog | audit_logs | Historial inmutable de transiciones |

## Dependencies

| Servicio | Propósito | Tipo |
|----------|-----------|------|
| core-banking-adapter-api | Validación KYC | Síncrono |
| dms-adapter-api | Gestión de documentos | Síncrono |

## NFR

- SLA: < 500ms por request
- Idempotencia: endpoints de creación y transición de estado
- Auditoría completa: todas las acciones registradas en AuditLog
- Retención: 7 años mínimo (compliance)
- ACID: transacciones PostgreSQL para cambios de estado atómicos
