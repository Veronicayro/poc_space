# Copilot Repository Instructions

This repository uses phased target architecture generation.

Use `.github/agents/target-architecture-design.agent.md` for target architecture work.

## Core rules

- The agent is the orchestrator. Do not require users to paste the full workflow.
- Always align functionality/business cases to enterprise capabilities and the configured domain standard before detailed solution design.
- Default banking domain standard is BIAN Release 14.
- Do not infer BIAN Service Domains from model memory.
- Use `architecture/context/` for governance rules.
- Use `architecture/schemas/` as canonical output contracts.
- Use `.github/skills/*/SKILL.md` for task-specific capabilities.
- Keep design output under `functionality/<ID>/design/`.
- Validate phase outputs before marking a phase complete in `state.yaml`.

## General skill rules (apply to every skill unless explicitly overridden)

- Work only on the current functionality.
- Prefer reading `design/context/context-pack.yaml` first when it exists.
- Prefer structured YAML outputs for machine-consumable artifacts.
- Write assumptions explicitly.
- If evidence is missing, write a gap instead of inventing facts.
- Keep outputs concise and directly consumable by downstream skills.
