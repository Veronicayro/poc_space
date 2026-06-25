# v3 to v4 Migration Notes

## Problem corrected

v3 placed agents and skills correctly, but the usage model still required prompts to describe too much orchestration. v4 moves the phase choreography into the agent.

## Major changes

- Added internal phase catalog to `.github/agents/target-architecture-design.agent.md`.
- Added enterprise capability alignment before solution/API/component design.
- Added generic domain standard provider abstraction with BIAN Release 14 as default.
- Added new skills:
  - `architecture-workspace-readiness`
  - `domain-standard-baseline-indexer`
  - `enterprise-capability-mapper`
  - `architecture-standards-validator`
  - `experience-contract-designer`
- Expanded architecture governance rules to restore naming, BIAN, API, frontend, persistence, cache, event, state and cloud rules.
- Updated `architecture-scope-planner` to infer execution mode instead of requiring it in the prompt.
- Added schemas:
  - `enterprise-capability-map.schema.yaml`
  - `domain-standard-alignment.schema.yaml`

## New usage pattern

Instead of:

```text
Run these 12 steps...
```

Use:

```text
Run target architecture phase enterprise-capability-alignment for functionality/cxp.
```
