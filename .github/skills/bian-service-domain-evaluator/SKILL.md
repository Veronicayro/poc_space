---
name: bian-service-domain-evaluator
description: Maps target Business and Domain APIs to BIAN Release 14 Service Domains using only the trusted BIAN source index.
---

# Skill: BIAN Service Domain Evaluator

## Goal

Map target Business and Domain APIs to BIAN Release 14 Service Domains using only `design/bian/bian-release14-source-index.yaml`.

## Output Schema reference

Use `architecture/schemas/bian-service-domain-evaluation.schema.yaml`.

## Inputs

- `design/context/context-pack.yaml`
- `design/bian/bian-release14-source-index.yaml`

## Output

Write: `design/bian/bian-service-domain-evaluation.yaml`


## Rules

- Do not use model memory.
- Do not select a Service Domain absent from the source index.
- Evaluate rejected candidates.
- Mark low-confidence mappings as unresolved.
- Do not generate API contracts.

## General skill rules

See: `.github/copilot-instructions.md` (shared "general skill rules").
