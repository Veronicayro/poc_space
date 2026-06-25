# Skill — bian-contract-deriver

## Objetivo

Derivar un contrato `openapi.yaml` **directamente desde el baseline BIAN Release 14** para APIs de tipo Business o Domain, generando también el archivo de evidencia `bian-adoption.yaml` y actualizando `bian-contract-adoption-matrix.yaml` — todo en una **única ejecución**.

Este skill aplica **exclusivamente** cuando `domain_standard.selected: true` AND `domain_standard.name: BIAN` en `domain-standard-alignment.yaml`.

---

## Verificación de aplicabilidad (obligatoria — ejecutar primero)

Leer `functionality/<ID>/design/domain-standard-alignment.yaml`:
- Si `domain_standard.selected: true` AND `domain_standard.name: BIAN` → aplicar este skill.
- Si no → **no aplicar este skill**; generar el contrato OpenAPI estándar basado en `component.yaml` y el `semantic-dictionary.yaml` (sin convenciones BIAN).

---

## Inputs

> **⚠️ Regla de acceso BIAN — leer ANTES de cualquier otra acción sobre el baseline:**
>
> El baseline BIAN se accede siguiendo esta jerarquía estricta. **NUNCA** ir directo al YAML crudo como primer paso:
>
> 1. **[OPT-A — obligatorio, siempre primero]** JSON cacheado:
>    `architecture/cache/bian/release14.0.0/index/<ServiceDomain>.json`
>    Contiene: `operationId`, `method`, `bian_operation`, `control_record`, propiedades de schemas ya resueltas.
> 2. **[OPT-B — si OPT-A no existe]** Generar el JSON con el script:
>    `python architecture/scripts/bian_extract_service_domain.py --service-domain <SD> --release 14.0.0`
>    Luego leer el JSON generado desde la ruta OPT-A.
> 3. **[OPT-C — solo si OPT-A y OPT-B fallan]** YAML OAS3 crudo:
>    `architecture/cache/bian/release14.0.0/oas3/yamls/<ServiceDomain>.yaml`
> 4. **AsyncAPI** (solo cuando el componente requiere mensajería asíncrona):
>    `architecture/cache/bian/release14.0.0/asyncapi-3.x/yamls/<ServiceDomain>.yaml`
>    (No existe JSON index para AsyncAPI; leer directamente, pero solo cuando es necesario.)
>
> Registrar qué opción se usó en el campo `bian_baseline_source` de `bian-adoption.yaml`.

Inputs requeridos (en este orden):
1. `functionality/<ID>/design/domain-standard-alignment.yaml` — verificar aplicabilidad y obtener el Service Domain seleccionado.
2. `functionality/<ID>/design/<layer>/<component>/component.yaml` — diseño del componente objetivo.
3. `functionality/<ID>/design/semantic-dictionary.yaml` — términos del dominio.
4. Baseline BIAN del Service Domain — acceder según jerarquía OPT-A/B/C descrita arriba.
5. `architecture/schemas/bian-contract-adoption.schema.yaml` — **lazy**: leer solo justo antes de escribir `bian-adoption.yaml`.

---

## Procedimiento (flujo obligatorio — single run)

Los pasos 1–5 deben completarse en una **única ejecución**. No dividir en múltiples runs para el mismo componente.

### Paso 1 — Acceder al baseline BIAN

Seguir jerarquía OPT-A → OPT-B → OPT-C.

Extraer del baseline:
- Nombre del Control Record.
- `operationId`s disponibles, métodos HTTP y tipos de operación BIAN (Initiate, Execute, Exchange, Retrieve, Update, Query).
- Nombres de campos clave en schemas de request/response.

Si el baseline es inaccesible por todas las rutas → emitir `BLOCK-01`; detener la ejecución del skill.

### Paso 2 — Generar `openapi.yaml` desde el baseline BIAN

El contrato debe derivarse estructuralmente del Control Record BIAN. Convenciones obligatorias:

**Bloque `info` — extensiones BIAN requeridas:**
```yaml
x-bian-sd: <ServiceDomainName>
x-bian-release: "14.0.0"
x-bian-control-record: <ControlRecordName>
x-bian-adoption-level: semantic_alignment | direct_adoption
x-bian-adoption-file: design/{business|domain}/<component>/contract/bian-adoption.yaml
```

**Tags:** usar el nombre del Control Record BIAN (ej. `DisbursementTransaction`) como tag primario — no un nombre genérico de negocio.

**Path parameters:** usar la convención BIAN `{<controlrecordname>id}` (ej. `{disbursementid}`) coincidiendo con el parámetro del baseline.

**OperationIds** — derivar del verbo BIAN + nombre del Control Record:
- Initiate → `initiate<ControlRecord>` (ej. `initiateDisbursementTransaction`)
- Execute  → `execute<ControlRecord>`
- Exchange → `exchange<ControlRecord>`
- Retrieve → `retrieve<ControlRecord>`
- Update   → `update<ControlRecord>`
- Query    → `list<ControlRecord>s`

**Extensiones por operación** — declarar en cada path operation:
```yaml
x-bian-operation: Initiate | Execute | Exchange | Retrieve | Update | Query
x-bian-cr: <ControlRecordName>
```

**Nombres de schemas** — derivar del nombre del Control Record:
- Request body           → `Initiate<ControlRecord>Request`
- Response body          → `<ControlRecord>Response`
- Lista/Query response   → `<ControlRecord>ListResponse`
- Exchange notification  → `<ControlRecord>ExchangeNotification`
- Status enum            → `<ControlRecord>StatusEnum` (valores derivados del lifecycle BIAN)

**Campos de schemas:**
- Nombrar en snake_case adaptado del campo BIAN (ej. `DisbursementProcessReference` → `disbursement_process_ref`).
