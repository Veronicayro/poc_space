# Phase 0 Decision — KYC_ONBOARDING_DIGITAL

**Request ID:** KYC_ONBOARDING_DIGITAL  
**Timestamp:** 2026-06-22  
**Functionality:** Digital KYC Onboarding  
**Target component:** `kyc-onboarding-api`  

---

## Decision: CREATE

**API Identificada:** N/A (ninguna API existente cubre el caso de orquestación de onboarding end-to-end)

**Dominio:** Customers / CustomerOnboarding (nuevo API Product dentro de la capacidad existente)

---

## Análisis

### Catálogo consultado

| API | Capability | Version | Status | Archivo |
|---|---|---|---|---|
| CustomerProfileAPI | Customers/CustomerOnboarding | 1.2.0 | Published | `catalog/domains/customers.yaml` |
| CustomerIdentityAPI | Customers/CustomerOnboarding | 1.1.0 | Published | `catalog/domains/customers.yaml` |
| KYCScreeningAPI | Compliance/KYC | 3.0.0 | Published | `catalog/domains/compliance.yaml` |

### Cobertura de casos de uso

| Caso de Uso | API Catálogo | Cobertura |
|---|---|---|
| UC-001: Registro cliente digital | CustomerProfileAPI `POST /customers` | ~70% |
| UC-002: Carga de documentos | CustomerIdentityAPI `POST /customers/{id}/identities` | ~55% |
| UC-003: Validación automática KYC | CustomerIdentityAPI `.../verify` + KYCScreeningAPI `/screenings` | ~55% |
| UC-004: Revisión manual de caso | **Ninguna API cubre esto** | 0% |
| UC-005: Notificación al cliente | **Ninguna API cubre esto** | 0% |

**Cobertura total: ~40–50%. Ninguna API individual cubre ≥70%.**

### Colisión detectada (sí)

Se detecta colisión parcial porque:
- Mismo capability name `CustomerOnboarding` en catálogo
- Mismo actor primario `CUSTOMER`
- UC-001, UC-002, UC-003 solapan con operaciones de APIs Published

**Sin embargo, la colisión es parcial (~50%)** y la intención de la nueva API es distinta: es un **orquestador de flujo end-to-end**, no un reemplazo de las APIs atómicas existentes.

---

## Acción propuesta

Crear `kyc-onboarding-api` como nuevo Business API Product bajo la capacidad `Customers/CustomerOnboarding`. Esta nueva API actúa como **orquestador del flujo de onboarding digital**, coordinando:

1. `CustomerProfileAPI` → creación/actualización del perfil de cliente
2. `CustomerIdentityAPI` → gestión y verificación de documentos de identidad
3. `KYCScreeningAPI` → screening AML/PEP
4. `ID_VERIFICATION_PROVIDER` → verificación de identidad contra proveedor externo
5. `NOTIFICATION_SERVICE` → emisión de eventos de cambio de estado al cliente

La nueva API NO reemplaza ninguna API existente; es **consumidora** de ellas.

---

## Propuesta técnica

**Nueva API:** `kyc-onboarding-api`  
**Layer:** Business API (coordina múltiples domain capabilities)  
**Base path:** `/api/kyc-onboarding/v1`  
**Endpoints principales (tentative — sujetos a Phase 3/4):**

```
POST   /onboarding-cases                          → Initiate onboarding (UC-001)
GET    /onboarding-cases/{caseId}                 → Get case status
POST   /onboarding-cases/{caseId}/documents       → Upload documents (UC-002)
POST   /onboarding-cases/{caseId}/validate        → Trigger auto-validation (UC-003)
GET    /onboarding-cases/{caseId}/validation-result
PATCH  /onboarding-cases/{caseId}/review-decision → Manual review decision (UC-004)
GET    /onboarding-cases                          → List cases (analyst view)
```

**Relación con APIs existentes:**
- Calls downstream: CustomerProfileAPI, CustomerIdentityAPI, KYCScreeningAPI
- Produces events: `OnboardingStatusChanged` → NOTIFICATION_SERVICE
- Calls external: AML_SERVICE, ID_VERIFICATION_PROVIDER

---

## Notas de gobernanza

- **Naming:** `kyc-onboarding-api` (kebab-case, alineado a `global-conventions.yaml`)
- **Versionado:** v1 (nueva API — no es extensión de versión existente)
- **Sin duplicidad:** Las APIs existentes (CustomerProfileAPI, CustomerIdentityAPI, KYCScreeningAPI) NO son modificadas ni reemplazadas; `kyc-onboarding-api` es un nuevo API Product en la misma capability `CustomerOnboarding`
- **Catálogo:** después de Phase 3, el agente deberá registrar `kyc-onboarding-api` en `catalog/domains/customers.yaml` bajo `CustomerOnboarding` (acción post-design)
- **BIAN alignment:** BIAN Service Domain candidato → `PartyLifecycleManagement` (KYC onboarding lifecycle) y `CustomerAgreement` — a confirmar en Phase 1
- **Backward compatibility:** no aplica (nueva API); las APIs existentes no son tocadas

---

## Gaps no cubiertos por catálogo (justifican CREATE)

- UC-004: Cola de revisión manual con workflow de analista KYC (state machine + decisión manual)
- UC-005: Emisión de eventos `OnboardingStatusChanged` (no existe en ninguna API del catálogo)
- Gestión de sesión/caso de onboarding end-to-end (estado: `INITIATED → DOCS_SUBMITTED → UNDER_REVIEW → APPROVED / REJECTED`)
- Orquestación cross-domain: CustomerProfileAPI + CustomerIdentityAPI + KYCScreeningAPI coordinados en un único flujo transaccional
- BR-004: Auto-escalación de validación fallida a revisión manual
- BR-005: Gate de acceso a productos condicionado al estado `APPROVED` del KYC
- BR-006/BR-007: Audit trail + PII cifrado scoped al ciclo de vida del onboarding
- Adaptadores a integraciones externas: AML_SERVICE y ID_VERIFICATION_PROVIDER

---

## Status

```yaml
phase0_status: COLLISION_DETECTED
collision_type: partial
collision_coverage: ~50%
recommendation: CREATE
user_decision: PENDING
```

> **Awaiting user decision: REUSE | EXTEND | CREATE_ANYWAY (confirmed CREATE)**
