---
decision_id: ADR-0004
title: "Resiliency for External Providers — Circuit Breaker with Differentiated Fallbacks"
architecture_view: tobe
layer: cross-cutting
date: "2026-06-22"
status: accepted
affected_components: [kyc-onboarding-api]
---

## Context

`kyc-onboarding-api` integrates with two HIGH-criticality external providers synchronously during UC-003 (Automatic KYC Validation):
- **AML_SERVICE** — mandatory per BR-003 ("AML validation is mandatory"). A failure MUST NOT silently skip the AML check.
- **ID_VERIFICATION_PROVIDER** — required for identity proofing. Unavailability should not permanently block customers if manual review can substitute.

Both integrations are synchronous REST calls with a 2s latency SLA (NFR). Both are external, meaning the bank has no SLA control over their availability. The onboarding flow must be resilient to transient failures without violating regulatory requirements.

## Decision

Apply a **circuit breaker** to both `AML_SERVICE` and `ID_VERIFICATION_PROVIDER` adapters with **differentiated fallback behaviors**:

| Provider | Circuit breaker | Fallback behavior |
|---|---|---|
| `AML_SERVICE` | Threshold: 5 failures / 30s; reset after 60s | **Hold** in `UNDER_VALIDATION`; page on-call; do NOT auto-escalate |
| `ID_VERIFICATION_PROVIDER` | Threshold: 5 failures / 30s; reset after 60s | **Auto-escalate** to `REVIEW_REQUIRED` (BR-004 applied) |

Both integrations use: retry policy (2 attempts, fixed 500ms backoff) → circuit breaker → fallback.

## Rationale

**Why circuit breaker:**
1. Cascading failure prevention: without a circuit breaker, a slow/unavailable external provider will exhaust the thread pool of `kyc-onboarding-api`, degrading all endpoints.
2. Fail-fast behavior: after the threshold, subsequent calls fail immediately rather than waiting for the 1500ms timeout, preserving system resources during an outage.

**Why differentiated fallbacks:**

*AML_SERVICE — Hold (not escalate):*
- BR-003 states AML validation is mandatory and cannot be skipped. Escalating to manual review without an AML result would allow a potentially non-compliant case to be approved by an analyst who lacks AML evidence. This creates a regulatory and legal risk.
- Holding the case in `UNDER_VALIDATION` preserves the regulatory gate. The case will retry when the circuit closes. Operations is notified to handle extended holds.

*ID_VERIFICATION_PROVIDER — Auto-escalate (BR-004):*
- Identity proofing is a compliance check, but the bank's KYC_ANALYST can substitute for automated proofing by manually reviewing identity documents. BR-004 explicitly accounts for this by routing failed automated validations to manual review.
- Auto-escalating preserves the customer journey without compromising compliance — the analyst reviews the identity documents directly.
- Permanently holding cases when IDV is unavailable would create a poor customer experience with no regulatory benefit.

## Alternatives considered

- **Retry only (no circuit breaker):** Rejected. Retries alone are insufficient for sustained outages; they increase load on an already failing external system.
- **Same fallback for both providers (always escalate):** Rejected. AML_SERVICE escalation without an AML result violates BR-003.
- **Async AML (fire-and-forget, process result later):** Rejected. The synchronous 2s SLA is a hard NFR requirement. Async AML would require a callback mechanism and significantly more complexity; deferred to a future iteration if SLA changes.
- **No fallback (let case fail with 503):** Rejected. Returning a 503 to the customer for a transient external failure is poor UX and would increase re-submission load on the system.

## Implications

- The circuit breaker MUST be implemented at the adapter level (`AmlServiceAdapter`, `IdVerificationAdapter`) — not at the API gateway level.
- The `aml_service_circuit_breaker_open` and `id_verification_circuit_breaker_open` metrics MUST be emitted and alerted on (see `design/non-functional-requirements.yaml#alerting`).
- Cases held in `UNDER_VALIDATION` due to AML circuit open require an operational runbook (out of scope for this ADR).
- The 30s failure threshold and 60s reset timeout are defaults; tune based on observed SLA data after go-live.
