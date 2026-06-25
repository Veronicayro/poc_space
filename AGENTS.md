# Repository Agent Entry Point

Use `.github/agents/target-architecture-design.agent.md` as the primary orchestrator for target architecture work.

## How to invoke

Preferred minimal command:

```text
Use .github/agents/target-architecture-design.agent.md.
Run target architecture phase <phase-name> for functionality/<ID>.
```

The agent must use its internal phase catalog and must not require the user to paste the orchestration steps.

## Supported phase names

Phase names are defined by the canonical phase catalog in:
- `.github/agents/target-architecture-design.agent.md`

Use the exact names listed there. (If the agent supports aliases, they are documented in that file.)

## Enterprise architecture priority

Always align business functionality and use cases to enterprise capabilities and the configured industry domain standard before designing APIs, components, contracts.

Default domain standard provider: BIAN Release 14.
Future domain standard providers may include ACORD, TM Forum or enterprise-specific capability maps.
