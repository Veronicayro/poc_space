# Target Architecture Design Prompt Examples

## Continue automatically from state

```text
Use .github/agents/target-architecture-design.agent.md.
Continue the target architecture workflow for functionality/cxp from the current phase in state.yaml.
```

## Run a specific phase

```text
Use .github/agents/target-architecture-design.agent.md.
Run target architecture phase enterprise-capability-alignment for functionality/cxp.
```

## Run backend component design for one component

```text
Use .github/agents/target-architecture-design.agent.md.
Run target architecture phase backend-component-design for functionality/cxp.
Target component: api-business-payment-order-initiation.
```

## Run contract design for one API

```text
Use .github/agents/target-architecture-design.agent.md.
Run target architecture phase backend-contract-design for functionality/cxp.
Target component: api-domain-party-reference-data-directory.
```

## Run cloud architecture for one provider

```text
Use .github/agents/target-architecture-design.agent.md.
Run target architecture phase cloud-architecture for functionality/cxp.
Target provider: Azure.
```

## Important

Do not paste the full orchestration steps. The agent owns the phase catalog, skills, gates and outputs.
