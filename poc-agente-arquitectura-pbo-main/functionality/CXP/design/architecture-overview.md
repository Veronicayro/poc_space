# Architecture Overview - Cuentas por Pagar (CXP)

**Functionality:** CXP - Cuentas por Pagar  
**Phase:** solution-landscape  
**Date:** 2026-06-17  
**Architecture Style:** Microservices - Layered (Experience → Business → Domain → Support)  
**Domain Standard:** BIAN Release 14

---

## Visión de Solución

El sistema de **Cuentas por Pagar (CXP)** es una solución greenfield de microservicios que gestiona el ciclo de vida completo de facturas de proveedores: desde el registro hasta la confirmación de pago bancario. La arquitectura garantiza integridad contable, trazabilidad completa y cumplimiento regulatorio (SOX/ISO27001).

---

## Diagrama Conceptual de Capas

```
┌─────────────────────────────────────────────────────────────────┐
│                    CANAL WEB (React SPA)                        │
│         Analista Financiero | Gerente | Tesorero                │
└────────────────────────┬────────────────────────────────────────┘
                         │ OAuth2/OIDC + RBAC
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│               EXPERIENCE LAYER (BFF)                            │
│           accounts-payable-exp-api                              │
│    Agrega: invoices + payments + status para la UI              │
└──────────────┬─────────────────────────┬───────────────────────┘
               │                         │
               ▼                         ▼
┌──────────────────────────┐  ┌──────────────────────────────────┐
│     BUSINESS LAYER       │  │        BUSINESS LAYER            │
│  invoice-management-api  │  │    payment-management-api        │
│  Lógica: registro,       │  │    Lógica: programación,         │
│  aprobación, rechazo,    │  │    ejecución, estado de pagos    │
│  cancelación facturas    │  │                                  │
└───────────┬──────────────┘  └──────────────┬───────────────────┘
            │                                │
            └──────────────┬─────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  DOMAIN LAYER                                   │
│              invoice-lifecycle-api                              │
│    State Machine: PENDING→APPROVED/REJECTED/SCHEDULED/PAID      │
│    Audit Trail: AuditLog inmutable                              │
└──────────────────────┬──────────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
┌───────────────────┐    ┌─────────────────────────────────────┐
│  SUPPORT LAYER    │    │         SUPPORT LAYER               │
│ erp-integration   │    │      banking-integration-api        │
│ -api              │    │   REST API + Webhooks HMAC-SHA256   │
│ Validación        │    │   Idempotency-Key, Circuit Breaker  │
│ proveedores +     │    │                                     │
│ asientos contables│    └──────────────┬──────────────────────┘
└────────┬──────────┘                   │
         │                             │
         ▼                             ▼
┌────────────────┐          ┌──────────────────────┐
│   ERP System   │          │   Banking System      │
│ REST API/Batch │          │  REST API + Webhooks  │
└────────────────┘          └──────────────────────┘
```

---

## Bounded Contexts

### BC-1: Invoice Management
- **APIs:** invoice-management-api, invoice-lifecycle-api
- **Responsabilidad:** Ciclo de vida completo de facturas
- **Datos propios:** Invoice, StateTransition, AuditLog
- **BIAN:** AccountsReceivable (semántica)

### BC-2: Payment Management
- **APIs:** payment-management-api
- **Responsabilidad:** Programación y ejecución de pagos
- **Datos propios:** PaymentOrder, PaymentSchedule
- **BIAN:** Disbursement (semántica)

### BC-3: Financial Integration
- **APIs:** erp-integration-api, banking-integration-api
- **Responsabilidad:** Conectividad con sistemas externos
- **BIAN:** FinancialAccounting, FinancialGateway (referencia)

---

## Flujos Clave

### Flujo 1: Registro y Aprobación de Factura
```
Analista → exp-api → invoice-management-api → invoice-lifecycle-api (PENDING)
                   └→ erp-integration-api → ERP (validar proveedor)
Gerente → exp-api → invoice-management-api → invoice-lifecycle-api (APPROVED)
```

### Flujo 2: Programación y Ejecución de Pago
```
Tesorero → exp-api → payment-management-api → invoice-lifecycle-api (SCHEDULED)
                   └→ banking-integration-api → Banking System
Banking Webhook → banking-integration-api → payment-management-api → invoice-lifecycle-api (PAID)
                                          └→ erp-integration-api → ERP (asiento contable)
```

---

## Stack Tecnológico

| Capa | Tecnología | Patrón |
|------|-----------|--------|
| Frontend | React SPA | BFF Pattern |
| Experience API | Node.js (Express) | BFF / Aggregator |
| Business APIs | Node.js / Java Spring Boot | Layered + DTO/Mapper |
| Domain API | Node.js / Java Spring Boot | State Machine |
| Support APIs | Node.js / Java Spring Boot | Adapter + Circuit Breaker |
| Base de datos | PostgreSQL | Schema-per-service, ACID |
| Auth | OAuth2/OIDC (Keycloak) | RBAC |
| Observabilidad | OpenTelemetry + Prometheus | Distributed Tracing |

---

## NFR Summary

| NFR | Target |
|-----|--------|
| Performance | < 300ms SLA, 500 usuarios concurrentes |
| Security | OAuth2/OIDC + RBAC + TLS 1.2+ |
| Observability | OpenTelemetry + Prometheus + JSON logs |
| Reliability | Retry (3x exp backoff) + Circuit Breaker |
| Compliance | AuditLog completo (SOX/ISO27001) |
| Idempotencia | X-Idempotency-Key para pagos bancarios |
