# Gaps and Assumptions - Cuentas por Pagar (CXP)

**Functionality:** CXP - Cuentas por Pagar  
**Date:** 2026-06-17  
**Status:** Discovery complete

---

## Gaps Identificados

| ID | Área | Descripción | Severidad | Mitigación |
|----|------|-------------|-----------|------------|
| GAP-001 | Discovery | Sistema greenfield; no existe API legacy de AP | Low | Diseño greenfield sin impacto legacy |
| GAP-002 | Integration | Esquemas/endpoints del ERP no especificados | Medium | Modelar IntegrationAdapter con contratos placeholder |
| GAP-003 | Integration | Mecanismo de autenticación del Banking System no especificado | Medium | Asumir REST + mutual TLS + HMAC webhook signing |
| GAP-004 | Frontend | No hay referencias Figma disponibles | Low | Diseño basado en patrones financieros (tablas + filtros) |
| GAP-005 | NFR | Proveedor de cloud no especificado | Low | Diseño cloud-agnostic con Kubernetes |

---

## Supuestos de Arquitectura

| ID | Supuesto |
|----|----------|
| ASS-001 | Sistema greenfield; no hay migración de APIs legacy |
| ASS-002 | OAuth2/OIDC con Keycloak (o equivalente) para autenticación/autorización |
| ASS-003 | BIAN Release 14 como estándar de dominio; Service Domains: AccountsReceivable, Disbursement, FinancialAccounting, ContractorandSupplierAgreement, FinancialGateway |
| ASS-004 | Arquitectura en capas: Experience → Business → Domain → Support/Integration |
| ASS-005 | PostgreSQL como base de datos principal (ACID compliance requerida) |
| ASS-006 | Arquitectura de microservicios desplegada en contenedores (Docker/Kubernetes) |
| ASS-007 | Observabilidad con OpenTelemetry + Prometheus + logging estructurado (JSON) |
| ASS-008 | Retry policy con circuit breaker para integraciones externas (ERP, Banking) |
| ASS-009 | TLS 1.2+ para todas las comunicaciones entre servicios y sistemas externos |

---

## Decisiones de Diseño Previas (del contexto del task)

### DDA-001: Lifecycle basado en máquina de estados
- **Decisión:** Los estados de factura se gestionan mediante state machine
- **Implicación:** WorkflowService como componente dedicado para validación de transiciones

### DDA-002: API REST
- **Decisión:** Interfaces mediante REST API versionadas
- **Implicación:** Versionamiento /v1/ en todos los endpoints; stateless

### DDA-003: Integración por webhooks con Banking System
- **Decisión:** Webhooks para comunicación asincrónica con banco
- **Implicación:** Idempotencia obligatoria; manejo de eventos duplicados con idempotency_key

---

## ADRs Previos (del contexto del task)

### ADR-001: PostgreSQL
- **Status:** Accepted
- **Justificación:** Consistencia transaccional (ACID) para ciclo de vida de facturas

### ADR-002: Arquitectura basada en servicios
- **Status:** Accepted
- **Justificación:** Escalabilidad y mantenibilidad

### ADR-003: RBAC
- **Status:** Accepted
- **Justificación:** Control de acceso por rol (ANALYST, MANAGER, TREASURER)
