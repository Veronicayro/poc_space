# Target Architecture Refactor Pack v4

This version restructures the target architecture agent as a true orchestrator for GitHub Copilot Cloud Agent / Copilot coding agent usage.

## What changed from v3

1. The orchestration is now internal to the agent. You no longer need to paste the full phase choreography in every prompt.
2. Enterprise capability alignment comes before solution/API/component design.
3. BIAN is modeled as the default domain standard provider, but the workflow is decoupled so ACORD, TM Forum or another industry standard can be introduced later.
4. The original architecture rules were restored as governance rules, schemas and validation gates.
5. `architecture-scope-planner` no longer requires the user to provide `execution_mode`; it infers it from constraints and allows optional overrides.
6. Bootstrap was renamed conceptually to Workspace Readiness / Control Plane Initialization. It is not design work; it verifies inputs and initializes the workflow control plane.

## Recommended structure

```text
.github/
  copilot-instructions.md
  instructions/
  agents/
    target-architecture-design.agent.md
  skills/
    <skill-name>/SKILL.md

architecture/
  context/
  schemas/
  prompts/
  migration/

functionality/<ID>/
  state.yaml
  discovery/
  supplemental-context/
  design/
```

## Minimal usage

Use a short command. The agent already knows the orchestration.

```text
Use .github/agents/target-architecture-design.agent.md.
Run target architecture phase enterprise-capability-alignment for functionality/cxp.
```

Or:

```text
Use .github/agents/target-architecture-design.agent.md.
Continue the target architecture workflow for functionality/cxp from the current phase in state.yaml.
```

## Phase names

Phase names are defined by the canonical phase catalog in:
- `.github/agents/target-architecture-design.agent.md`

Use the exact names listed there. (If the agent supports aliases, they are documented in that file.)

## Core principle

The prompt selects the phase and optional target component/provider. The agent owns the orchestration, gates, skill order, required inputs and required outputs.
