# Target Architecture Phase Outputs Catalog (Canonical)

This document is the **single source of truth** for which artifacts the target-architecture orchestrator is allowed to create/update.

## Scope and constraints

- The agent is an **architecture orchestrator** for **banking** target architecture (TO-BE) for **one functionality at a time**.
- The agent **must not** generate application code, microservice implementations, IaC code, or any artifacts not listed here.
- The agent **may update in-place** any artifact listed here for the active `functionality/<ID>/` only.
- If an artifact is conditional and the condition is not met, the agent must mark it as **N/A** in its run manifest; it must **not** create placeholder files.

Paths below are **relative to** `functionality/<ID>/`.

---

## Phase 0 — `workspace-readiness` (control plane init)

**Required outputs**
- `design/context/gaps.yaml`

**State update**
- `state.yaml` (initialize phase section only)

---

## Phase 1 — `enterprise-capability-alignment` (EA alignment + BIAN)

**Required outputs**
- `design/context/context-pack.yaml`
- `design/enterprise-capability-map.yaml`
- `design/domain-standard-alignment.yaml`
- `design/semantic-dictionary.yaml`

**Conditional outputs (BIAN selected as domain standard provider)**
- `design/bian/bian-release14-source-index.yaml`
- `design/bian/bian-service-domain-evaluation.yaml`
- `design/bian/gaps-and-access-issues.md`

---

## Phase 2 — `scope-and-execution-planning` (execution plan)

**Required outputs**
- `design/execution-plan.yaml`
- `design/existing-component-impact.yaml`

---

## Phase 3 — `solution-landscape` (solution target landscape)

**Required outputs**
- `design/architecture-overview.md`
- `design/api-landscape.yaml`
- `design/component-inventory.yaml`

---

## Phase 4 — `api-landscape-design` (API decisions + ADRs)

**Required outputs**
- `design/api-landscape.yaml` (update from Phase 3)
- `design/experience-api-style-evaluation.md`

**Conditional outputs**
- `design/adr/tobe/*.md` (API decision ADRs; one or more files)

**Notes**
- This phase must not generate component-level API contracts.

---

## Phase 5 — `backend-component-design` (per component)

**Scope rule**
- Only for one target component per run (or the next pending component from state).

**Required outputs (per component directory)**
- `design/{experience|business|domain|support}/<component>/component.yaml`
- `design/{experience|business|domain|support}/<component>/readme.md`
- `design/{experience|business|domain|support}/<component>/integration/integration-model.yaml`

**Conditional outputs**
- `design/{experience|business|domain}/<component>/models/domain-model.yaml` (Business/Domain APIs only)

**Explicitly excluded**
- OpenAPI / AsyncAPI / GraphQL contracts (handled by Phase 6).

---

## Phase 6 — `backend-contract-design` (per API contract)

**Scope rule**
- Only for one target API per run (or the next pending API from state).

**Required outputs (per component directory)**
- `design/{experience|business|domain|support}/<component>/contract/openapi.yaml` **OR**
- `design/{experience|business}/<component>/contract/graphql.schema.graphql` (Experience APIs only; when selected)

**Conditional outputs**
- `design/{experience|business|domain|support}/<component>/contract/asyncapi.yaml` (only when async is required)
- `design/{business|domain}/<component>/contract/bian-adoption.yaml` (Business/Domain APIs only)
- `design/bian/bian-contract-adoption-matrix.yaml` (only when at least one Business/Domain contract is produced)

---

## Phase 7 — `backend-diagram-design` (diagrams)

**Scope rule**
- Either one target component per run, or `scope: backend-general`.

**Required outputs (per component directory)**
- `design/{experience|business|domain|support}/<component>/sequence/sequence.mmd`
- `design/{experience|business|domain|support}/<component>/flow/flow.mmd`

**Conditional outputs**
- `design/{experience|business|domain|support}/<component>/state/state-map.yaml` (only when stateful)

**Required outputs (global backend)**
- `design/diagrams/architecture-backend-tobe.mmd`

**Conditional outputs (transition exists)**
- `design/diagrams/architecture-backend-transition.mmd`

---

## Phase 8 — `adr-generation` (ADRs refresh)

**Required outputs**
- `design/adr/tobe/*.md` (one or more files)

**Conditional outputs (transition exists)**
- `design/adr/transition/*.md`

---

## Phase 9 — `validation-and-state-update` (validation + state)

**Required outputs**
- `design/validation-report.yaml`
- `state.yaml` (update)

---

# End-to-end “agent completion” expected artifact set

When the workflow is completed end-to-end for a functionality, the final expected outputs are:

1. **Control plane**
   - `state.yaml`
   - `design/context/gaps.yaml`

2. **EA + domain standard alignment**
   - `design/context/context-pack.yaml`
   - `design/enterprise-capability-map.yaml`
   - `design/domain-standard-alignment.yaml`
   - `design/semantic-dictionary.yaml`
   - *(if BIAN selected)* `design/bian/bian-release14-source-index.yaml`
   - *(if BIAN selected)* `design/bian/bian-service-domain-evaluation.yaml`
   - *(if BIAN selected)* `design/bian/gaps-and-access-issues.md`

3. **Execution planning**
   - `design/execution-plan.yaml`
   - `design/existing-component-impact.yaml`

4. **Solution landscape**
   - `design/architecture-overview.md`
   - `design/api-landscape.yaml`
   - `design/component-inventory.yaml`

5. **API decisions**
   - `design/experience-api-style-evaluation.md`
   - `design/adr/tobe/*.md` *(one or more ADRs across API decisions)*

6. **Backend component design + contracts + diagrams**
   - `design/{experience|business|domain|support}/<component>/**` *(for each selected API component; as per Phases 5–7)*
   - *(if any Business/Domain contract produced)* `design/bian/bian-contract-adoption-matrix.yaml`

7. **Validation**
   - `design/validation-report.yaml`
