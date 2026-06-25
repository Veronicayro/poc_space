# core-banking-adapter-api — Core Banking Integration Adapter

**Layer:** Support | **External System:** Core Bancario

## Overview

Adaptador que abstrae la integración con el Core Bancario para las operaciones críticas del proceso de originación: validación KYC, creación del producto crédito y ejecución del desembolso.

## Endpoints

| Método | Path | Descripción |
|--------|------|-------------|
| GET | `/v1/customers/{customerId}/kyc` | Validar cliente (KYC) |
| POST | `/v1/loan-products` | Crear producto crédito en core |
| POST | `/v1/disbursements` | Ejecutar instrucción de desembolso |
| GET | `/v1/disbursements/{id}/status` | Consultar estado del desembolso |
| GET | `/v1/amortization-schedules/{loanId}` | Consultar tabla de amortización |

## Resiliencia

- **Circuit Breaker:** 5 fallos en 30s → abre; 60s recovery check
- **Retry:** 3 reintentos con backoff exponencial para KYC y desembolso
- **Idempotencia:** `Idempotency-Key` header obligatorio en POST /disbursements

## NFR

- KYC SLA: < 1000ms | Desembolso SLA: < 3000ms
- El desembolso es operación crítica: si falla tras reintentos, requiere intervención manual
