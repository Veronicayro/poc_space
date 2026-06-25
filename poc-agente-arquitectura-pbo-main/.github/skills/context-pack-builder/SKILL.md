---
name: context-pack-builder
description: Builds a compact, token-efficient context package for downstream skills.
---

# Skill: Context Pack Builder

## Goal

Build a compact, token-efficient context package for downstream skills.

## Schema reference

Use `architecture/schemas/context-pack.schema.yaml`.

## Inputs allowed

- `functionality/<ID>/discovery/use-cases.yaml`
- `functionality/<ID>/discovery/business-rules.yaml`
- `functionality/<ID>/discovery/nfrs.yaml`
- `functionality/<ID>/discovery/service-domain-candidates.yaml`
- `functionality/<ID>/supplemental-context/business.md`

## Inputs forbidden
- `functionality/<ID>/design/execution-plan.yaml`
- `functionality/<ID>/discovery/existing-apis-inventory.yaml`
- `design/api-landscape.yaml`
- `design/component-inventory.yaml`
- any contract artifact

## Outputs

Write:

```text
design/context/context-pack.yaml
```

## General skill rules

See: `.github/copilot-instructions.md` (shared "general skill rules").
