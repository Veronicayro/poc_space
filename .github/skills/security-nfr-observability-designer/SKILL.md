---
name: security-nfr-observability-designer
description: Designs cross-cutting security, non-functional requirements, and observability models for the target architecture package.
---

# Skill: Security, NFR, and Observability Designer

## Goal

Design cross-cutting security, non-functional requirements, and observability models.

## Inputs

- `design/context/context-pack.yaml`
- `design/component-inventory.yaml`
- `design/api-landscape.yaml`
- enterprise security and observability standards when available

## Outputs

Write:

```text
design/security-model.md
design/non-functional-requirements.yaml
design/observability-model.md
```

## Required coverage

Security:

- identity model
- authentication
- authorization
- trust boundaries
- secret handling
- sensitive data handling
- session security
- API security
- event security
- storage security
- audit requirements
- private networking

NFR:

- availability
- scalability
- latency
- throughput
- auditability
- resiliency
- deployment constraints
- data retention
- compliance constraints
- portability
- sovereignty or residency constraints when provided

Observability:

- logging
- tracing
- metrics
- correlation strategy
- alerting
- operational visibility
- business telemetry when relevant
