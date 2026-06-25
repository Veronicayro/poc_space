# kyc-onboarding-api

**Layer:** Business  
**Type:** REST API (orchestrator)  
**Technology:** Java  
**BIAN:** PartyLifecycleManagement Release 14.0.0 (adapted)  
**Status:** Draft — Phase 6 (backend-component-design)

## Purpose

Business API orchestrator for the end-to-end digital KYC onboarding lifecycle. Owns the `OnboardingCase` state machine and coordinates downstream catalog APIs and external providers to register new bank customers with full regulatory compliance.

## Base path

```
/api/kyc-onboarding/v1
```

## Actors

| Actor | Channel | Scopes |
|---|---|---|
| CUSTOMER | Web, Mobile | `kyc.onboarding.initiate`, `kyc.onboarding.documents.write`, `kyc.onboarding.read` |
| KYC_ANALYST | Backoffice | `kyc.onboarding.read`, `kyc.onboarding.review.write` |
| SYSTEM | Internal | `kyc.onboarding.validate` (machine-to-machine) |

## Use cases supported

| UC | Name | BIAN behavior |
|---|---|---|
| UC-001 | Customer digital registration | Initiate |
| UC-002 | Document upload | Documentation/Execute |
| UC-003 | Automatic KYC validation | Execute + Qualification/Retrieve + IdentityProofing/Retrieve |
| UC-004 | Manual review | Control |
| UC-005 | Customer notification | Exchange → async event |

## OnboardingCase lifecycle

```
INITIATED → DOCS_SUBMITTED → UNDER_VALIDATION → APPROVED
                                              ↘ REVIEW_REQUIRED → APPROVED
                                                               ↘ REJECTED
```

## Downstream dependencies

| Component | Type | Operations used |
|---|---|---|
| CustomerProfileAPI v1.2.0 | Internal catalog API | POST /customers, PATCH /customers/{id} |
| CustomerIdentityAPI v1.1.0 | Internal catalog API | POST /identities, POST /verify |
| KYCScreeningAPI v3.0.0 | Internal catalog API | POST /screenings, GET /screenings/{id} |
| AML_SERVICE | External (adapter) | REST sync — circuit breaker applied |
| ID_VERIFICATION_PROVIDER | External (adapter) | REST sync — circuit breaker applied |
| NOTIFICATION_SERVICE | External async | Event consumer of `OnboardingStatusChanged` |

## Events published

| Event | Trigger |
|---|---|
| `OnboardingCaseInitiated` | Case created (INITIATED) |
| `OnboardingStatusChanged` | Any state transition |
| `OnboardingApproved` | State → APPROVED |
| `OnboardingRejected` | State → REJECTED |

## Key constraints

- **Security:** OAuth2/OIDC + RBAC; TLS 1.2+; PII encrypted at rest (AES-256)
- **Performance:** p95 < 2000ms; 500 req/s
- **Compliance:** ISO27001, GDPR (pseudonymization, erasure, data minimization)
- **Resiliency:** Circuit breaker on AML_SERVICE + ID_VERIFICATION_PROVIDER; 3 retries with exponential backoff

## Artifact map

```
design/business/kyc-onboarding-api/
├── component.yaml                  ← component design (this phase)
├── readme.md                       ← this file
├── integration/
│   └── integration-model.yaml      ← downstream integrations
├── models/
│   └── domain-model.yaml           ← entities and aggregates
├── data/
│   └── persistence-model.yaml      ← relational DB schema
├── events/
│   └── event-model.yaml            ← domain event schemas
├── state/
│   └── state-map.yaml              ← OnboardingCase state machine
└── contract/                       ← produced in Phase 7
    ├── openapi.yaml
    └── bian-adoption.yaml
```
