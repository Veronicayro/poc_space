# ADR-CXP-001: Uso de REST/JSON como estilo de API

**Status:** Accepted  
**Date:** 2026-06-17  
**Functionality:** CXP - Cuentas por Pagar

---

## Contexto

El sistema CXP expone operaciones de facturas y pagos a una SPA React con tres roles (ANALYST, MANAGER, TREASURER). Se requiere definir el estilo de API para todas las capas.

## Decisión

Se adopta **REST/JSON** con URI versioning `/v1/` para todas las capas del sistema CXP.

## Justificación

- Alineado con DDA-002 del contexto del proyecto
- Compatibilidad nativa con React Query/Axios
- Caché HTTP nativa para GETs
- RBAC por ruta más simple que por campo (GraphQL)
- Interoperabilidad con ERP y Banking System

## Alternativas Descartadas

| Alternativa | Razón |
|---|---|
| GraphQL | Overkill; RBAC por campo más complejo |
| gRPC | No compatible con navegadores sin proxy |

## Consecuencias

- **+** Interoperabilidad, simplicidad, estándar ampliamente adoptado
- **-** Posibles múltiples round-trips (mitigado con BFF pattern)
- Breaking changes requieren nueva versión `/v2/`
