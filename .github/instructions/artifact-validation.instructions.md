---
applyTo: "functionality/**/design/**"
---

# Artifact Validation Instructions

Before marking a target architecture design complete, validate the artifact set.

## Completion policy

The design is incomplete if any required root artifact, BIAN artifact, component descriptor, API contract, integration model, sequence diagram, flow diagram, or conditional persistence/cache/event/state artifact is missing.

## Validation output

Write validation findings to:

```text
design/validation-report.yaml
```

The validation report must classify issues as:

- blocking
- warning
- informational

A design stage can be marked complete only when no blocking issue remains.
