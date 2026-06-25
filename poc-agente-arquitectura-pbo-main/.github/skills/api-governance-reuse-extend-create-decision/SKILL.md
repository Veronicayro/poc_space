# Skill — api-governance-reuse-extend-create-decision (Phase 0)

## Objetivo

Analizar un **requerimiento funcional** contra el **catálogo de APIs existente** y emitir **una decisión única**:

- `REUSE` (reutilizar una API existente)
- `EXTEND` (extender una API existente sin romper compatibilidad)
- `CREATE` (crear una nueva API, solo si no existe alternativa)

Esta skill es **agnóstica** a la funcionalidad y aplica gobernanza estricta para evitar duplicidad.

---

## Entradas (inputs)

1) Requerimiento funcional provisto por el usuario (texto o YAML).
2) Catálogo de APIs del repo:
   - `catalog/api-catalog-index.yaml`
   - `catalog/api-catalog-mock-bank.yaml`
   - `catalog/domains/*.yaml` (dominios y APIs por dominio)

---

## Salidas (outputs) — fuera de `functionality/` + respuesta por chat

> **Siempre** persistir el input antes del análisis.

- `architecture/context/api-governance/phase0/requests/<request-id>.yaml`
- `architecture/context/api-governance/phase0/decisions/<request-id>.md`
- (opcional) `architecture/context/api-governance/phase0/decisions/<request-id>.yaml`

Además, el agente debe **devolver por chat** el mismo contenido del reporte de decisión (en el **formato obligatorio**) como respuesta al usuario, y referenciar las rutas de los archivos persistidos.

---

## Procedimiento (flujo obligatorio)

### Paso 0 — Persistencia del input (obligatorio)

Crear `requests/<request-id>.yaml` con:
- `request_id`
- `timestamp`
- `functional_requirement` (texto o YAML embebido)
- `catalog_sources` (rutas del catálogo consultado)
- `constraints` (si el usuario indicó reglas adicionales)

**Regla:** no continuar al análisis si no se persistió el input.

### Paso 1 — Búsqueda en catálogo (y BIAN baseline cuando aplique)

1. Identificar dominio/subdominio candidato a partir del requerimiento.
2. Buscar APIs existentes por:
   - Recurso (customers, accounts, loans, payments, cards, compliance, risk, etc.)
   - Operaciones (create/get/update/delete/authorize/execute/retrieve/submit, etc.)
   - Casos de uso similares
3. **Si el requerimiento declara explícitamente BIAN** (p. ej. `x-bian-sd`, `x-bian-release`, `x-bian-control-record`) o si la funcionalidad cae en un Service Domain BIAN, consultar el baseline respetando la **jerarquía cache-first obligatoria** (Rule 3 del agente — nunca saltar directamente al YAML crudo):
   - **[OPT-A] Primero:** leer el JSON cacheado `architecture/cache/bian/release14.0.0/index/<ServiceDomain>.json` (contiene operationIds, métodos y propiedades ya resueltas).
   - **[OPT-B] Si OPT-A no existe:** ejecutar `python architecture/scripts/bian_extract_service_domain.py --service-domain <ServiceDomain> --release 14.0.0` y leer el JSON generado.
   - **[OPT-C] Solo si OPT-A y OPT-B fallan:** leer el YAML crudo `architecture/cache/bian/release14.0.0/oas3/yamls/<ServiceDomain>.yaml` (o `asyncapi-3.x/yamls/<ServiceDomain>.yaml` si aplica).
   - **Prohibido:** saltar directamente a OPT-C sin intentar OPT-A y OPT-B.
   - Registrar qué opción se usó en el artefacto de salida (`requests/<request-id>.yaml` campo `bian_source_option`).
   - Extraer **paths exactos** y `operationId`s exactos del baseline para usarlos como evidencia.

**Evidencia mínima:** listar 1–5 APIs más cercanas con su versión (si aplica) y endpoints relevantes; y si aplica BIAN, referenciar el baseline (ruta) + paths/operationIds exactos.

### Paso 2 — Análisis de compatibilidad

Para cada API candidata, clasificar:

- **Cubre completamente**: endpoints existentes satisfacen el caso sin cambios.
- **Cubre parcialmente**: falta endpoint/campo/operación, pero puede añadirse sin romper compatibilidad.
- **Sin relación**: no corresponde al dominio o al caso.

### Paso 3 — Decisión (obligatoria y única)

Seleccionar SOLO una:

- `REUSE` si existe API que cubre completamente.
- `EXTEND` si existe API que cubre parcialmente y puede ampliarse **backward-compatible**.
- `CREATE` solo si **no existe** API adecuada.

### Paso 4 — Acciones según decisión

#### Si REUSE
- Indicar API existente (nombre + versión).
- Indicar endpoint específico.
- Proveer ejemplo de uso (request/response mínimo).

#### Si EXTEND
- Indicar API existente (nombre + versión).
- Proponer:
  - nuevo endpoint o recurso, **o**
  - nuevos campos
- Validar backward compatibility:
  - añadir campos opcionales, no remover/renombrar existentes
  - no cambiar semantics de respuestas existentes
- Sugerir si requiere nueva versión (solo si el cambio no puede ser compatible).
- **Regla BIAN (obligatoria):** si el requerimiento exige adopción BIAN "tal cual", los **paths y operationIds** propuestos deben provenir **textualmente** del baseline BIAN en `architecture/cache/bian/release14.0.0/**/yamls/`. Está prohibido inventar/normalizar rutas.

#### Si CREATE
- Definir dominio
- Nombre de la API (consistente con catálogo)
- Endpoints base RESTful (sin verbos en la URL)
- Evitar duplicación de recursos existentes

---

## Formato de salida (obligatorio)

1) El archivo `decisions/<request-id>.md` debe respetar EXACTAMENTE:

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

2) La respuesta por chat al usuario debe incluir **exactamente el mismo bloque** anterior (mismo formato), seguido por una línea breve con los paths:
- Request persistido: `architecture/context/api-governance/phase0/requests/<request-id>.yaml`
- Decision persistida: `architecture/context/api-governance/phase0/decisions/<request-id>.md`

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

---

## Reglas de gobernanza (hard rules)

- NUNCA crear nueva API si una existente puede reutilizarse o extenderse.
- Evitar duplicación de recursos (no crear `/createPayment` si ya existe `/payments`).
- Mantener consistencia RESTful **salvo** que el requerimiento exija adopción BIAN literal; en ese caso, prevalece el baseline BIAN (paths/operationIds tal cual).
- Respetar el dominio de negocio (bounded context).
- Considerar versionado solo ante cambios incompatibles.

---

## Stop-the-line (obligatorio)

Tras emitir el reporte:
- **Publicar la decisión en el chat** (formato obligatorio).
- **Persistir request y decisión** en `architecture/context/api-governance/phase0/**`.
- **No** producir artefactos de diseño (contracts/components/api-landscape) ni tocar `functionality/` hasta confirmación explícita del usuario sobre la decisión.
