# Architecture Overview — Digital KYC Onboarding (KYC_ONBOARDING_DIGITAL)

**Version:** 0.1 (draft)  
**Phase:** solution-landscape  
**Date:** 2026-06-22  
**Technology:** Java  
**BIAN:** Release 14.0.0 — PartyLifecycleManagement (adapted)

---

## Solution Vision

`kyc-onboarding-api` is a **Business API orchestrator** that implements the end-to-end digital
KYC onboarding lifecycle for new bank customers. It owns the `OnboardingCase` state machine,
coordinates atomic catalog APIs and external providers, and emits domain events for downstream
notification. It does **not** replace existing Published APIs — it consumes them.

---

## Bounded Contexts

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     KYC ONBOARDING BOUNDED CONTEXT                          │
│  Owner: kyc-onboarding-api (Business layer)                                 │
│                                                                             │
│  Entities: OnboardingCase, KYCResult, IdentityDocument (ref)                │
│  State:    INITIATED → DOCS_SUBMITTED → UNDER_VALIDATION                    │
│                     → APPROVED | REVIEW_REQUIRED → APPROVED | REJECTED      │
└─────────────────────────────────────────────────────────────────────────────┘
         │ delegates to (sync REST)                │ publishes events
         ▼                                         ▼
┌──────────────────────────┐          ┌────────────────────────────────┐
│  CATALOG DOMAIN APIs     │          │  NOTIFICATION_SERVICE (async)  │
│  (existing, Published)   │          │  Event: OnboardingStatusChanged │
│  • CustomerProfileAPI    │          └────────────────────────────────┘
│  • CustomerIdentityAPI   │
│  • KYCScreeningAPI       │
└──────────────────────────┘
         │ calls external (sync REST)
         ▼
┌──────────────────────────┐
│  EXTERNAL PROVIDERS      │
│  • AML_SERVICE (HIGH)    │
│  • ID_VERIFICATION (HIGH)│
└──────────────────────────┘
```

---

## Key Flows

### Flow 1 — Happy Path (auto-approved)

```
CUSTOMER                kyc-onboarding-api          Downstream APIs / Ext.
   │                           │                            │
   │── POST /onboarding ──────►│ [UC-001]                   │
   │                           │── POST /customers ────────►│ CustomerProfileAPI
   │                           │◄─ customerId ──────────────│
   │                           │  create OnboardingCase     │
   │◄─ caseId (INITIATED) ─────│                            │
   │                           │                            │
   │── POST /documents ────────│ [UC-002]                   │
   │                           │── POST /identities ───────►│ CustomerIdentityAPI
   │                           │◄─ documentId ─────────────│
   │                           │  state → DOCS_SUBMITTED    │
   │◄─ 202 Accepted ───────────│                            │
   │                           │                            │
   │                           │── POST /verify ───────────►│ CustomerIdentityAPI
   │                           │── POST /screenings ───────►│ KYCScreeningAPI
   │                           │── POST /id-verify ────────►│ ID_VERIFICATION_PROVIDER
   │                           │   [UC-003] state → UNDER_VALIDATION
   │                           │◄─ all PASS ────────────────│
   │                           │  state → APPROVED          │
   │                           │── emit OnboardingApproved ►│ NOTIFICATION_SERVICE
   │◄─ notify: APPROVED ───────────────────────────────────►│
```

### Flow 2 — Manual Review Path

```
   │  (same UC-001 + UC-002 steps)
   │                           │
   │                           │ [UC-003] one check FAILS
   │                           │  state → REVIEW_REQUIRED
   │                           │── emit OnboardingStatusChanged ► NOTIFICATION_SERVICE
   │◄─ notify: UNDER_REVIEW ───│                            │
   │                           │                            │
KYC_ANALYST                    │                            │
   │── PATCH /review ──────────│ [UC-004]                   │
   │                           │  record ReviewDecision     │
   │                           │  state → APPROVED/REJECTED │
   │                           │── emit OnboardingStatusChanged ► NOTIFICATION_SERVICE
   │◄─ notify: final result ───│                            │
```

---

## Component Responsibilities

### `kyc-onboarding-api` (Business layer — CREATE)

**Owns:**
- `OnboardingCase` lifecycle (state machine)
- `KYCResult` aggregation (consolidates results from KYCScreeningAPI + ID_VERIFICATION_PROVIDER)
- `ReviewDecision` recording (analyst manual decisions)

**Delegates (does not own):**
- Customer profile persistence → `CustomerProfileAPI`
- Document storage and identity verification → `CustomerIdentityAPI`
- AML/PEP screening → `KYCScreeningAPI`
- Raw AML checks → `AML_SERVICE` (via internal adapter)
- Raw identity proofing → `ID_VERIFICATION_PROVIDER` (via internal adapter)
- Customer notifications → `NOTIFICATION_SERVICE` (via internal event publisher)

**Does NOT:**
- Manage customer master data (CustomerProfileAPI owns this)
- Store identity documents (CustomerIdentityAPI owns this)
- Execute AML logic (delegated to KYCScreeningAPI + AML_SERVICE)
- Grant product access (downstream systems consume `OnboardingApproved` event)
- Perform credit scoring (out of scope)

---

## Decision: Event Adapter as Internal Module

`kyc-onboarding-event-adapter` is implemented as an **internal module** of `kyc-onboarding-api`,
not as a separate deployable component. Rationale: the event publication is tightly coupled to
state transitions in the onboarding case lifecycle; a separate service would add operational
overhead without architectural benefit at this scale. If notification volume warrants fan-out
or multi-channel routing in the future, extraction to a support service can be done without
breaking the onboarding API contract.

---

## Persistence Model (high-level)

| Entity | Owner | Storage |
|---|---|---|
| OnboardingCase | kyc-onboarding-api | Relational (PostgreSQL-compatible) |
| KYCResult | kyc-onboarding-api | Relational (embedded in case) |
| IdentityDocument (ref) | CustomerIdentityAPI | Reference only; URL stored in case |
| AuditEntry | kyc-onboarding-api | Append-only audit log table |

---

## NFR Summary

| Concern | Requirement |
|---|---|
| AuthN | OAuth2/OIDC |
| AuthZ | RBAC (`kyc.customer`, `kyc.analyst`) |
| Encryption in transit | TLS 1.2+ |
| Encryption at rest | PII fields encrypted at persistence layer |
| Latency | < 2s (synchronous validation paths) |
| Concurrency | 500 req/s |
| Observability | Structured logging, distributed tracing (W3C), real-time metrics |
| Compliance | ISO27001, GDPR |

---

## Layer Allocation

| Layer | Component | Status |
|---|---|---|
| Business | `kyc-onboarding-api` | CREATE |
| Support (internal) | Event publisher module (within kyc-onboarding-api) | CREATE (internal) |
| External | CustomerProfileAPI, CustomerIdentityAPI, KYCScreeningAPI | REUSE (downstream) |
| External | AML_SERVICE, ID_VERIFICATION_PROVIDER | REUSE (adapter) |
| External async | NOTIFICATION_SERVICE | REUSE (event consumer) |

---

*Maturity: draft — API names and contract details to be finalized in Phase 4 (api-landscape-design).*
