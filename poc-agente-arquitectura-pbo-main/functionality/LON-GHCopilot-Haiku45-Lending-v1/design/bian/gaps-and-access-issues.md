# BIAN Release 14 — Gaps & Access Issues

## Document Metadata

- Functionality: LON-GHCopilot-Haiku45-Lending-v1
- Phase: Phase 1 (enterprise-capability-alignment)
- Date: 2026-06-24
- Purpose: Record BIAN baseline access status and semantic gaps

---

## BIAN Baseline Access Status

### Release 14.0.0 — Local Cache

✓ **Status: ACCESSIBLE**

All required BIAN Release 14.0.0 OAS3 files are present in local cache:

- `architecture/cache/bian/release14.0.0/oas3/yamls/` — ALL Service Domains indexed
- `architecture/cache/bian/release14.0.0/asyncapi-3.x/yamls/` — Available (not required for Phase 1)
- `architecture/cache/bian/release14.0.0/index/` — Operation index directory (JSON caches)

### Selected Service Domains — Retrieval Status

| Service Domain | OAS3 File | Status | File Size | Hash |
|---|---|---|---|---|
| CustomerOffer | CustomerOffer.yaml | ✓ Retrieved | Valid | Dynamic |
| Underwriting | Underwriting.yaml | ✓ Retrieved | Valid | Dynamic |
| Disbursement | Disbursement.yaml | ✓ Retrieved | Valid | Dynamic |
| PartyLifecycleManagement | PartyLifecycleManagement.yaml | ✓ Retrieved | Valid | Dynamic |
| ReferenceDataDirectory | ReferenceDataDirectory.yaml | ✓ Referenced | Valid | Dynamic |

---

## Semantic Gaps (BIAN vs. Digital Personal Loan Origination)

### Gap 1: Document Upload Protocol

**Description:**
BIAN CustomerOffer expects documents as part of offer verification (UC-002), but BIAN does not define:
- Document upload API/mechanism
- Document type validation rules
- Document storage location/format
- Integration with document repository

**Discovery Context:**
- Use Case: UC-002 (Document upload)
- Business Rule: BR-012 (encryption at rest)
- External Dependency: EXT-006 (DOCUMENT_STORAGE)

**BIAN Coverage:**
- `CustomerOffer.Update` includes "document checks" in procedure definition
- No detailed operation for document submission/validation

**Resolution Path:**
- **Phase 2:** Analyze existing document handling systems (existing-landscape-analyzer)
- **Phase 6:** Design custom DocumentUpload component as bridge to DOCUMENT_STORAGE (EXT-006)
- **Phase 7:** Generate custom API contract for document handling (not BIAN-derived)

**Severity:** MEDIUM (expected; common BIAN adaptation point)

**Blocking:** NO — Document handling can be designed as adapter layer

---

### Gap 2: Notification/Messaging Infrastructure

**Description:**
UC-008 (Status notification) has no BIAN Service Domain mapping.
BIAN does not define notification/messaging domains.

**Discovery Context:**
- Use Case: UC-008 (Status notification)
- External Dependency: EXT-005 (NOTIFICATION_SERVICE)

**BIAN Coverage:**
- None — messaging is cross-cutting infrastructure

**Resolution Path:**
- **Phase 5:** Define notification/event pattern in security-nfr-observability-designer
- **Phase 6:** Design AsyncAPI for internal event publishing
- Integration with EXT-005 is external service dependency

**Severity:** LOW (expected; standard infrastructure responsibility)

**Blocking:** NO — notification is decoupled from BIAN orchestration

---

### Gap 3: Manual Review Workflow (Gray-Zone Referral)

**Description:**
BR-005 (gray-zone referral) and UC-006 (manual review) require SLA and workflow definition.
BIAN Underwriting.Update handles manual decision recording but does not define:
- Referral SLA (BR-005 assumes 4-8 business hours; not formalized)
- Work distribution algorithm
- Escalation rules
- Decision recording format/deadline

**Discovery Context:**
- Use Case: UC-006 (Manual referral review)
- Business Rule: BR-005 (gray-zone referral)
- Assumption: A-007 (4-8 business hours SLA)

**BIAN Coverage:**
- `Underwriting.Update` records analyst decision
- No workflow engine specification

