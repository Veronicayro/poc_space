# BIAN Alignment Decision Framework (Early-Stage, Token-Efficient)

## Objective (do this first)
Determine the correct **BIAN alignment level** for **each** capability, API, bounded context, microservice, business process, integration, or architectural component identified during TO‑BE design.

The objective is **not** “does BIAN apply or not”.

The objective is to classify the **alignment level**:

- **REQUIRED**
- **ASSOCIATED**
- **NONE**

This evaluation must be performed **before**:
- defining boundaries (service boundaries / bounded contexts),
- designing contracts (OpenAPI/AsyncAPI),
- defining microservices,
- modeling integrations and architectural artifacts.

> Optimization rule: if the artifact is classified as **NONE**, do not spend tokens searching for BIAN Service Domains.

---

## Hard rules (non-negotiable)
1. **Never use keywords, paths, technologies, vendors, or names** as decision criteria.
2. **Evaluate business purpose and architectural responsibility.**
3. **Never invent Service Domains.** Only official BIAN Service Domains are allowed.
4. **Service Domain ≠ microservice.** A single Service Domain can be implemented by N services.
5. **Consult the official BIAN catalog before selecting a Service Domain.** Never rely on LLM memory.
6. If multiple Service Domains are possible, **justify** the selection and **why alternatives were rejected**.

---

## Alignment levels

### REQUIRED
Classify as **REQUIRED** when the capability **owns and manages** a **banking business asset** and represents a business-recognizable banking capability.

Typical characteristics:
- Owns business entities, state, lifecycle.
- Owns business rules/decisions.
- Maps to one or more **BIAN Service Domains**.

Output:
- `BIAN_ALIGNMENT = REQUIRED`
- Identify `Mapped Service Domain` (and alternatives considered).

---

### ASSOCIATED
Classify as **ASSOCIATED** when the capability primarily **supports** one or more banking capabilities but does **not** own the primary banking asset.

Typical characteristics:
- Workflows, orchestration, validations, supporting rules.
- Exists **because** a “parent” banking capability exists.
- Must not be modeled as an independent Service Domain unless BIAN explicitly defines it.

Output:
- `BIAN_ALIGNMENT = ASSOCIATED`
- Identify:
  - `Parent Service Domain`
  - supporting relationship / dependency.

---

### NONE
Classify as **NONE** when it is infrastructure/technology/platform or an implementation concern.

Examples:
- API Gateway, OAuth, Kafka infrastructure, logging/monitoring, adapters, ERP/bank connectors, schedulers, storage, etc.

Output:
- `BIAN_ALIGNMENT = NONE`
- `Mapped Service Domain = N/A`

---

## Decision criteria (boolean answers)
Evaluate **without assumptions**:

1) **Business Asset Ownership**  
Does it own/manage a banking business asset? (Customer, Account, Loan, Card, Payment, Agreement, Product, Facility, Collateral, etc.)

2) **Business Lifecycle Ownership**  
Does it own lifecycle transitions? (create/approve/reject/activate/close/settle/cancel…)

3) **Business Rule Ownership**  
Does it own banking business rules (not just technical validations)?

4) **Business Dependency**  
Would it still exist if the parent banking capability disappeared?  
- If it would NOT exist → `TRUE` (business-dependent)  
- If it would still exist → `FALSE`

5) **Technology Independence**  
Would it still exist if all vendors/stacks/protocols/infra were replaced?

---

## Classification algorithm (minimal)
- If `AssetOwnership=TRUE` AND `LifecycleOwnership=TRUE` AND `RuleOwnership=TRUE` AND `TechnologyIndependence=TRUE`
  → **REQUIRED**
- Else if `BusinessDependency=TRUE`
  → **ASSOCIATED**
- Else
  → **NONE**

---

## Mandatory step: consult BIAN catalog (only when needed)
- If the result is **REQUIRED** or **ASSOCIATED**:
  1) Consult the official BIAN catalog (in this repo: `architecture/cache/bian/release14.0.0/...`).
  2) Select the closest Service Domain.
  3) If there is more than one candidate: list 2–3 candidates and justify.

> If the result is **NONE**: do not consult the catalog.

---

## Required output format (copy/paste)
Capability: <name>

Alignment Level: REQUIRED | ASSOCIATED | NONE

Business Asset Ownership: TRUE | FALSE  
Business Lifecycle Ownership: TRUE | FALSE  
Business Rule Ownership: TRUE | FALSE  
Business Dependency: TRUE | FALSE  
Technology Independence: TRUE | FALSE

Mapped Service Domain: <service domain or N/A>  
Parent Service Domain: <service domain or N/A>

Justification: <reasoning>  
Reasoning Trace: <1-5 bullets describing observed purpose/responsibility>  
Confidence: 0-100%

---

## Micro-optimization guidance (for agents)
- Run this evaluation with short responses (booleans + 3–5 bullets) for each capability at the beginning.
- Only afterwards (if REQUIRED/ASSOCIATED) expand in detail and design APIs/artifacts.
