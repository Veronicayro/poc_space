# Refactor Pack v3 Migration Map

This pack preserves the v2 content while moving files to Copilot-friendly repository locations.

## Path mapping

| v2 path | v3 path |
|---|---|
| `agents/target-architecture-design.agent.md` | `.github/agents/target-architecture-design.agent.md` |
| `skills/adr-generator.md` | `.github/skills/adr-generator/SKILL.md` |
| `skills/api-landscape-designer.md` | `.github/skills/api-landscape-designer/SKILL.md` |
| `skills/architecture-scope-planner.md` | `.github/skills/architecture-scope-planner/SKILL.md` |
| `skills/artifact-completeness-validator.md` | `.github/skills/artifact-completeness-validator/SKILL.md` |
| `skills/backend-component-designer.md` | `.github/skills/backend-component-designer/SKILL.md` |
| `skills/bian-baseline-indexer.md` | `.github/skills/bian-baseline-indexer/SKILL.md` |
| `skills/bian-contract-deriver.md` | `.github/skills/bian-contract-deriver/SKILL.md` |
| `skills/bian-service-domain-evaluator.md` | `.github/skills/bian-service-domain-evaluator/SKILL.md` |
| `skills/cloud-logical-designer.md` | `.github/skills/cloud-logical-designer/SKILL.md` |
| `skills/cloud-provider-mapper.md` | `.github/skills/cloud-provider-mapper/SKILL.md` |
| `skills/cloud-provider-realizer.md` | `.github/skills/cloud-provider-realizer/SKILL.md` |
| `skills/context-pack-builder.md` | `.github/skills/context-pack-builder/SKILL.md` |
| `skills/data-cache-event-state-designer.md` | `.github/skills/data-cache-event-state-designer/SKILL.md` |
| `skills/diagram-generator.md` | `.github/skills/diagram-generator/SKILL.md` |
| `skills/existing-landscape-analyzer.md` | `.github/skills/existing-landscape-analyzer/SKILL.md` |
| `skills/experience-api-style-evaluator.md` | `.github/skills/experience-api-style-evaluator/SKILL.md` |
| `skills/frontend-mfe-designer.md` | `.github/skills/frontend-mfe-designer/SKILL.md` |
| `skills/security-nfr-observability-designer.md` | `.github/skills/security-nfr-observability-designer/SKILL.md` |
| `skills/semantic-dictionary-builder.md` | `.github/skills/semantic-dictionary-builder/SKILL.md` |
| `context/architecture-governance.md` | `architecture/context/architecture-governance.md` |
| `context/artifact-taxonomy.md` | `architecture/context/artifact-taxonomy.md` |
| `context/bian-release14-governance.md` | `architecture/context/bian-release14-governance.md` |
| `context/cloud-provider-capability-map.md` | `architecture/context/cloud-provider-capability-map.md` |
| `context/output-schemas.md` | `architecture/context/output-schemas.md` |
| `schemas/README.md` | `architecture/schemas/README.md` |
| `schemas/adr.schema.yaml` | `architecture/schemas/adr.schema.yaml` |
| `schemas/api-landscape.schema.yaml` | `architecture/schemas/api-landscape.schema.yaml` |
| `schemas/bian-contract-adoption.schema.yaml` | `architecture/schemas/bian-contract-adoption.schema.yaml` |
| `schemas/bian-service-domain-evaluation.schema.yaml` | `architecture/schemas/bian-service-domain-evaluation.schema.yaml` |
| `schemas/bian-source-index.schema.yaml` | `architecture/schemas/bian-source-index.schema.yaml` |
| `schemas/cache-model.schema.yaml` | `architecture/schemas/cache-model.schema.yaml` |
| `schemas/cloud-landscape.schema.yaml` | `architecture/schemas/cloud-landscape.schema.yaml` |
| `schemas/cloud-provider-mapping.schema.yaml` | `architecture/schemas/cloud-provider-mapping.schema.yaml` |
| `schemas/component.schema.yaml` | `architecture/schemas/component.schema.yaml` |
| `schemas/context-pack.schema.yaml` | `architecture/schemas/context-pack.schema.yaml` |
| `schemas/event-model.schema.yaml` | `architecture/schemas/event-model.schema.yaml` |
| `schemas/execution-plan.schema.yaml` | `architecture/schemas/execution-plan.schema.yaml` |
| `schemas/frontend-landscape.schema.yaml` | `architecture/schemas/frontend-landscape.schema.yaml` |
| `schemas/persistence-model.schema.yaml` | `architecture/schemas/persistence-model.schema.yaml` |
| `schemas/semantic-dictionary.schema.yaml` | `architecture/schemas/semantic-dictionary.schema.yaml` |
| `schemas/state-map.schema.yaml` | `architecture/schemas/state-map.schema.yaml` |
| `schemas/validation-report.schema.yaml` | `architecture/schemas/validation-report.schema.yaml` |
| `prompts/run-target-architecture-design.md` | `architecture/prompts/run-target-architecture-design.md` |

## Compatibility note

The root `AGENTS.md` remains in place as a repository-level entry point. It now points to `.github/agents/target-architecture-design.agent.md` and `.github/skills/<skill-name>/SKILL.md`.
