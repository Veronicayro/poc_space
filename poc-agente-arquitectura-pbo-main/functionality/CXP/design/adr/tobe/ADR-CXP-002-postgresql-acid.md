# ADR-CXP-002: PostgreSQL como Base de Datos Principal

**Status:** Accepted  
**Date:** 2026-06-17  
**Functionality:** CXP - Cuentas por Pagar  
**Ref:** ADR-001 del contexto del task

---

## Contexto

El sistema CXP gestiona el ciclo de vida de facturas con múltiples transiciones de estado, auditoría completa y requisitos de integridad transaccional. Se requiere una base de datos que garantice ACID compliance para operaciones financieras críticas.

## Decisión

Se adopta **PostgreSQL** como motor de base de datos principal para todos los componentes CXP, con el patrón **schema-per-service**.

**Schemas:**
- `cxp_invoices` — invoice-management-api
- `cxp_payments` — payment-management-api
- `cxp_lifecycle` — invoice-lifecycle-api (incluye audit_log)
- `cxp_banking` — banking-integration-api (idempotency log)

## Justificación

- **ACID compliance** requerida para operaciones financieras críticas
- Soporte nativo para **transacciones serializable** (prevención de race conditions en state transitions)
- **JSON/JSONB** para auditoría flexible
- **Índices parciales** para queries por status + supplier_id (rendimiento SLA < 300ms)
- Schema-per-service mantiene aislamiento lógico entre microservicios
- Amplio soporte en ecosistema cloud (RDS, Cloud SQL, Azure Database for PostgreSQL)

## Alternativas Consideradas

| Alternativa | Razón de descarte |
|---|---|
| MongoDB | Sin garantías ACID nativas; inconsistencias en operaciones financieras |
| MySQL | Menor soporte para features avanzados (row-level locking, JSONB) |
| Oracle | Licenciamiento costoso; menor portabilidad cloud |

## Consecuencias

- **+** Fuerte integridad transaccional
- **+** Cumplimiento SOX/ISO27001 (audit trail inmutable)
- **+** Soporte para tablas de audit log append-only (SECURITY DEFINER)
- **-** Mayor complejidad operativa vs NoSQL para datos no estructurados
- **-** Requiere gestión de migraciones (Flyway/Liquibase)
- **Restricción:** Las tablas de auditoría (audit_log, state_transitions, idempotency_log) son APPEND-ONLY; no se permiten UPDATE ni DELETE

## Índices Requeridos

```sql
-- invoice-management-api
CREATE INDEX idx_invoices_status ON cxp_invoices.invoices(status);
CREATE INDEX idx_invoices_supplier ON cxp_invoices.invoices(supplier_id);
CREATE INDEX idx_invoices_due_date ON cxp_invoices.invoices(due_date);
UNIQUE INDEX idx_invoices_uniqueness ON cxp_invoices.invoices(supplier_id, invoice_number);

-- payment-management-api
CREATE INDEX idx_payments_status ON cxp_payments.payment_orders(status);
CREATE INDEX idx_payments_invoice ON cxp_payments.payment_orders(invoice_id);
UNIQUE INDEX idx_idempotency ON cxp_payments.payment_orders(idempotency_key);
