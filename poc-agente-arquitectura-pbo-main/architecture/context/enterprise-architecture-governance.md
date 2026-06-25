# Architecture Governance Rules

These are stable architecture rules. Skills must apply them. Validators must verify them where possible.

## 1. General architecture rules

- Design must remain implementation-agnostic at application and business logic level.
- Do not bind application architecture to .NET, Java, Spring, Quarkus, Node.js, Python, React, Angular, Lambda, Kubernetes or any specific runtime unless explicitly required as a constraint input.
- Frontend, backend and cloud must be designed together, but not necessarily in the same execution.
- Do not produce one overloaded architecture view. Split architecture into views by concern and provider.
- Every designed component must have purpose, ownership, bounded responsibility, dependencies, consumers, state ownership when applicable and non-functional requirements when applicable.
- Every relevant design decision must be explicit and traceable through ADRs.
- Similar business concepts must use the same semantic names across frontend, APIs, events, persistence, cache and state models.
- Existing components must be evaluated for reuse, modification or deprecation before new components are created.

## 2. Enterprise architecture and domain standard rules

- Business cases and functionality scope must be mapped to enterprise capabilities before solution architecture details.
- Domain standard alignment must be completed before Business or Domain APIs are finalized.
- Default domain standard provider is BIAN Release 14.
- The workflow must remain provider-decoupled so ACORD, TM Forum or another provider can be introduced later.

## 3. BIAN Release 14 rules

- Do not use model memory to identify BIAN Service Domains.
- Do not select a BIAN Service Domain unless the corresponding Release 14 YAML exists in the fetched or repository-provided source index.
- Business and Domain APIs must be aligned to relevant BIAN Service Domains selected from fetched BIAN Release 14 baseline files only.
- BIAN version is strictly Release 14 unless explicitly changed by governance.
- Adopt only required operations, entities and schemas.
- Do not import unnecessary BIAN operations.
- If exact fit is not possible, record alignment type, rationale, confidence, deviations, used BIAN files, rejected candidates and unresolved gaps.
- If no acceptable BIAN Service Domain exists, record `Unresolved BIAN Alignment` and block affected Business or Domain API design until reviewed.
