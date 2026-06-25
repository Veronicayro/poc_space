# Skill — api-landscape-governance

## Goal

Analyze the required BIAN capabilities (identified in Phase 1) against the existing API catalog, autonomously decide for each architectural layer (`reuse | extend | create`), and produce the 3 landscape artifacts without requiring additional user input.

---

## Inputs (whitelist)

| Source | Field key | Purpose |
|--------|-------------|-----------|
| `design/bian/bian-service-domain-evaluation.yaml` | `service_domains[].name`, `service_domains[].operations[]` | BIAN SDs y operaciones requeridas por la funcionalidad |
| `catalog/bian-capability-index.yaml` | `bian_sd_to_capability`, `capabilities[].action`, `gaps[]` | Cobertura de cada SD en el catálogo actual |
| `architecture/context/api-landscape-inventory.yaml` | `layers.experience`, `layers.business`, `layers.domain`, `layers.support` | APIs existentes por capa con endpoints reutilizables/extensibles |
| `functionality/<ID>/discovery/integration-inventory.yaml` | `integrations[].adapter_name`, `integrations[].operations[]` | Adaptadores de soporte existentes |

---

## Required rules

- These rules is required for design api landscape: `architecture/context/api-architecture-governance.md`

## Proceso de análisis (autónomo — sin input del usuario)

### Paso 1 — Leer BIAN SDs requeridos

Desde `design/bian/bian-service-domain-evaluation.yaml`, extraer:
- Lista de Service Domains requeridos
- Operaciones BIAN necesarias por SD (ej. Retrieve, Initiate, Update)

### Paso 2 — Contrastar por capa

Para cada SD requerido, evaluar cobertura en el catálogo:

**Capa domain:**
- Buscar en `catalog/bian-capability-index.yaml` → sección `bian_sd_to_capability`
- Si existe entrada → leer `capabilities[id].action` del `api-landscape-inventory.yaml`
  - `action: reutilizar` si la cobertura es total para las operaciones requeridas
  - `action: extender` si la cobertura es parcial (faltan endpoints específicos)
  - `action: crear` si el SD no tiene entrada (GAP) → verificar sección `gaps[]`
- Si no existe entrada → `action: crear`

**Capa business:**
- Buscar en `architecture/context/api-landscape-inventory.yaml` → `layers.business`
- Buscar por capacidad o dominio que corresponda a las funcionalidades requeridas
- Determinar si la orquestación requerida ya existe:
  - Múltiples SDs involucrados y reglas de negocio transversales → la capa **aplica**
  - Un solo SD, flujo directo sin reglas complejas → la capa **no aplica**

**Capa experience:**
- Buscar en `architecture/context/api-landscape-inventory.yaml` → `layers.experience`
- Buscar por flujo o caso de uso que corresponda
- Si no existe BFF para este flujo → `action: crear`

**Capa support:**
- Buscar en `functionality/<ID>/discovery/integration-inventory.yaml`
- Si el dominio requiere acceso a sistema legado on-prem → la capa **aplica**
- Si la integración es con proveedor cloud externo y el Domain API lo gestiona directamente → la capa **no aplica**

### Paso 3 — Inferir el patrón del landscape

Con base en el análisis de los pasos anteriores, el skill infiere el patrón que mejor describe el resultado. El patrón es descriptivo — no prescriptivo. El skill debe elegir el más cercano al resultado real del análisis, o describir una combinación si ninguno aplica exactamente.

Referencias canónicas de patrones: `architecture/context/api-landscape-scenarios.md`

### Paso 4 — Generar los 3 artefactos

---

## Artefacto 1 — `design/api-landscape.yaml`

Schema: `architecture/schemas/api-landscape.schema.yaml` v2.0