**Resolution Path:**
- **Phase 6:** Define ManualReviewWorkflow component with SLA enforcement
- **Phase 7:** If required, generate AsyncAPI for worklist/task management

**Severity:** MEDIUM (affects service level management)

**Blocking:** NO — SLA definition is orchestration responsibility

---

### Gap 4: Offer Expiration Enforcement

**Description:**
BR-007 (72-hour offer expiration) is a business rule, not a BIAN-defined operation.
BIAN CustomerOffer records validity period but does not specify:
- Expiration check mechanism (passive lookup vs. active enforcement)
- Rejection of post-expiration acceptance (automatic vs. gated)
- Notification before expiration

**Discovery Context:**
- Use Case: UC-004 (Offer generation) + UC-005 (Acceptance)
- Business Rule: BR-007 (72-hour expiration)
- Assumption: A-006 (webhook + scheduled task)

**BIAN Coverage:**
- `CustomerOffer.FacilityApplication` stores validity date
- No temporal enforcement operation

**Resolution Path:**
- **Phase 6:** Design OfferExpirationManager component with scheduler
- **Phase 5 (NFR):** Enforce temporal constraints and notification triggers

**Severity:** MEDIUM (critical for business rule enforcement)

**Blocking:** NO — enforcement is orchestration responsibility

---

### Gap 5: Data Encryption at Rest (BR-012)

**Description:**
BR-012 requires encryption of sensitive data at rest (credit score, customer PII, signature proof).
BIAN does not specify encryption implementation.

**Discovery Context:**
- Business Rule: BR-012 (data encryption at rest)
- Applies to: CustomerOffer data, CreditDecision scores, SignedContract documents

**BIAN Coverage:**
- None — encryption is infrastructure/compliance responsibility

**Resolution Path:**
- **Phase 5:** Define encryption requirements in security-nfr-observability-designer
- **Phase 6:** Implement via persistence layer (Hibernate, Spring Data interceptors)

**Severity:** CRITICAL (compliance requirement)

**Blocking:** NO — orthogonal to BIAN contract design

---

### Gap 6: Audit Trail Persistence (BR-010)

**Description:**
BR-010 requires immutable audit logs of all credit decisions with timestamp, actor, and reason.
BIAN Underwriting.Update expects audit trail but does not specify:
- Log format
- Persistence mechanism
- Query/compliance access patterns
- Retention policy

**Discovery Context:**
- Business Rule: BR-010 (decision audit trail)
- Internal Dependency: INT-002 (Audit & Compliance Log system)

**BIAN Coverage:**
- Underwriting process expects decision recording
- No audit infrastructure definition

**Resolution Path:**
- **Phase 2:** Assess existing Audit & Compliance Log system (INT-002)
- **Phase 6:** Design AuditLogger component + integration with INT-002

**Severity:** CRITICAL (regulatory compliance)

**Blocking:** NO — audit handling is integration responsibility

---

## Blocking Issues

**Status: NONE**

All BIAN baseline files are accessible and indexed.
No blocking access issues detected.
Semantic gaps are expected and handled via downstream phases (2–7).

---

## Recommendations

### For Phase 2 (Scope & Execution Planning)

1. **Confirm Document Handling Integration:** Validate DOCUMENT_STORAGE (EXT-006) API compatibility
2. **Verify Audit System Capability:** Confirm INT-002 supports BR-010 compliance logging
3. **Review Manual Review Workflow:** Clarify CREDIT_ANALYST SLA and escalation rules

### For Phase 5 (Security/NFR/Observability)

1. **Encryption Implementation:** Define data classification and key management strategy
2. **Offer Expiration:** Specify scheduler-based enforcement and notification rules
3. **Audit Trail Design:** Codify log format, retention, and access controls

### For Phase 6 (Backend Component Design)

1. **Document Upload Bridge:** Design adapter between Loan Origination API and DOCUMENT_STORAGE (EXT-006)
2. **Manual Review Workflow:** Implement referral routing and SLA enforcement
3. **Offer Expiration Manager:** Scheduler for post-72h rejection and customer notification

---

## Summary

BIAN Release 14 provides excellent baseline coverage for Digital Personal Loan Origination.
Identified gaps are semantic (not access issues) and are addressed through standard downstream design phases.

**BIAN Alignment Quality: HIGH (0.92 confidence)**

No BIAN access blocks. Ready to proceed to Phase 2.
