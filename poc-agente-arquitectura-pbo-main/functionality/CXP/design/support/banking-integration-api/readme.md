# banking-integration-api — README

**Layer:** Support  
**Version:** v1  
**Technology:** Node.js / Java Spring Boot  
**Base Path:** `/api/v1/banking`  
**BIAN Alignment:** FinancialGateway (reference)

---

## Propósito

Adaptador para integración con el Banking System externo. Gestiona envío de órdenes de pago, recepción de confirmaciones bancarias via webhook con validación HMAC-SHA256, e idempotencia para prevenir pagos duplicados.

## Responsabilidades

- Enviar PaymentOrders al banco con X-Idempotency-Key
- Recibir y validar webhooks bancarios (HMAC-SHA256)
- Garantizar idempotencia (banking_idempotency_log)
- Circuit breaker y retry para resiliencia

## Seguridad de Webhooks

1. Validar firma HMAC-SHA256 del header `X-Banking-Signature`
2. Verificar timestamp del evento (prevenir replay attacks)
3. Comprobar event_id en `banking_idempotency_log` (idempotencia)
4. Procesar solo si pasa todas las validaciones

## Resiliencia

| Patrón | Config |
|---|---|
| Retry | max 3, exp backoff 1000ms, idempotente |
| Circuit Breaker | threshold 3 fallos, timeout 60s |

## Dependencia Externa

- **Banking System** — REST API, mTLS + API Key, TLS 1.2+, HMAC-SHA256 webhooks
