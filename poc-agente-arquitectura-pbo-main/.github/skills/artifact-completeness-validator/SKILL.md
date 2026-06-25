---
name: artifact-completeness-validator
description: Validates file completeness, schema conformance, phase gates, BIAN traceability and governance rule compliance for the target architecture package.
---

# Artifact Completeness Validator Skill

## Purpose

Validate that the design package is complete, consistent and traceable.

## Inputs

- `functionality/<ID>/state.yaml`
- `functionality/<ID>/design/`
- `architecture/schemas/`
- `architecture/context/architecture-governance.md`
- `architecture/context/bian-release14-governance.md`

## Output

- `design/validation-report.yaml`

## Required validations

- Enterprise capability alignment exists before solution/API/component design.
- Domain standard alignment exists.
- BIAN source index exists when BIAN is the provider.
- Business and Domain API BIAN alignment is traceable to Release 14 baseline files.
- Business and Domain contracts have `contract/bian-adoption.yaml`.
- Every API has a contract.
- Every API has sequence and flow diagrams according to rules.
- Naming conventions are satisfied.
- ADR structure is satisfied.
- `state.yaml` accurately reflects phase and artifact status.

## Rule

Do not silently generate missing artifacts in validation-only mode. Report issues and required actions.
