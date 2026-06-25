# erp-integration-api — README

**Layer:** Support  
**Version:** v1  
**Technology:** Node.js / Java Spring Boot  
**Base Path:** `/api/v1/erp`  
**BIAN Alignment:** FinancialAccounting + ContractorandSupplierAgreement (reference)

---

## Propósito

Anti-Corruption Layer (ACL) entre el dominio CXP y el sistema ERP externo. Transforma mensajes, gestiona resiliencia (circuit breaker + retry) y cachea validaciones frecuentes.

## Responsabilidades

- Validar proveedores activos en ERP (con cache 5min)
- Registrar asientos contables post-pago (FinancialAccounting.LedgerPosting)
- Transformación CXP schema ↔ ERP schema
- Circuit breaker ante fallos del ERP

## Resiliencia

| Patrón | Config |
|---|---|
| Retry | max 3, exponential backoff 500ms |
| Circuit Breaker | threshold 5 fallos, timeout 30s |
| Cache | TTL 300s para validación proveedores |

## Dependencia Externa

- **ERP System** — REST API, OAuth2 client credentials, TLS 1.2+
