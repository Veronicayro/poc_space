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

## 2. BIAN Release 14 rules

- Do not use model memory to identify BIAN Service Domains.
- Do not select a BIAN Service Domain unless the corresponding Release 14 YAML exists in the fetched or repository-provided source index.
- Business and Domain APIs must be aligned to relevant BIAN Service Domains selected from fetched BIAN Release 14 baseline files only.
- BIAN version is strictly Release 14 unless explicitly changed by governance.
- Business APIs are Service Domain-aligned APIs that orchestrate.
- Domain APIs are Service Domain-aligned APIs that do not orchestrate.
- Business and Domain API contracts must use fetched BIAN Release 14 semantic APIs as the mandatory baseline for synchronous contracts when relevant.
- Business and Domain API contracts must use fetched BIAN Release 14 AsyncAPI as the mandatory baseline for asynchronous contracts when relevant.
- Adopt only required operations, entities and schemas.
- Do not import unnecessary BIAN operations.
- All Business and Domain API contracts must be in English.
- If exact fit is not possible, record alignment type, rationale, confidence, deviations, used BIAN files, rejected candidates and unresolved gaps.
- If no acceptable BIAN Service Domain exists, record `Unresolved BIAN Alignment` and block affected Business or Domain API design until reviewed.

## 3. API naming and responsibility rules

Naming conventions:

- Experience API: `api-experience-<supported-flow>`
- Business API: `api-business-<bian-service-domain>`
- Domain API: `api-domain-<bian-service-domain>`
- Support API: `api-support-<system-or-capability>`
- Microfrontend: `mfe-<supported-flow>`
- Use kebab-case for generated names.

Layer responsibilities:

- Experience APIs support channel or flow-specific journeys, shape frontend requests/responses and coordinate UX composition. They must not absorb core domain logic.
- Business APIs orchestrate reusable business capabilities, cross-domain process logic, business policies and workflow coordination. They must be BIAN-aligned when BIAN is the selected provider.
- Domain APIs encapsulate stable domain semantics and business capabilities without orchestration. They must be BIAN-aligned when BIAN is the selected provider.
- Support APIs isolate legacy integrations, external systems, protocol adaptation and anti-corruption concerns.

## 4. Experience API style rules

- Experience APIs may be REST or GraphQL.
- Prefer REST when interaction is operation-centric, resource boundaries are stable, caching is important or standard API management is primary.
- Consider GraphQL when UI needs dynamic field projection, multiple views need different shapes of the same data, over-fetching/under-fetching is material, or the journey is composition-heavy.
- Both REST and GraphQL may be used only with explicit justification.
- Experience APIs must preserve semantic field naming aligned to the semantic dictionary and BIAN BOM concepts where applicable.

## 5. Contract rules

- If a component is an API, a contract is mandatory.
- Experience REST APIs use OpenAPI.
- Experience GraphQL APIs use GraphQL schema artifacts.
- Business and Domain APIs must have `contract/openapi.yaml` and `contract/bian-adoption.yaml`.
- Business and Domain APIs must have `contract/asyncapi.yaml` when exposing asynchronous interactions.
- Business and Domain target operations must be traceable to selected BIAN baseline operations unless explicitly documented as adaptation.
- If a BIAN field is renamed, document the mapping in `semantic-dictionary.yaml` and `contract/bian-adoption.yaml`.

## 6. Mandatory artifact completeness rules

- Contracts are mandatory for every designed API.
- Sequence diagrams are mandatory for every designed API, every frontend component, every MFE-to-Experience API interaction and the end-to-end general flow.
- Flow diagrams are mandatory for the end-to-end general flow, every Experience API, every Business API, every frontend component and any Domain/Support API with non-trivial branching.
- Persistence models are mandatory for components that own or read/write persistent state.
- Event models are mandatory for components that publish or consume events.
- Cache models are mandatory for components that use cache.
- State maps are mandatory for components with stateful orchestration, deferred processing or lifecycle progression.
- If a component does not require persistence, cache, events or state, its `readme.md` must explicitly say so.
- A design stage is incomplete if any mandatory artifact is missing.
