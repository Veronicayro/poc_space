# Digital Personal Loan Origination — Architecture Overview

**Functionality ID:** LON-GHCopilot-Haiku45-Lending-v1  
**Phase:** 3 (Solution Landscape)  
**Status:** DRAFT  
**Date:** 2026-06-24

---

## Solution Vision

The Digital Personal Loan Origination solution delivers a seamless, automated end-to-end lending experience for customers across web and mobile channels. The system orchestrates loan request intake, real-time credit evaluation, personalized offer generation, digital contract acceptance, and funds disbursement through a BIAN-aligned microservice architecture.

The solution prioritizes speed-to-decision (< 5 minutes for auto-approved cases), regulatory compliance at every step, and customer transparency throughout the lifecycle. By integrating with external credit bureaus and internal scoring engines, the system enables both automated decisions and exception handling through human review workflows, ensuring balanced risk management and customer satisfaction.

The architecture separates customer-facing experience APIs from business orchestration and domain-specific services, allowing independent evolution of channels, business rules, and compliance requirements. Event-driven notifications keep customers informed and enable asynchronous processing of compliance tasks.

---

## Key Flows

### Flow 1: Happy Path — Automated Approval & Disbursement

**Actors:** CUSTOMER, SYSTEM  
**Use Cases:** UC-001 → UC-002 → UC-003 → UC-004 → UC-005 → UC-007 → UC-008  
**Business Rules:** BR-001, BR-002, BR-003, BR-006, BR-007, BR-009, BR-011, BR-012  

**Sequence:**
1. **Request Initiation (UC-001):** Customer submits loan request via mobile/web with amount, term, and employment data.
   - `LoanRequest-Experience-API` → `LoanOriginationOrchestrator-Business-API`
   - Orchestrator calls `PartyLifecycleMgmt-Domain-API` to validate KYC status (BR-001).

2. **Document Upload (UC-002):** Customer uploads supporting documents (payslips, ID, tax forms).
   - `LoanRequest-Experience-API` receives documents, stores in document storage.
   - Orchestrator publishes `LoanDocumentsUploaded` event (audit, BR-010).

3. **Automated Credit Evaluation (UC-003):** System queries credit bureau and runs scoring engine.
   - Orchestrator calls `Underwriting-Domain-API` with request details.
   - Underwriting queries external CREDIT_BUREAU and SCORING_ENGINE.
   - System returns preliminary decision + credit score (BR-003, BR-004).
   - If score ≥ threshold: APPROVED; else REFERRED (see Flow 2).

4. **Offer Generation (UC-004):** System generates personalized loan offer with rate/term/payment.
   - Orchestrator calls `CustomerOffer-Domain-API` with underwriting result.
   - Offer calculates rate based on score + risk profile (BR-006).
   - Offer is marked DRAFT, set to expire in 72 hours (BR-007).
   - `LoanOffer-Experience-API` presents offer to customer.

5. **Digital Acceptance (UC-005):** Customer reviews and accepts offer; system captures digital signature.
   - `LoanOffer-Experience-API` receives acceptance + signature via DIGITAL_SIGNATURE_PROVIDER.
   - `CustomerOffer-Domain-API` records acceptance, transitions offer to ACCEPTED state (BR-009).
   - Orchestrator publishes `OfferAccepted` event.

6. **Disbursement (UC-007):** System instructs core banking to credit funds to customer account.
   - Orchestrator calls `Disbursement-Domain-API` with loan amount and customer account.
   - Disbursement publishes `DisbursementInstruction` event (BR-011).
   - Core banking (EXT-003) confirms transfer asynchronously.

7. **Status Notification (UC-008):** Customer notified of milestone completions.
   - Orchestrator publishes state-change events.
   - Notification service (EXT-005) sends SMS/Email based on customer preferences.

**Happy Path Duration:** ~5 minutes (real-time evaluation to funding approval).

---

### Flow 2: Exception Path — Manual Referral & Review

**Actors:** CUSTOMER, CREDIT_ANALYST, SYSTEM  
**Use Cases:** UC-001 → UC-002 → UC-003 (REFERRED) → UC-006 → UC-004 → UC-005 → UC-007 → UC-008  
**Business Rules:** BR-002, BR-005, BR-008  

**Sequence:**
1. **Steps 1–3 same as happy path**, but credit evaluation returns REFERRED instead of APPROVED.
   - Score is in gray zone (e.g., 650–700, unclear employment).
   - System cannot auto-approve or auto-reject (BR-005).

2. **Manual Referral (UC-006):** Credit analyst reviews case in backoffice.
   - `LoanOriginationOrchestrator-Business-API` publishes `UnderwritingReferral` event.
   - Credit analyst accesses backoffice tools (NOT in this architecture scope).
   - Analyst makes decision: APPROVE or REJECT with justification (BR-010 audit).

