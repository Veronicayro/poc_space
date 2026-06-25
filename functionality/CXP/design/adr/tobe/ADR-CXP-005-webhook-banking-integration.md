# ADR-CXP-005: Integración con Banking System via REST + Webhooks

**Status:** Accepted  
**Date:** 2026-06-17  
**Functionality:** CXP - Cuentas por Pagar  
**Ref:** DDA-003 del contexto del task

---

## Contexto

El sistema CXP necesita comunicarse con el Banking System externo para ejecutar pagos y recibir confirmaciones. Se requiere un mecanismo que sea eficiente, seguro y que garantice exactamente-una-vez semántica (idempotencia) para evitar pagos duplicados.

## Decisión

Se adopta **REST API saliente + Webhooks entrantes** como patrón de integración con el Banking System:

- **Outbound:** REST HTTPS con mTLS + API Key; header `X-Idempotency-Key` obligatorio
- **Inbound:** Webhooks con validación de firma **HMAC-SHA256** y verificación de timestamp
- **Idempotencia:** Log de `event_id` en `cxp_banking.banking_idempotency_log`
- **Resiliencia:** Circuit breaker (threshold 3, timeout 60s) + retry exponencial (max 3)

## Justificación

- **REST saliente:** Ampliamente soportado por plataformas bancarias; sincrónico para confirmación inicial
- **Webhooks entrantes:** Comunicación asincrónica eficiente; el banco notifica cuando el pago se confirma sin polling
- **HMAC-SHA256:** Estándar de seguridad para webhooks bancarios (previene spoofing)
- **Idempotency-Key:** Previene pagos duplicados en reintentos (BR-CXP-009)
- Alineado con BIAN FinancialGateway pattern

## Alternativas Consideradas

| Alternativa | Razón de descarte |
|---|---|
| Polling activo | Ineficiente; incrementa carga en Banking System; latencia alta |
| Message Broker (Kafka/SQS) | Mayor complejidad; Banking System puede no soportarlo |
| gRPC streaming | Bajo soporte en plataformas bancarias legacy |

## Consecuencias

- **+** Comunicación asincrónica eficiente para confirmaciones
- **+** Idempotencia garantiza exactamente-una-vez semántica
- **+** HMAC-SHA256 previene eventos falsos
- **-** Dependencia de disponibilidad del Banking System (mitigado: circuit breaker)
- **-** Necesidad de gestionar endpoint público para webhooks (requiere configuración en Banking)
- **Restricción:** El `X-Idempotency-Key` es OBLIGATORIO para `POST /banking/payment-orders`
- **Restricción:** Los webhooks DEBEN validar firma antes de procesar; rechazar con 400 si firma inválida
- **Restricción:** Timestamps de webhook con antigüedad > 300 segundos deben ser rechazados (anti-replay)
