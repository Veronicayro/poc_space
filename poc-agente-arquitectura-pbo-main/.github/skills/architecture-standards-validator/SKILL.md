---
name: architecture-standards-validator
description: Validates backend target-architecture artifacts against governance rules such as naming, layering, BIAN, persistence, cache, event and diagram standards (frontend/cloud excluded).
---

# Architecture Standards Validator Skill

## Purpose

Validate that produced architecture artifacts conform to governance rules, not only that files exist.

## Inputs

- `architecture/context/architecture-governance.md`
- `architecture/context/bian-release14-governance.md`
- `architecture/schemas/`
- `functionality/<ID>/design/`

## Outputs

- validation findings included in `design/validation-report.yaml`

## Validation checks

- API names follow required naming conventions.
- Experience, Business, Domain and Support APIs comply with layer responsibilities.
- Business and Domain APIs have BIAN or domain-standard alignment before contracts.
- Business and Domain contracts include `bian-adoption.yaml` when BIAN is provider.
- Validate **early-stage** BIAN alignment decisions using `architecture/prompts/bian-alignment-decision-framework.md`:
  - Each relevant capability/component declares an Alignment Level: REQUIRED | ASSOCIATED | NONE
  - If REQUIRED/ASSOCIATED: there is a mapping to an official BIAN Service Domain (with a reference to the cached BIAN catalog)
  - If NONE: do not force BIAN mapping and do not generate unnecessary BIAN artifacts (token optimization)
- REST vs GraphQL decisions exist for Experience APIs.
- Persistence, cache, event and state artifacts exist when component flags require them.
- ADRs exist for significant decisions.