3. **Approval/Rejection Callback:** System receives decision and updates orchestrator.
   - If APPROVED: continue to Flow 1 Step 4 (offer generation).
   - If REJECTED: orchestrator publishes `ApplicationRejected` event; customer notified (UC-008).

4. **Steps 4–8 as happy path** (if approved).

**Exception Path Duration:** 1–2 business days (depends on analyst workload).

---

## Bounded Contexts & Responsibility Allocation

The loan origination domain decomposes into 6 bounded contexts, each with clear ownership and responsibilities:

### 1. **Party & KYC Context**
- **Responsibility:** Maintain customer identity, KYC/AML compliance, party data.
- **Owned by:** Party & Compliance Squad.
- **Primary Component:** `PartyLifecycleMgmt-Domain-API` (BIAN PartyLifecycleManagement).
- **Key Flows:** KYC lookup (Flow 1 Step 1, Flow 2 Step 1).
- **External Dependency:** INT-001 (Identity & KYC system).
- **Boundary:** Read-only for loan origination; party data owned elsewhere.

### 2. **Loan Offer Context**
- **Responsibility:** Manage loan request lifecycle, offer generation, customer acceptance, contract recording.
- **Owned by:** Lending Product Squad.
- **Primary Component:** `CustomerOffer-Domain-API` (BIAN CustomerOffer).
- **Key Flows:** Request intake (Flow 1 Step 1–2), offer generation (Step 4), acceptance (Step 5).
- **External Dependencies:** EXT-004 (Digital Signature), EXT-006 (Document Storage), INT-002 (Audit).
- **Boundary:** Manages offer state machine (DRAFT → SUBMITTED → ACCEPTED → DISBURSED); coordinates with underwriting.

### 3. **Credit Evaluation & Underwriting Context**
- **Responsibility:** Perform automated and manual credit assessment; record decision with rationale.
- **Owned by:** Credit Risk & Underwriting Squad.
- **Primary Component:** `Underwriting-Domain-API` (BIAN Underwriting).
- **Key Flows:** Automated scoring (Flow 1 Step 3, Flow 2 Step 1), manual review (Flow 2 Step 2).
- **External Dependencies:** EXT-001 (Credit Bureau), EXT-002 (Scoring Engine), INT-002 (Audit).
- **Boundary:** Makes credit decisions; logs all evaluations; raises exceptions for gray zones.

### 4. **Disbursement Context**
- **Responsibility:** Execute fund transfers from bank to customer account; confirm completion.
- **Owned by:** Payments & Settlement Squad.
- **Primary Component:** `Disbursement-Domain-API` (BIAN Disbursement).
- **Key Flows:** Disbursement instruction (Flow 1 Step 6).
- **External Dependency:** EXT-003 (Core Banking system).
- **Boundary:** Delegates actual fund movement to core banking; orchestrates confirmation.
- **Reuse Opportunity:** DisbursementAPI v1.1 (Phase 4 decision).

### 5. **Loan Origination Orchestration Context**
- **Responsibility:** Coordinate multi-step workflow; manage state machine; publish events; integrate external services.
- **Owned by:** Platform Engineering / Loan Origination Squad.
- **Primary Component:** `LoanOriginationOrchestrator-Business-API` (proprietary).
- **Key Flows:** All flows (Flow 1, Flow 2) — orchestrator is the master coordinator.
- **Internal Dependencies:** All domain APIs, INT-002 (Audit), EXT-005 (Notifications).
- **Boundary:** Implements workflow state machine; does NOT own data (delegates to domain APIs); publishes domain events.

### 6. **Customer Experience & Channels Context**
- **Responsibility:** Present request intake, offer presentation, status updates to customers via web/mobile.
- **Owned by:** Digital Channels Squad.
- **Primary Components:**
  - `LoanRequest-Experience-API` (request + document upload)
  - `LoanOffer-Experience-API` (offer review + acceptance)
  - `LoanStatus-Experience-API` (status polling)
- **Key Flows:** All flows (customer touchpoints).
- **Internal Dependency:** `LoanOriginationOrchestrator-Business-API` (delegation).
- **Boundary:** Stateless BFFs; all business logic delegated to business/domain layers.

---

## Layer Architecture & API Allocation

