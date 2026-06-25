# invoice-management-api — README

**Layer:** Business  
**Version:** v1  
**Technology:** Node.js / Java Spring Boot  
**Base Path:** `/api/v1/invoices`  
**BIAN Alignment:** AccountsReceivable (semantic_alignment)

---

## Propósito

Servicio de negocio central para la gestión del ciclo de vida de facturas de proveedores. Implementa reglas de negocio de registro, aprobación, rechazo y cancelación. Delega la gestión de estados a `invoice-lifecycle-api`.

## Responsabilidades

- Registrar facturas con validación de proveedor activo (via `erp-integration-api`)
- Prevenir facturas duplicadas por `(supplier_id, invoice_number)` — BR-CXP-002
- Orquestar flujo de aprobación/rechazo con registro de auditoría
- Persistir entidad `Invoice` en PostgreSQL (schema: `cxp_invoices`)
- Delegar transiciones de estado a `invoice-lifecycle-api`

## Reglas de Negocio Implementadas

| Regla | Descripción |
|---|---|
| BR-CXP-001 | Proveedor debe existir y estar activo en ERP |
| BR-CXP-002 | Unicidad (supplier_id + invoice_number) |
| BR-CXP-003 | Estado inicial = PENDING |
| BR-CXP-005 | Registrar aprobador + timestamp |
| BR-CXP-006 | Motivo de rechazo obligatorio (10-500 chars) |
| BR-CXP-010 | Solo PENDING/APPROVED/SCHEDULED cancelables |

## Dependencias

- `invoice-lifecycle-api` — transiciones de estado y auditoría
- `erp-integration-api` — validación de proveedores

## Modelo de Datos (schema: cxp_invoices)

**invoices:** `(id, supplier_id, invoice_number, amount, currency, status, issue_date, due_date, created_at, updated_at)`  
**Unique constraint:** `(supplier_id, invoice_number)`  
**Indexes:** `[status, supplier_id, due_date, created_at]`
