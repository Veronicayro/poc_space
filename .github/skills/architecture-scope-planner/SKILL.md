---
name: architecture-scope-planner
description: Infers execution mode, required views, required skills and gates after enterprise capability/domain standard alignment has been completed.
---

# Architecture Scope Planner Skill

## Purpose

Create `design/execution-plan.yaml` without requiring the user to provide all fields. The skill must infer the execution mode and required outputs from constraints, capability alignment, discovery and state.

## Inputs

- `functionality/<ID>/state.yaml`
- `design/context/context-pack.yaml`
- `design/enterprise-capability-map.yaml`
- `design/domain-standard-alignment.yaml`
- `design/bian/bian-service-domain-evaluation.yaml` when BIAN is provider
- `functionality/<ID>/supplemental-context/`
- optional user override: execution mode, provider target or target component

## Outputs

- `design/execution-plan.yaml`

## Execution mode inference

Do not ask the user to fill `execution_mode` unless the source material is contradictory.

Infer using these rules:

- Azure-only constraints -> `azure-only`.
- AWS-only constraints -> `aws-only`.
- GCP-only constraints -> `gcp-only`.
- Explicit provider comparison -> `provider-comparison`.
- Multi-runtime placement or portability requirement -> `multi-runtime`.
- On-prem dependency with managed runtime connectivity -> `hybrid`.
- On-prem-only runtime -> `on-premise`.
- No provider constraint -> `standard`.
- Very small scope -> `minimal`.
- Enterprise reference package requiring all views -> `full`.

## Required output fields

Conform to `architecture/schemas/execution-plan.schema.yaml`.

## Rules

- This skill runs after enterprise capability alignment.
- Do not design APIs, contracts or components. Deployment/runtime details are out of scope (cloud excluded).
- Identify required design views, required skills and blocking gates.
- Record rationale for inferred execution mode.
- If a user override conflicts with constraints, record the conflict as a blocking gap.
