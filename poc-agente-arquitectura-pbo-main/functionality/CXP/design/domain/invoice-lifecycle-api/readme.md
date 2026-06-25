# invoice-lifecycle-api — README

**Layer:** Domain  
**Version:** v1  
**Technology:** Node.js / Java Spring Boot  
**Base Path:** `/api/v1/invoice-lifecycle`  
**BIAN Alignment:** AccountsReceivable → InvoiceLifecycleProcedure

---

## Propósito

Servicio de dominio puro para gestión de la máquina de estados de facturas. No tiene dependencias externas. Es la única fuente de verdad sobre el estado y la historia de cada factura.

## State Machine

```
PENDING → APPROVED → SCHEDULED → PAID
PENDING → REJECTED
PENDING/APPROVED/SCHEDULED → CANCELLED
```

## Reglas de Negocio

- **BR-CXP-004:** Solo transiciones válidas permitidas
- **BR-CXP-005:** Registro de aprobador + timestamp inmutable
- **BR-CXP-013:** Audit trail completo (SOX/ISO27001)

## Persistencia (schema: cxp_lifecycle)

- `invoice_lifecycle` — estado actual por factura
- `state_transitions` — historial inmutable
- `audit_log` — registro de auditoría completo
