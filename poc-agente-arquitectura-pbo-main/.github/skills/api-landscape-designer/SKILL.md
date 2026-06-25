---
name: api-landscape-designer
description: Designs the target API landscape across Experience, Business, Domain, and Support layers.
---

# Skill: API Landscape Designer

## Goal

Design the target API landscape across Experience, Business, Domain, and Support layers.

## Schema reference

Use `architecture/schemas/api-landscape.schema.yaml`.

## Inputs

- `design/context/context-pack.yaml`
- `design/existing-component-impact.yaml`
- `design/semantic-dictionary.yaml`
- `design/bian/bian-service-domain-evaluation.yaml`

## Output

Write:

```text
design/api-landscape.yaml
```

## Output schema

```yaml
apis:
  - api_name: string
    api_type: experience | business | domain | support
    naming_rationale: string
    supported_flow_or_domain: string
    candidate_bian_service_domain: string
    bian_alignment_type: direct | adapted | partial | unresolved | n/a
    orchestration_role: orchestrating | non-orchestrating | n/a
    interaction_style: rest | graphql | asyncapi | mixed
    decision: reuse | modify | create | deprecate
    primary_consumers: []
    dependencies: []
    stateful_or_stateless: stateful | stateless
    related_contracts: []
    bian_baseline_reference: string
    notes: string
```

## Rules

- Do not generate full contracts.
- Experience APIs are journey-oriented.
- Business APIs may orchestrate and must be BIAN-aligned.
- Domain APIs must be non-orchestrating and BIAN-aligned.
- Support APIs isolate legacy or external integration.

## General skill rules

See: `.github/copilot-instructions.md` (shared "general skill rules").