```yaml
schema_version: "2.0"
functionality_id: <ID>
scenario: <patrón inferido en Paso 3>

layers:
  experience:
    apis:
      - api_name: <nombre>
        action: reutilizar | extender | crear
        catalog_ref: <ruta al catálogo> | null
        pattern: <BFF | ...>
        consumers: [<canal>]
        calls_to: [<api en capa business o domain>]
    # Si no aplica:
    # applicable: false
    # reason: <razón concisa>

  business:
    apis:
      - api_name: <nombre>
        action: reutilizar | extender | crear
        catalog_ref: <ruta> | null
        new_endpoints: [<endpoint>]   # solo si action=extender
        calls_to: [<api en capa domain>]

  domain:
    apis:
      - api_name: <nombre>
        action: reutilizar | extender | crear
        catalog_ref: <ruta> | null
        bian_sd: <ServiceDomain>
        bian_operation: <operación BIAN>
        new_endpoints: [<endpoint>]   # solo si action=extender
        calls_to: [<api en capa support>]

  support:
    apis:
      - api_name: <nombre>
        action: reutilizar | crear
        pattern: Adapter/ACL
        target_system: <sistema>
        legacy_operations: [<operación>]
```

**Reglas obligatorias:**
- `action` debe derivar del análisis del Paso 2 — nunca hardcoded
- `catalog_ref` requerido cuando `action=reutilizar` o `action=extender`
- `catalog_ref: null` cuando `action=crear`
- Capa con `applicable: false` no debe tener campo `apis`
- `bian_sd` y `bian_operation` solo en capa `domain`

---

## Artefacto 2 — `design/diagrams/api-landscape-diagram.md`

Diagrama Mermaid que representa visualmente el landscape de esta funcionalidad.

**Reglas:**
- Incluir solo las capas donde `applicable != false`
- Cada nodo muestra el nombre de la API y el emoji de su acción:
  - 🟢 `reutilizar`
  - 🟡 `extender`
  - 🔴 `crear`
- Las conexiones entre capas deben reflejar el campo `calls_to` del `api-landscape.yaml`
- El nodo raíz es el usuario/canal o el sistema disparador del flujo
- El nodo hoja es el sistema core o proveedor externo

**Plantilla base:**
```markdown
# API Landscape — <nombre de la funcionalidad>
<!-- Escenario: <patrón inferido> -->

```mermaid
flowchart TD
  [nodo de origen]
  [capas activas con sus APIs]
  [sistema destino]
  [conexiones derivadas de calls_to]
```

**Leyenda:** 🟢 reutilizar · 🟡 extender · 🔴 crear
```

---

## Artefacto 3 — `design/diagrams/api-landscape-inventory-delta.md`

Tabla comparativa que evidencia qué existe en el catálogo y qué es nuevo.

**Reglas:**
- Una fila por API en cada capa activa
- `Estado: existente` cuando `catalog_ref != null`
- `Estado: nueva` cuando `catalog_ref == null`
- Columna `Endpoint / Cambio` resume la operación reutilizada, el endpoint nuevo propuesto, o el nombre de la API nueva

**Plantilla:**
```markdown
# Delta de Inventario — <nombre de la funcionalidad>
<!-- Escenario: <patrón inferido> -->

| Capa | API | Estado | Acción | Endpoint / Cambio |
|------|-----|--------|--------|-------------------|
| <capa> | <api_name> | existente | 🟢 reutilizar | <endpoint existente> |
| <capa> | <api_name> | existente | 🟡 extender  | + <nuevo endpoint> |
| <capa> | <api_name> | nueva     | 🔴 crear     | <nombre nuevo API> |
```

---

## Reglas de gobernanza (hard rules)

1. **NUNCA crear** una nueva API si una existente puede reutilizarse o extenderse.
2. **SIEMPRE contrastar** contra el catálogo antes de decidir `crear`.
3. Cuando `action=extender`: proponer cambios backward-compatible. Si no es posible → recomendar nueva versión de la misma API (no nueva API diferente).
4. Cuando `action=crear`: el nombre debe seguir la convención: `pbco-{tipo}-api-{dominio}-{recurso}`.
5. El campo `scenario` en el YAML es descriptivo — el modelo lo infiere del análisis, no lo selecciona de una lista fija.
6. Las capas que no aplican deben documentarse explícitamente (`applicable: false + reason`), no omitirse silenciosamente.
