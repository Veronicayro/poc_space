---
decision_id: ADR-0003
title: "Persistence Technology — Relational Database with Transactional Outbox Pattern"
architecture_view: tobe
layer: data
date: "2026-06-22"
status: accepted
affected_components: [kyc-onboarding-api]
---

## Context

`kyc-onboarding-api` owns the `OnboardingCase` aggregate and must persist:
- Onboarding case state (state machine: 6 states, 6 transitions)
- KYC validation results (Qualification + IdentityProofing outcomes)
- Analyst review decisions (append-only)
- Audit log per business rule BR-006 (append-only, immutable, 7-year retention)
- Domain events pending publication (for reliable delivery to NOTIFICATION_SERVICE)

The team must select: (a) a storage engine, and (b) a pattern for reliable event publication that avoids the dual-write problem (persisting state + publishing event as two independent operations).

PII data (customer name, document number) requires encryption at rest (BR-007, GDPR, ISO27001).

## Decision

1. **Storage engine:** PostgreSQL-compatible relational database (e.g., PostgreSQL 16+, AWS Aurora PostgreSQL)
2. **Event publication pattern:** Transactional Outbox Pattern — domain events written to an `outbox_events` table in the **same DB transaction** as state changes; a relay process reads and publishes to the event broker asynchronously

## Rationale

**Relational database:**
1. **ACID transactions required:** Every state transition in the OnboardingCase state machine must atomically update `onboarding_cases.status`, insert a `kyc_results` row, insert an `audit_entries` row, and insert an `outbox_events` row — a multi-table transaction. NoSQL document databases do not provide cross-collection ACID guarantees by default.
2. **Column-level PII encryption:** PostgreSQL supports column-level encryption (e.g., `pgcrypto` AES-256) without requiring a separate encryption service, satisfying BR-007.
3. **Structured audit queries:** `audit_entries` (append-only, 7-year retention) requires range queries by `onboarding_case_id` and `occurred_at`. Relational indexes are optimal for these access patterns.
4. **Strong consistency:** OnboardingCase status transitions require serializable reads to prevent concurrent state mutation (e.g., two simultaneous analyst decisions on the same case). PostgreSQL row-level locking provides this.
5. **GDPR pseudonymization:** PostgreSQL supports in-place column nullification for GDPR erasure without deleting audit records.

**Transactional Outbox Pattern:**
1. **Dual-write elimination:** Without outbox, a state change committed to DB followed by a failed event publish creates an inconsistent state (case APPROVED but NOTIFICATION_SERVICE not notified). The outbox pattern makes event publication an eventual consequence of the DB transaction, eliminating dual-write risk.
2. **At-least-once delivery:** The relay process retries unpublished events from `outbox_events` until confirmed. Combined with consumer-side idempotency (deduplication by `event_id`), this achieves effective exactly-once processing.
3. **DB-native:** The outbox table lives in the same PostgreSQL instance — no additional infrastructure required.

## Alternatives considered

- **MongoDB / document store:** Rejected. Multi-document ACID transactions are supported in MongoDB 4.0+ but add complexity; the relational model (case → results → decisions → audit) is a natural fit for SQL joins and foreign key integrity.
- **Event sourcing:** Rejected. Event sourcing would require significant architectural complexity (event store, projections, eventual consistency on reads) that is not justified for a single-aggregate service at the current scale. Can be revisited if the audit trail requirement expands.
- **Outbox-less (fire-and-forget events):** Rejected. Notification delivery is MEDIUM criticality but GDPR-relevant (customers must be notified of outcome). A failed notification that is never retried would be a compliance gap.
- **Saga / choreography for state changes:** Rejected. The OnboardingCase owns all state internally; cross-service saga coordination would add latency and complexity without benefit.

## Implications

- The `outbox_events` table MUST be co-located in the same PostgreSQL database as `onboarding_cases`.
- A relay process (lightweight scheduler or CDC consumer) MUST be implemented to publish `outbox_events` to the event broker; `published_at` MUST be set on success.
- GDPR erasure procedure: set `customer_name_enc = NULL`, `document_number_enc = NULL` on the relevant `onboarding_cases` row; audit_entries are retained with `actor_id` only (pseudonymized).
- Maximum retry attempts and dead-letter behavior for `outbox_events` MUST be defined during implementation.
