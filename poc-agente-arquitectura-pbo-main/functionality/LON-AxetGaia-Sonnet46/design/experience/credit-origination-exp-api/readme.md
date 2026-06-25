# credit-origination-exp-api — Credit Origination BFF

**Layer:** Experience | **Type:** BFF (Backend for Frontend) | **BIAN:** N/A

## Overview

BFF que sirve la SPA React del sistema LON. Agrega y orquesta las APIs de dominio/negocio, calcula las acciones disponibles por rol/estado, y adapta los modelos de dominio a DTOs optimizados para cada vista del frontend.

## Key Design Decisions

- **Vistas por rol:** Las respuestas se adaptan según el claim `roles` del JWT
- **allowed_actions:** Calculado por el BFF para evitar lógica de permisos en el frontend
- **Paginación:** Cursor-based para listados de solicitudes
- **Errores:** RFC 7807 Problem Details en todos los endpoints
- **Idempotencia:** Via `Idempotency-Key` header en endpoints de acción

## Endpoints

| Método | Path | Roles | Descripción |
|--------|------|-------|-------------|
| GET | `/v1/credit-applications` | Todos | Listado con filtros por rol |
| POST | `/v1/credit-applications` | CREDIT_OFFICER | Crear solicitud |
| GET | `/v1/credit-applications/{id}` | Todos | Detalle de solicitud |
| GET | `/v1/credit-applications/{id}/timeline` | Todos | Historial de estados |
| POST | `/v1/credit-applications/{id}/documents` | CREDIT_OFFICER | Adjuntar documento |
| POST | `/v1/credit-applications/{id}/submit` | CREDIT_OFFICER | Enviar para evaluación |
| POST | `/v1/credit-applications/{id}/approve` | CREDIT_MANAGER, CREDIT_COMMITTEE | Aprobar |
| POST | `/v1/credit-applications/{id}/reject` | CREDIT_MANAGER, CREDIT_COMMITTEE | Rechazar |
| POST | `/v1/credit-applications/{id}/escalate` | CREDIT_MANAGER | Escalar al comité |
| POST | `/v1/credit-applications/{id}/disburse` | DISBURSEMENT_OFFICER | Ejecutar desembolso |

## NFR

- SLA: < 500ms
- Idempotencia en todos los endpoints de acción
