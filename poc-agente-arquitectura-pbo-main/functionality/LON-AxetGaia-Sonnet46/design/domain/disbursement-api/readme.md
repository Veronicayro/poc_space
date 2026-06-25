# disbursement-api — Credit Disbursement Execution

**Layer:** Domain | **BIAN SD:** Disbursement (direct adoption) | **CR:** DisbursementTransaction | **Release:** 14.0.0

## Overview

El `disbursement-api` ejecuta el desembolso de créditos aprobados. Adopta directamente el SD BIAN Disbursement, usando el Control Record `DisbursementTransaction` para coordinar la transferencia de fondos al core bancario y registrar la confirmación.

## BIAN Alignment

| Campo | Valor |
|-------|-------|
| Service Domain | Disbursement |
| Control Record | DisbursementTransaction |
| Adoption Level | Direct |
| BIAN Baseline | `architecture/cache/bian/release14.0.0/oas3/yamls/Disbursement.yaml` |

## Endpoints (BIAN-derived)

| Método | Path | BIAN OperationId | Descripción |
|--------|------|------------------|-------------|
| POST | `/v1/Disbursement/Initiate` | `Initiate` | Iniciar instrucción de desembolso |
| PUT | `/v1/Disbursement/{disbursementid}/Execute` | `Execute` | Ejecutar desembolso en el core |
| PUT | `/v1/Disbursement/{disbursementid}/Exchange` | `Exchange` | Confirmar desembolso ejecutado |
| GET | `/v1/Disbursement/{disbursementid}/Retrieve` | `Retrieve` | Consultar estado del desembolso |

## Use Cases Cubiertos

| UC | Título | Actor |
|----|--------|-------|
| UC-LON-007 | Ejecutar desembolso | DISBURSEMENT_OFFICER |

## Data Flow

```
credit-origination-exp-api
  → disbursement-api: POST /Initiate (creditRequestId, destinationAccount, amount)
    → core-banking-adapter-api: POST /disbursements
      ← { core_reference, executed_at }
    → credit-request-api: Exchange (action: disbursed)
  ← { disbursementId, status: EXECUTED, core_reference }
```

## NFR

- SLA: < 2000ms (incluye llamada al core bancario)
- Idempotencia: via `Idempotency-Key` header
- Auditoría completa de cada instrucción de desembolso
