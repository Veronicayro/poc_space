---
decision_id: ADR-0001
title: "API Layer Selection — Business Layer for kyc-onboarding-api"
architecture_view: tobe
layer: business
date: "2026-06-22"
status: accepted
affected_components: [kyc-onboarding-api]
---

## Context

The Digital KYC Onboarding functionality requires a new API to serve two distinct actors:
- **CUSTOMER** (via Web/Mobile channels) who initiates onboarding and uploads documents
- **KYC_ANALYST** (via Backoffice) who reviews failed cases and submits decisions

The team must decide whether to expose the onboarding capability as an **Experience API** (channel-optimized, presentation-focused) or as a **Business API** (capability-owning, orchestrating, channel-agnostic).

The execution plan (`design/execution-plan.yaml`) identifies the required layers as: `business`, `support`, `data`, `events`. No Experience API layer was identified as required.

## Decision

`kyc-onboarding-api` is placed in the **Business layer**.

## Rationale

1. **Capability ownership:** The API owns the `OnboardingCase` aggregate and its full state machine — this is business domain logic, not a presentation concern.
2. **Multiple actors, same contract:** Both CUSTOMER (web/mobile) and KYC_ANALYST (backoffice) consume the same API with scope-differentiated authorization (`kyc.onboarding.initiate` vs. `kyc.onboarding.review.write`). An Experience API would only add an indirection layer with no presentation value for a single-resource API.
3. **Orchestration:** The API coordinates across three catalog domain APIs (CustomerProfileAPI, CustomerIdentityAPI, KYCScreeningAPI) and two external providers — an orchestration concern that belongs to the Business layer per API governance guidelines.
4. **BIAN alignment:** BIAN PartyLifecycleManagement is a Business-layer Service Domain focused on lifecycle management, not presentation.
5. **Simplicity:** Adding an Experience API would require an additional component, additional contract, and additional hop with no tangible benefit for the current scope.

## Alternatives considered

- **Experience API + Business API split:** Rejected. The onboarding contract is not channel-specific; both actors access the same resources with the same semantics. The split would create a thin passthrough Experience API with no business value.
- **Domain API:** Rejected. `kyc-onboarding-api` orchestrates multiple domains — it cannot be scoped to a single domain.
- **Support API:** Rejected. The API is a primary capability, not a utility/infrastructure concern.

## Implications

- Channel teams (Web, Mobile) MUST consume `kyc-onboarding-api` directly (no intermediate Experience API).
- If channel-specific optimizations are needed in the future (e.g., mobile-specific payload reduction, BFF pattern), an Experience API SHOULD be added as a separate Phase 4 deliverable without modifying this contract.
- Authorization is enforced via RBAC scopes at the Business API level; the API gateway MUST validate scopes before forwarding requests.
