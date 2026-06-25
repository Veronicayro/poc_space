---
name: experience-contract-designer
description: Generates REST OpenAPI or GraphQL schema contracts for Experience APIs using the semantic dictionary and API style evaluation.
---

# Experience Contract Designer Skill

## Purpose

Generate Experience API contracts after Experience API style has been evaluated.

## Inputs

- `design/api-landscape.yaml`
- `design/experience-api-style-evaluation.md`
- `design/semantic-dictionary.yaml`
- target Experience API folder

## Outputs

- `contract/openapi.yaml` for REST Experience APIs
- `contract/graphql.schema.graphql` for GraphQL Experience APIs

## Rules

- Shape contracts for the supported flow and consumer needs (frontend details excluded).
- Do not absorb core domain logic into Experience APIs.
- Preserve semantic field naming aligned to `semantic-dictionary.yaml` and BIAN BOM concepts where applicable.
- Do not rename the same business concept differently across layers without rationale.
- Do not generate Business or Domain contracts in this skill.
