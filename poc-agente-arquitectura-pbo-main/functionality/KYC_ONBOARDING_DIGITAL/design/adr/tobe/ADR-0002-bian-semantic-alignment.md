---
decision_id: ADR-0002
title: "BIAN Adoption Level — Semantic Alignment with PartyLifecycleManagement"
architecture_view: tobe
layer: business
date: "2026-06-22"
status: accepted
affected_components: [kyc-onboarding-api]
---

## Context

The repository mandates BIAN Release 14 as the domain standard for Business and Domain API contracts. For `kyc-onboarding-api`, the team must decide:
1. **Which BIAN Service Domain** to align to.
2. **At what adoption level**: `direct_adoption` (paths/schemas replicated verbatim) vs. `semantic_alignment` (paths and schemas derived but adapted to AP conventions).

Available BIAN candidates evaluated in `design/bian/bian-service-domain-evaluation.yaml`:
- `PartyLifecycleManagement` — fit score 0.92
- `CustomerOffer` — fit score 0.45 (rejected: product-centric scope)
- `PartyReferenceDataDirectory` — fit score 0.35 (rejected: reference data concern)

## Decision

- **Selected Service Domain:** `PartyLifecycleManagement` Release 14.0.0
- **Adoption level:** `semantic_alignment`

BIAN path parameter naming convention (`{partylifecyclemanagementid}`, `{documentationid}`, `{qualificationid}`, `{identityproofingid}`) is **preserved verbatim** in the AP contract.

## Rationale

1. **Best-fit Service Domain:** PartyLifecycleManagement tracks party relationship state from initial establishment checks through lifecycle maintenance — exactly the scope of digital KYC onboarding. Its sub-behaviors (Documentation, Qualification, IdentityProofing, Control) map directly to UC-001 through UC-004 (confidence 0.92).
2. **Semantic alignment over direct adoption:** The BIAN baseline uses generic path structure (`/PartyLifecycleManagement/Initiate`) and flat `PartyRelationshipAdministrativePlan` request/response bodies. Direct adoption would force consumers to use non-intuitive BIAN paths for a digital onboarding API. Semantic alignment allows resource-oriented paths (`/onboarding-cases`) while preserving BIAN semantics in `operationId` naming, `x-bian-*` extensions, schema names, and field descriptions.
3. **Governance traceability:** Full traceability is maintained in `contract/bian-adoption.yaml`: all selected/omitted paths, field mappings, and adaptation rationale are documented per BLOCK-02 requirements.
4. **Omitted BIAN operations justified:** 9 of 15 BIAN paths are omitted. The Exchange behavior is replaced by async event publication (architectural decision ADR-0005); Update, Execute, Request, and Precedents operations are out of MVP scope — all documented with rationale.

## Alternatives considered

- **Direct adoption (paths verbatim):** Rejected. `/PartyLifecycleManagement/Initiate` would be a confusing path for a product that targets digital onboarding consumers. Additionally, the BIAN Exchange behavior (synchronous bilateral exchange) conflicts with the chosen async event model for notifications.
- **CustomerOffer alignment:** Rejected. CustomerOffer is product-lifecycle-centric (offer → sales product agreement) and does not cover AML screening, identity proofing, or manual review queue semantics. Fit score 0.45.
- **No BIAN alignment (custom contract):** Rejected. Repository governance mandates BIAN alignment for Business APIs. A custom contract would fail the BLOCK-03 gate.

## Implications

- The contract (`contract/openapi.yaml`) MUST preserve `x-bian-sd`, `x-bian-control-record`, `x-bian-release`, `x-bian-adoption-level`, `x-bian-operation`, and `x-bian-cr` extensions on all operations.
- BIAN path parameter names (`partylifecyclemanagementid`, etc.) are used as-is in all API paths, even though they are verbose. This is a deliberate governance decision.
- `contract/bian-adoption.yaml` MUST be maintained in sync with any future contract changes.
- The adoption matrix (`architecture/context/bian-contract-adoption-matrix.yaml`) MUST be updated if the contract version is incremented.
