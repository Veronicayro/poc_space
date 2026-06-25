# ADR-CXP-004: Lifecycle Basado en Máquina de Estados

**Status:** Accepted  
**Date:** 2026-06-17  
**Functionality:** CXP - Cuentas por Pagar  
**Ref:** DDA-001 del contexto del task

---

## Contexto

El ciclo de vida de las facturas involucra múltiples estados y transiciones controladas. Se necesita un mecanismo que garantice la integridad de los cambios de estado, prevenga transiciones inválidas y mantenga un historial completo para auditoría.

## Decisión

Se implementa una **State Machine** (máquina de estados finitos) como servicio de dominio dedicado (`invoice-lifecycle-api`) para gestionar el ciclo de vida de las facturas.

**Estados:** PENDING → APPROVED/REJECTED/CANCELLED | APPROVED → SCHEDULED/CANCELLED | SCHEDULED → PAID/CANCELLED

**Implementación:**
- Servicio de dominio puro (sin dependencias externas)
- Validación de transición en base a tabla de transiciones válidas (BR-CXP-004)
- Historial inmutable de transiciones (append-only)
- Audit log completo por operación

## Justificación

- Garantiza que solo transiciones válidas sean ejecutadas (previene estados inválidos)
- Separación de responsabilidades: la lógica de estados está aislada en un dominio puro
- Alineado con BIAN: `InvoiceLifecycleProcedure` mapea a `AccountsReceivableProcedure`
- Historial inmutable cumple requisitos SOX/ISO27001
- Facilita debugging y trazabilidad de cualquier cambio de estado

## Consecuencias

- **+** Mayor trazabilidad y control sobre el ciclo de vida
- **+** Previene transiciones inválidas a nivel de servicio
- **+** Audit trail completo para cumplimiento regulatorio
- **-** Complejidad adicional: las APIs de negocio deben llamar al lifecycle service
- **-** Latencia adicional por llamada al servicio de dominio (mitigado: SLA interno < 100ms)
- **Restricción:** Toda transición de estado DEBE pasar por `invoice-lifecycle-api`; nunca se debe actualizar directamente la columna `status` en `cxp_invoices.invoices`
