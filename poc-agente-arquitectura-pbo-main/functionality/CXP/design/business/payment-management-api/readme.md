# payment-management-api — README

**Layer:** Business  
**Version:** v1  
**Technology:** Node.js / Java Spring Boot  
**Base Path:** `/api/v1/payments`  
**BIAN Alignment:** Disbursement (semantic_alignment)

---

## Propósito

Servicio de negocio para programación y ejecución de pagos a proveedores. Orquesta el flujo APPROVED→SCHEDULED→PAID coordinando con `banking-integration-api` para la ejecución real y con `invoice-lifecycle-api` para las transiciones de estado.

## Responsabilidades

- Crear órdenes de pago (PaymentOrder) con validación de estado APPROVED
- Ejecutar pagos con idempotencia (X-Idempotency-Key)
- Recibir y procesar confirmaciones bancarias vía webhook
- Transicionar facturas a SCHEDULED y PAID

## Reglas de Negocio

| Regla | Descripción |
|---|---|
| BR-CXP-007 | Solo facturas APPROVED pueden programarse |
| BR-CXP-008 | Fecha de pago debe ser futura |
| BR-CXP-009 | Idempotencia en ejecución de pagos |

## Idempotencia

- Header: `X-Idempotency-Key` en ejecución de pagos
- Clave: `hash(invoice_id + payment_id + execution_date)`
- Tabla: `idempotency_log` en schema `cxp_payments`

## Dependencias

- `invoice-lifecycle-api` — transiciones de estado
- `banking-integration-api` — ejecución de pagos + confirmaciones
