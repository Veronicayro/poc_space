---
applyTo: "functionality/**/design/**,agents/**,.github/skills/**,context/**"
---

# Architecture Design Instructions

Apply these rules when creating or editing architecture design artifacts.

## Layering

Use these layers consistently:

- experience
- business
- domain
- support
- data
- cache
- events
- security
- observability

## API responsibilities

- Experience APIs support a channel or user journey and shape data for consumer needs.
- Business APIs orchestrate reusable business capabilities and cross-domain process logic.
- Domain APIs expose stable non-orchestrating domain capabilities.
- Support APIs isolate legacy, external, or protocol-specific integration concerns.

## Mandatory traceability

Every generated component must have:

- purpose
- owner scope
- responsibility boundary
- consumers
- dependencies
- state ownership when applicable
- non-functional requirements when applicable
- decision: reuse, modify, create, or deprecate

## Output format

Prefer YAML for structured inventories and Markdown for rationale. Mermaid diagrams must be stored as `.mmd` files.
