# Gaps and Assumptions — KYC_ONBOARDING_DIGITAL

## Assumptions

- A-001: The `AML_SERVICE` external endpoint is available and returns a synchronous response within the 2s latency SLA.
- A-002: The `ID_VERIFICATION_PROVIDER` integrates via REST and is capable of processing identity documents in real time.
- A-003: The `NOTIFICATION_SERVICE` is event-driven; the onboarding orchestrator publishes domain events consumed by the notification service.
- A-004: A customer may only have one active onboarding case at a time.
- A-005: PII encryption at rest is the responsibility of the persistence layer; the API layer enforces TLS in transit.
- A-006: The KYC analyst backoffice channel is an internal-only interface; API security is enforced via RBAC with `kyc.analyst` role.
- A-007: Audit trail persistence (BR-006) is handled by the onboarding service itself; integration with an external audit trail service is out of scope for Phase 1.

## Gaps

- G-001: Document storage mechanism (file store vs. reference) is not specified; assumed to be external object storage with signed URL references stored in the onboarding case.
- G-002: Specific AML_SERVICE API contract is not provided; integration model will use an adapter pattern.
- G-003: Idempotency semantics for UC-001 (re-submission by same customer) need confirmation.
- G-004: SLA for manual review turnaround (UC-004) not specified; assumed async with no hard SLA.
- G-005: Multi-language support requirement not specified; assumed single-language (Spanish) for MVP.
