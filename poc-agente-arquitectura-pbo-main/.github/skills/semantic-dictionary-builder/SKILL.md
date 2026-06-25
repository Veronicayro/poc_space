---
name: semantic-dictionary-builder
description: Creates the canonical enterprise semantic dictionary that uses terms that were based on and mapped from business requirements to business capabilities.
---

# Skill: Semantic Dictionary Builder

## Goal

Create the canonical enterprise semantic dictionary that uses terms that were based on and mapped from business requirements to business capabilities.

## Schema reference

Use `architecture/schemas/semantic-dictionary.schema.yaml`.

## Inputs

- `design/context/context-pack.yaml`
- `design/enterprise/enterprise-capability-map.yaml`
- `design/enterprise/domain-standard-alignment.yaml`
- BIAN evaluation output when available

## Output

Write: `design/enterprise/semantic-dictionary.yaml`

## Rules

- Use English canonical names for contracts.
- Preserve known business aliases.
- Do not introduce different names for the same concept across layers or technologies stacks or apis, microservices, or any other implementation artifacts.

## General skill rules

See: `.github/copilot-instructions.md` (shared "general skill rules").
