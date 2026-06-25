---
applyTo: "functionality/**/design/bian/**,functionality/**/design/business/**,functionality/**/design/domain/**"
---

# BIAN Governance Instructions

Business and Domain API design must be grounded in BIAN Release 14 baseline artifacts.

## Non-negotiable rules

- Use BIAN Release 14 only.
- Do not select Service Domains from model memory.
- Use `design/bian/bian-release14-source-index.yaml` as the only Service Domain inventory.
- Inspect selected baseline YAML bodies before deriving operations or schemas.
- If BIAN files cannot be fetched or read, block Business and Domain contract generation.
- Record unresolved mappings in `design/bian/gaps-and-access-issues.md`.

## Required evidence per Business or Domain API

Each Business or Domain API must include `contract/bian-adoption.yaml` with:

- BIAN release
- selected Service Domain
- source OAS3 file
- source AsyncAPI file when applicable
- selected paths or channels
- selected operations or messages
- selected schemas
- omitted baseline elements
- adaptation rationale
- validation status