```
┌────────────────────────────────────────────────────────────────────────┐
│ EXPERIENCE LAYER (BFF / Customer-Facing)                              │
│                                                                        │
│  • LoanRequest-Experience-API      → Intake & document upload        │
│  • LoanOffer-Experience-API        → Offer review & acceptance       │
│  • LoanStatus-Experience-API       → Status polling & transparency   │
└────────────────────────────────────────────────────────────────────────┘
                               ↓ delegates to
┌────────────────────────────────────────────────────────────────────────┐
│ BUSINESS LAYER (Orchestration & Process APIs)                         │
│                                                                        │
│  • LoanOriginationOrchestrator-Business-API → Master workflow engine  │
│    - Manages state machine (DRAFT → SUBMITTED → APPROVED → ACCEPTED) │
│    - Coordinates domain APIs, external services, events               │
│    - Implements business rules (BR-001 through BR-012)               │
└────────────────────────────────────────────────────────────────────────┘
                        ↓ calls (orchestrates)
┌────────────────────────────────────────────────────────────────────────┐
│ DOMAIN LAYER (BIAN-Aligned Service Domains)                           │
│                                                                        │
│  1. PartyLifecycleMgmt-Domain-API → KYC lookup (PartyLifecycle SD)   │
│  2. CustomerOffer-Domain-API      → Request & offer (CustomerOffer)  │
│  3. Underwriting-Domain-API       → Credit eval (Underwriting SD)    │
│  4. Disbursement-Domain-API       → Fund transfer (Disbursement SD)  │
└────────────────────────────────────────────────────────────────────────┘
                     ↓ integrates with external / internal
┌────────────────────────────────────────────────────────────────────────┐
│ SUPPORT LAYER (Cross-Cutting Concerns)                                │
│                                                                        │
│  • LoanAuditLog-Support-API → Async event publisher (compliance)     │
│  • INT-001 (Identity & KYC) → External system (mandatory)            │
│  • INT-002 (Audit & Compliance) → Event broker (compliance)          │
│  • EXT-001 (Credit Bureau) → External service call                   │
│  • EXT-002 (Scoring Engine) → External service call                  │
│  • EXT-003 (Core Banking) → External system (disbursement)           │
│  • EXT-004 (Digital Signature) → External service call               │
│  • EXT-005 (Notification Service) → Event consumer                   │
│  • EXT-006 (Document Storage) → External storage                     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Data & State Ownership

| Context | Owner | Persistent Data | State Machine | Events Published |
|---------|-------|-----------------|----------------|------------------|
| **Party/KYC** | INT-001 | Customer identity, KYC status | KYC lifecycle (external) | KYCApproved, KYCRejected |
| **Loan Offer** | CustomerOffer-Domain-API | Request, offer, contract | Draft → Submitted → Accepted → Disbursed | RequestCreated, OfferGenerated, OfferAccepted |
| **Underwriting** | Underwriting-Domain-API | Credit assessment, decision log | Assessment → Decision | AssessmentStarted, DecisionMade |
| **Disbursement** | Disbursement-Domain-API | Disbursement instruction, status | Instruction → Confirmed | DisbursementStarted, DisbursementConfirmed |
| **Orchestration** | LoanOriginationOrchestrator | Workflow state (read from domains) | Multi-step state machine | All domain events re-published |
| **Audit & Compliance** | INT-002 | Audit log, decision history | Immutable log | AuditEventLogged |

---

## Non-Functional Requirements & Cross-Cutting Concerns

### Performance
- Request-to-offer SLA: < 5 minutes (auto-approved cases).
- API latency: < 500ms p95 (including external calls).
- Database response time: < 100ms p99.

### Reliability & Availability
- Uptime SLA: 99.9% (3 nines) during business hours; 99.0% off-hours.
- Graceful degradation: If credit bureau unavailable, refer case for manual review (BR-005).
- Idempotency: All domain API calls must support retry + idempotent keys.

### Security & Compliance
- Data encryption at rest (all PII fields, BR-012).
- TLS 1.2+ in flight.
- Role-based access control (RBAC) for backoffice users.
- Audit trail for all decisions (BR-010, immutable logs).
- PCI-DSS compliance (if card data handled in future).

### Observability
- Structured logging (JSON) with trace IDs (correlation).
- Metrics: request latency, decision breakdown (approved/referred/rejected), error rates.
- Tracing: end-to-end request tracing via OpenTelemetry.
- Alerts: SLA breaches, error rate spikes, external system failures.

---

## Phase 3 → Phase 4 Handoff

This solution-level landscape document provides:
- ✓ Vision and key flows for Phase 4 API landscape design.
- ✓ Bounded contexts and responsibility allocation for Phase 6 component design.
- ✓ Draft component inventory (9 components) for Phase 6 sequencing.
- ✓ BIAN Service Domain alignment (4 domains) for Phase 7 contract derivation.

**Key Decision Pending in Phase 4:**
- CreditApplicationAPI v1.3 (catalog collision) → decision point: EXTEND or CREATE new Experience API.
- Resolution happens autonomously in `api-landscape-governance/SKILL.md`.

**Key Decision Pending in Phase 6:**
- DisbursementAPI v1.1 reuse vs. extension for Disbursement-Domain-API.

---

**Next Steps:** Phase 4 (api-landscape-design) will finalize API inventory, resolve catalog collisions, and produce the target API landscape for component design.
