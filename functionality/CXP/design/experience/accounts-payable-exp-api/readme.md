# accounts-payable-exp-api — README

**Layer:** Experience (BFF)  
**Version:** v1  
**Technology:** Node.js (Express)  
**Base Path:** `/api/v1/accounts-payable`

---

## Propósito

BFF (Backend for Frontend) para la SPA React de Cuentas por Pagar. Punto único de entrada del canal web que agrega datos de `invoice-management-api` y `payment-management-api`, aplica RBAC y adapta respuestas al modelo de presentación de la UI.

## Responsabilidades

- Exponer endpoints REST para gestión de facturas y pagos
- Validar tokens JWT (OAuth2/OIDC) y enforcement de RBAC
- Agregar/componer respuestas de APIs downstream
- Propagar `X-Correlation-ID` para trazabilidad distribuida
- Formatear errores según RFC 7807

## Endpoints

| Método | Path | Rol requerido |
|--------|------|---------------|
| GET | /invoices | ALL |
| POST | /invoices | ANALYST |
| GET | /invoices/{id} | ALL |
| PUT | /invoices/{id} | ANALYST |
| POST | /invoices/{id}/approve | MANAGER |
| POST | /invoices/{id}/reject | MANAGER |
| POST | /invoices/{id}/cancel | ANALYST, MANAGER |
| POST | /invoices/{id}/schedule-payment | TREASURER |
| GET | /payments | TREASURER |
| GET | /payments/{id} | TREASURER |

## Dependencias Downstream

- `invoice-management-api` — operaciones de facturas
- `payment-management-api` — operaciones de pagos

## Seguridad

- OAuth2/OIDC — Bearer token JWT
- RBAC middleware por endpoint
- TLS 1.2+ en todas las comunicaciones

## NFRs

- SLA: < 300ms
- Observabilidad: OpenTelemetry + Prometheus + JSON logs
- Errores: RFC 7807 Problem Details
