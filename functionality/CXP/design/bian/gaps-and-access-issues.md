# BIAN Gaps and Access Issues - Cuentas por Pagar (CXP)

**Phase:** enterprise-capability-alignment  
**Date:** 2026-06-17  
**BIAN Release:** 14.0.0  
**Gate Status:** ✅ PASS

---

## Access Status

| Service Domain | Local Cache | Status |
|---|---|---|
| AccountsReceivable | architecture/cache/bian/release14.0.0/asyncapi-3.x/yamls/AccountsReceivable.yaml | ✅ Available |
| Disbursement | architecture/cache/bian/release14.0.0/asyncapi-3.x/yamls/Disbursement.yaml | ✅ Available |
| FinancialAccounting | architecture/cache/bian/release14.0.0/asyncapi-3.x/yamls/FinancialAccounting.yaml | ✅ Available |
| ContractorandSupplierAgreement | architecture/cache/bian/release14.0.0/asyncapi-3.x/yamls/ContractorandSupplierAgreement.yaml | ✅ Available |
| FinancialGateway | architecture/cache/bian/release14.0.0/asyncapi-3.x/yamls/FinancialGateway.yaml | ✅ Available |

**No access issues.** Todos los Service Domains están disponibles en caché local.

---

## Semantic Gaps

### GAP-BIAN-001: Ausencia de Service Domain "Accounts Payable"
- **Severity:** Medium
- **Description:** BIAN R14 no tiene SD dedicado para AP. El SD más cercano es `AccountsReceivable`.
- **Resolution:** Adaptación semántica: `AccountsReceivableProcedure` → `InvoiceLifecycleProcedure`. Dirección invertida (Supplier=acreedor, Org=deudor).
- **Impact:** Bajo.

### GAP-BIAN-002: ContractorandSupplierAgreement — alcance parcial
- **Severity:** Low
- **Description:** CXP solo requiere consultar si un proveedor existe; no implementa el dominio completo.
- **Resolution:** Uso como referencia semántica. Validación delegada al ERP via `erp-integration-api`.
- **Impact:** Bajo.

---

## Contract Adoption Gate (Phase 7 pre-check)

| SD | Adoption Level | Contract Derivation | Gate |
|---|---|---|---|
| AccountsReceivable | semantic_alignment | No (OpenAPI propio) | ✅ PASS |
| Disbursement | semantic_alignment | No (OpenAPI propio) | ✅ PASS |
| FinancialAccounting | reference | No | ✅ PASS |
| ContractorandSupplierAgreement | reference | No | ✅ PASS |
| FinancialGateway | reference | No | ✅ PASS |

**Conclusión:** BLOCK-01 (Phase 7) no aplica. Nivel de adopción es semántico/referencia.
