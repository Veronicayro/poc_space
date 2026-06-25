---
name: data-cache-event-state-designer
description: Designs persistence, cache, event, and state artifacts for components that require them.
---

# Skill: Data, Cache, Event, and State Designer

## Goal

Design persistence, cache, event, and state artifacts for components that require them.

## Schema reference

Use `architecture/schemas/persistence-model.schema.yaml, architecture/schemas/cache-model.schema.yaml, architecture/schemas/event-model.schema.yaml, architecture/schemas/state-map.schema.yaml`.

## Inputs

- `design/component-inventory.yaml`
- `design/api-landscape.yaml`
- component folders
- `design/semantic-dictionary.yaml`

## Outputs

Conditionally write per component:

```text
data/persistence-model.yaml
cache/cache-model.yaml
events/event-model.yaml
state/state-map.yaml
```

Also write or update:

```text
design/data/data-landscape.yaml
design/cache/cache-landscape.yaml
design/events/event-landscape.yaml
```

## Rules

- Generate persistence only when a component owns, mutates, or requires durable state.
- Generate cache only when there is clear architectural value.
- Generate events only when they support decoupling, eventual consistency, deferred flows, integration, or state progression.
- Prefer Avro for governed internal event contracts unless JSON is justified.

## General skill rules

See: `.github/copilot-instructions.md` (shared "general skill rules").
