---
name: bian-baseline-indexer
description: Fetches or reads BIAN Release 14 baseline files and builds a trusted source index for downstream alignment and contract work.
---

# Skill: BIAN Baseline Indexer

## Goal

Fetch or read BIAN Release 14 baseline files and build a trusted source index.

## Inputs

- BIAN Release 14 OAS3 source directory: architecture/cache/bian/release14.0.0/oas3/yamls
- BIAN Release 14 AsyncAPI 3.x source directory: architecture/cache/bian/release14.0.0/asyncapi-3.x/yamls

## Outputs

Write:

```text
design/bian/bian-release14-source-index.yaml
design/bian/gaps-and-access-issues.md
```

Create:

```text
design/bian/selected-baselines/
```

## Output Schema reference

Use `architecture/schemas/bian-source-index.schema.yaml`.

## Rules

- Do not select Service Domains.
- Do not generate contracts.
- Do not rely on model memory.
- If source access fails, write a blocking gap and stop BIAN-dependent steps.
- Prefer a local cached registry when it is already present and matches Release 14.
- When a Service Domain candidate is evaluated, the runner MUST build or reuse an operation index cache:
  - Read cache first:
    - `architecture/cache/bian/release<release>/index/<ServiceDomain>.json`
  - If missing, create it once (no ad-hoc scripts):
    - `python architecture/scripts/bian_extract_service_domain.py --service-domain <ServiceDomain> --release <release>`
  - Store only a reference to that cache in `design/bian/bian-release14-source-index.yaml` as `operation_index_ref`.
  - Avoid dumping large OAS3 fragments, large lists of paths, or schema bodies inline in Phase 1 outputs.
