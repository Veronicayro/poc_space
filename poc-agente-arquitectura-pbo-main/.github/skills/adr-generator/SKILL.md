# Skill: ADR Generator

## Goal

Generate Architecture Decision Records for major decisions made during target architecture design.

## Schema reference

Use `architecture/schemas/adr.schema.yaml`.

## Inputs

- `design/architecture-overview.md`
- `design/api-landscape.yaml`
- `design/bian/bian-service-domain-evaluation.yaml`
- `design/security-model.md`

## Outputs

Write ADRs under:

```text
design/adr/tobe/
design/adr/transition/    # only when transition exists
```

## ADR schema

```markdown
# ADR-XXXX: <title>

- decision_id: ADR-XXXX
- architecture_view: tobe | transition
- layer: experience | business | domain | support | data | cache | events | cross-cutting
- status: proposed | accepted | superseded

## Context

## Decision

## Rationale

## Alternatives considered

## Implications

## Affected components
```

## Rules

- Generate ADRs for non-obvious or architecturally significant decisions only.
- Do not generate decorative ADRs.
- Every ADR must reference affected components.
