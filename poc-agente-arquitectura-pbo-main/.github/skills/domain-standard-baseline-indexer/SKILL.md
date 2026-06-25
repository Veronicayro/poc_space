---
name: domain-standard-baseline-indexer
status: DEPRECATED
deprecated_by: bian-baseline-indexer
description: >-
  DEPRECATED. Skill reemplazada por `bian-baseline-indexer`, que cubre el mismo
  propósito para BIAN Release 14. Para soporte de proveedores futuros (ACORD,
  TM Forum), crear una skill específica en lugar de extender esta.
---

> ⚠️ **SKILL DEPRECADA** — No invocar. Usar `.github/skills/bian-baseline-indexer/SKILL.md`.
>
> Esta skill queda como referencia histórica. Produce los mismos outputs que
> `bian-baseline-indexer` y su uso puede generar artefactos duplicados.

# Domain Standard Baseline Indexer Skill (DEPRECADA)

## Motivo de deprecación

`bian-baseline-indexer` cubre exactamente el mismo propósito para el proveedor
activo (BIAN Release 14): fetching/lectura de baselines, construcción del
source index y registro de gaps de acceso.

Ambas skills producían los mismos outputs (`design/bian/bian-release14-source-index.yaml`,
`design/bian/gaps-and-access-issues.md`, `design/bian/selected-baselines/`),
generando riesgo de doble escritura y consumo innecesario de tokens.

## Skill canónica

Usar: `.github/skills/bian-baseline-indexer/SKILL.md`
