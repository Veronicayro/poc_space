---
name: diagram-generator
description: Generates required Mermaid diagrams for the architecture package from the approved landscapes and component folders.
---

# Skill: Diagram Generator

## Goal

Generate required Mermaid diagrams for the architecture package.

## Inputs

- `design/component-inventory.yaml`
- `design/api-landscape.yaml`
- component folders

## Outputs

Write:

```text
design/sequence-general.mmd
design/flow-general.mmd
design/diagrams/context-target.mmd
design/diagrams/architecture-backend-tobe.mmd
```

Conditionally write:

```text
design/diagrams/architecture-backend-transition.mmd
```

Also ensure per-component sequence and flow diagrams exist when required.

## Rules

- Do not overload one architecture diagram with all concerns.
- Split by backend, transition, and supporting views (keep each diagram single-concern).
- General sequence diagrams stay interaction-level.
- Component sequence diagrams include internal orchestration and dependencies.
