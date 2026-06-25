---
name: backend-component-designer
description: Designs TO-BE backend components (experience/business/domain/support) and transitional components when required.
---

# Skill: Backend Component Designer

## Goal

Design TO BE backend components and transitional backend components when required.

## Inputs

- `design/context/context-pack.yaml`
- `design/api-landscape.yaml`
- `design/bian/bian-service-domain-evaluation.yaml`
- `design/existing-component-impact.yaml`

## Outputs

Write per-component artifacts only (the orchestrator phase catalog is the source of truth for allowed outputs):

```text
design/experience/<api-name>/component.yaml
design/business/<api-name>/component.yaml
design/domain/<api-name>/component.yaml
design/support/<api-name>/component.yaml
```

Each backend API component must include (at minimum, depending on layer and phase):

- `component.yaml`
- `readme.md`
- `integration/integration-model.yaml`
- `models/domain-model.yaml` (Business/Domain only; when required)

Diagrams (`sequence/sequence.mmd`, `flow/flow.mmd`) are produced in the backend diagram phase by the diagram/diagram-related skills.

## Rules

- TO BE backend architecture includes synchronous and asynchronous interactions together.
- Transitional backend architecture is generated only for coexistence, strangler, support API, or anti-corruption needs.
- Record reuse, modify, create, or deprecate decision per component.
