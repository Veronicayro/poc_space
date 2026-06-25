---
decision_id: ADR-0005
title: "Notification Integration — Async Event Publisher as Internal Module (Outbox-backed)"
architecture_view: tobe
layer: events
date: "2026-06-22"
status: accepted
affected_components: [kyc-onboarding-api]
---

## Context

UC-005 requires notifying the customer of every onboarding state change via `NOTIFICATION_SERVICE`. The integration style is asynchronous (events), criticality is MEDIUM. The team must decide how to implement the notification trigger:

**Option A:** Implement event publication as an **internal module** within `kyc-onboarding-api` (same deployable, same transaction via outbox pattern).

**Option B:** Extract event publication to a **separate support API** (`kyc-onboarding-event-adapter`) that receives webhooks or polls from `kyc-onboarding-api`.

**Option C:** Implement a **BIAN Exchange** behavior endpoint that NOTIFICATION_SERVICE calls to receive state updates (synchronous, pull-based).

Additionally: the BIAN PartyLifecycleManagement baseline provides an `Exchange` behavior path for bidirectional status exchange. The team must decide whether to use it for notifications.

## Decision

**Option A selected:** Async event publication is implemented as an **internal module** within `kyc-onboarding-api`.

**BIAN Exchange behavior is NOT exposed** as a notification mechanism. The Exchange path is omitted from the AP contract (documented in `contract/bian-adoption.yaml#omitted_operations`).

Domain events (`OnboardingStatusChanged`, `OnboardingApproved`, `OnboardingRejected`) are written to the `outbox_events` table in the same DB transaction as state changes. A relay process publishes them to the event broker; NOTIFICATION_SERVICE subscribes.

## Rationale

**Internal module (Option A):**
1. **Tight coupling with state transitions:** Event emission is a direct consequence of state machine transitions — separating it into a different deployable introduces a choreography dependency that adds latency and failure modes without architectural benefit.
2. **Outbox pattern already available:** The persistence design (ADR-0003) establishes the `outbox_events` table. Event publication becomes a relay concern, not a separate service concern.
3. **Operational simplicity:** A single deployable unit is simpler to operate, monitor, and scale for the current scope. The event volume (at most 500 req/s per NFR) does not warrant a dedicated event adapter service.
4. **Future extraction path:** If event fan-out, multi-channel routing, or event transformation complexity grows, the internal module CAN be extracted to a dedicated support service without changing the `kyc-onboarding-api` contract.

**BIAN Exchange not used for notifications:**
1. BIAN Exchange is a synchronous bilateral exchange pattern — it requires NOTIFICATION_SERVICE to call back into `kyc-onboarding-api` for updates. This is the inverse of the desired push model.
2. Async pub/sub decouples the notification service from the onboarding service, preventing notification delivery failures from blocking the onboarding flow.
3. The GDPR principle of data minimization is better served by events (only status + caseId + timestamp) than by BIAN Exchange payloads (full CR record).

**Separate support API (Option B) rejected:**
- Adds an additional network hop (internal), an additional deployable, and a second contract to maintain — with no tangible benefit given the single consumer and low event volume.
- Would require `kyc-onboarding-api` to call the event adapter OR the adapter to poll for state changes — both patterns add complexity.

## Implications

- The `outbox_events` relay process MUST be implemented as part of the `kyc-onboarding-api` service (e.g., a scheduled thread or Spring `@Scheduled` job).
- Event schemas (`OnboardingStatusChanged`, `OnboardingApproved`, `OnboardingRejected`) MUST be defined in `events/event-model.yaml` and shared with NOTIFICATION_SERVICE before integration.
- Consumers MUST implement idempotent processing using `event_id` for deduplication (at-least-once delivery guarantee from outbox).
- If the number of event consumers exceeds 3 or event volume exceeds 5,000/day, evaluate Avro schema registry adoption (currently JSON per `events/event-model.yaml`).
- `NOTIFICATION_SERVICE` subscription contract (topic name, filter, schema version) MUST be confirmed with the Channels / Notifications Squad before go-live.
