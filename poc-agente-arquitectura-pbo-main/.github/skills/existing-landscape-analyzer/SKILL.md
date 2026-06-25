---
name: existing-landscape-analyzer
description: Determines whether existing components should be reused, modified, deprecated, or replaced before creating new components.
---

# Skill: Existing Landscape Analyzer

## Goal

Determine whether existing components should be reused, modified, deprecated, or replaced before creating new components.

## Inputs

- `design/context/context-pack.yaml`
- existing API catalog
- existing consumer interface inventory (if any)
- existing event catalog
- existing data/cache inventory

## Output

Write:

```text
design/existing-component-impact.yaml
```

## Output schema

```yaml
existing_component_assessments:
  - component_name: string
    component_type: api | service | event | database | cache | external
    current_owner: string
    semantic_fit: high | medium | low | unknown
    contract_fit: high | medium | low | unknown
    ownership_fit: high | medium | low | unknown
    data_fit: high | medium | low | unknown
    state_fit: high | medium | low | unknown
    operational_fit: high | medium | low | unknown
    decision: reuse | modify | create_new | deprecate | unresolved
    rationale: string
    required_changes: []
```

## Rules

- Do not create a new component when an existing component has high semantic, ownership, and contract fit.
- Record unresolved candidates for architectural review.

## General skill rules

See: `.github/copilot-instructions.md` (shared "general skill rules").
