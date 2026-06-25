# Schemas

This folder contains the canonical output contracts for the target architecture workflow.

Use these schemas as the source of truth for generated YAML and Markdown artifacts. Skills must reference these schemas instead of redefining output structure inside long prompts.

## Schema usage rules

- Skills generate artifacts conforming to these schemas.
- Validators check artifacts against these schemas.
- Context files define governance and principles, not artifact shapes.
- New artifact types require a new schema file or an explicit schema extension.
- Do not duplicate full schema definitions inside agent or skill instructions.

## Core schemas

- `execution-plan.schema.yaml`
- `context-pack.schema.yaml`
- `component.schema.yaml`
- `api-landscape.schema.yaml`
- `frontend-landscape.schema.yaml`
- `cloud-landscape.schema.yaml`
- `cloud-provider-mapping.schema.yaml`
- `bian-source-index.schema.yaml`
- `bian-service-domain-evaluation.schema.yaml`
- `bian-contract-adoption.schema.yaml`
- `semantic-dictionary.schema.yaml`
- `persistence-model.schema.yaml`
- `cache-model.schema.yaml`
- `event-model.schema.yaml`
- `state-map.schema.yaml`
- `adr.schema.yaml`
- `validation-report.schema.yaml`
