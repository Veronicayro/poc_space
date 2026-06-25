---
name: enterprise-capability-mapper
description: Maps business cases and functionality scope to enterprise capabilities and the configured domain standard provider before solution architecture design.
---

# Enterprise Capability Mapper Skill

## Purpose


To align enterprise architecture to an industry or enterprise domain standard before solution architecture is produced.

Default provider: BIAN Release 14.


## Inputs

- `design/context/context-pack.yaml`
- `design/bian/bian-release14-source-index.yaml` when provider is BIAN

## Required alignment flow

1. Identify business cases and functionality scope.
2. Map business cases to enterprise capabilities.
3. Select domain standard provider, defaulting to BIAN Release 14.
4. Build or read provider baseline index from architecture/cache/bian/release14.0.0/oas/yamls by Service Domain name.
5. Map enterprise capabilities to provider domains/capabilities.
6. Record evidence, rationale, confidence and gaps.
7. Only then proceed to API, backend, frontend and cloud architecture.

## Outputs

- `design/enterprise/enterprise-capability-map.yaml`
- `design/enterprise/domain-standard-alignment.yaml`
- (BIAN) **No** genera ni actualiza `design/bian/bian-service-domain-evaluation.yaml`; ese artefacto es responsabilidad de `bian-service-domain-evaluator` y se consume como input.

## Output Schema reference

- `architecture/schemas/enterprise-capability-map.schema.yaml`
- `architecture/schemas/domain-standard-alignment.schema.yaml`

## Rules

- Identify business cases, business outcomes, actors and enterprise capabilities.
- Map capabilities to provider domains or Service Domains.
- For BIAN, **use as input** `design/bian/bian-service-domain-evaluation.yaml` (if exists) to limit the selection to Service Domains with evidence; if it does not exist, treat Service Domains as *candidates only* and reflect this in `design/bian/domain-standard-alignment.yaml`.
- For BIAN, only select Service Domains present in `bian-release14-source-index.yaml`.
- Record rejected candidates, rationale and confidence.
- Record unresolved capabilities and blocking gaps.
- Do not design APIs or contracts in this skill.

## Output quality

Every selected domain standard mapping must include:

- capability id
- provider name and version
- selected domain or service domain
- source reference
- alignment type
- confidence
- rationale
- rejected candidates
- unresolved gaps
