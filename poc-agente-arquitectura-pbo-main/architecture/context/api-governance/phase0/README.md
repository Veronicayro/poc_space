# Phase 0 — API governance decision (REUSE | EXTEND | CREATE)

Este directorio contiene artefactos **agnósticos** a una funcionalidad específica para ejecutar la **Fase 0** de gobernanza de APIs:

- **requests/**: persistencia del input del usuario (requerimiento + referencias al catálogo).
- **decisions/**: reporte de decisión y análisis, en el formato estructurado obligatorio.

## Objetivo

Antes de crear/nombrar/alterar APIs o contratos, se debe validar si el requerimiento:

1) puede **reutilizar** una API existente (`REUSE`), o  
2) debe **extender** una API existente sin romper compatibilidad (`EXTEND`), o  
3) requiere **crear** una nueva API (`CREATE`), solo si no hay alternativa.

## Regla de stop (hard gate)

No se deben producir artefactos de diseño de APIs/contratos (ni tocar `functionality/`) hasta que exista una decisión de Fase 0 y el usuario la confirme explícitamente.

## Formato de salida (reporte)

El reporte en `decisions/<request-id>.md` debe respetar EXACTAMENTE:

Decision: [REUSE | EXTEND | CREATE]
API Identificada:
[Nombre de la API o N/A]
Dominio:
[Dominio]
Análisis:
[Explicación clara de por qué se tomó la decisión]
Acción propuesta:
[Qué se debe hacer exactamente]
Propuesta técnica:
[Endpoints, cambios o nueva API según el caso]
Notas de gobernanza:
[Validación de consistencia, duplicidad, versionado]
