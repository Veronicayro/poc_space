---
name: architecture-workspace-readiness
description: Initializes and verifies the target architecture workflow control plane without producing architecture design.
---

# Architecture Workspace Readiness Skill

## Purpose

Prepare the repository workspace and workflow state for phased target architecture work. This is not a design phase.

## Inputs

- `functionality/<ID>/state.yaml`
- `functionality/<ID>/discovery/`
- `functionality/<ID>/supplemental-context/`

## Outputs

- `functionality/<ID>/design/context/gaps.yaml`
- initialized phase tracking section in `functionality/<ID>/state.yaml`

## Rules

- Do not design APIs, components, BIAN mappings, deployment/runtime (cloud excluded), contracts, diagrams or ADRs.
- Create missing base folders only when needed.
- Record missing inputs as blocking or non-blocking gaps.
- Initialize phase state so later phases can continue without repeating previous work.

## Required checks

- functionality id exists
- state file exists and is readable
- discovery folder exists
- supplemental context folder exists
- design folder exists or can be created
- architecture assets exist under `architecture/context/` and `architecture/schemas/`
