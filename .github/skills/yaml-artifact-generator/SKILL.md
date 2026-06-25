# Skill — yaml-artifact-generator

## Propósito

Evitar errores de sintaxis YAML causados por patrones frecuentes en modelos pequeños/medianos. Basado en errores reales observados (`Unexpected scalar at node end`, `Map keys must be unique`).

---

## Error 1 — Texto libre fuera de comillas en valores de lista

El error `Unexpected scalar at node end` ocurre cuando hay texto sin comillas **después** de un valor ya cerrado.

```yaml
# ❌ ROMPE — texto suelto después del string
producedOutputs:
  - "design/api-landscape.yaml" DRAFT, action decisions pending Phase 4
  - "design/existing-component-impact.yaml" (UPDATED 2026-06-25)

# ✅ CORRECTO — todo dentro de comillas
producedOutputs:
  - "design/api-landscape.yaml (DRAFT - action decisions pending Phase 4)"
  - "design/existing-component-impact.yaml (UPDATED 2026-06-25)"
```

**Regla:** Si necesitas añadir anotaciones, sufijos o fechas a un string, inclúyelos **dentro** de las comillas.

---

## Error 2 — Claves duplicadas en el mismo objeto o lista

El error `Map keys must be unique` ocurre cuando la misma clave aparece más de una vez al mismo nivel de indentación.

```yaml
# ❌ ROMPE — "phase: Phase 6" duplicado en la misma lista
sequence:
  - phase: "Phase 6"
    status: "IN_PROGRESS"
  - phase: "Phase 6"        # DUPLICADO
    status: "COMPLETED"

# ✅ CORRECTO — añadir discriminador o consolidar
sequence:
  - phase: "Phase 6"
    iteration: 1
    status: "IN_PROGRESS"
  - phase: "Phase 6"
    iteration: 2
    status: "COMPLETED"
```

**Regla:** En listas de objetos con claves que se repiten, añadir otra clave que diferencie los items, o consolidarlos en un solo objeto con historial.

---

## Error 3 — Strings con paréntesis, comas o dos puntos sin comillas

```yaml
# ❌ ROMPE
notes: Phase 4 COMPLETE. Phase 5 is unblocked (all gates passed).
rationale: Consulta el buro de credito: retorna score y decision

# ✅ CORRECTO
notes: "Phase 4 COMPLETE. Phase 5 is unblocked (all gates passed)."
rationale: "Consulta el buro de credito: retorna score y decision"

# ✅ También válido para textos largos
notes: >
  Phase 4 COMPLETE. Phase 5 is unblocked (all gates passed).
```

**Regla:** Cualquier valor con `:`, `(`, `)`, `,`, `#`, `{`, `}` debe ir entre comillas dobles o en bloque `>` / `|`.

---

## Error 4 — Emojis y caracteres especiales en strings de lista

```yaml
# ❌ PUEDE ROMPER en algunos parsers
validationStatus:
  - ✅ CreditApplicationAPI collision resolved

# ✅ SEGURO — entre comillas
validationStatus:
  - "✅ CreditApplicationAPI collision resolved"
```

**Regla:** Los strings con emojis o símbolos especiales (✅, 🔴, ⚠️) deben ir siempre entre comillas dobles.

---

## Error 5 — Versiones y números de release sin comillas

```yaml
# ❌ AMBIGUO — 1.0 se parsea como número flotante; 14.0.0 no es número válido
schema_version: 1.0
bian_release: 14.0.0

# ✅ CORRECTO
schema_version: "1.0"
bian_release: "14.0.0"
```

---

## Error 6 — Listas con un solo elemento como string plano

```yaml
# ❌ ROMPE
consumers: MobileApp

# ✅ CORRECTO
consumers:
  - MobileApp
```

---

## Checklist rápida antes de escribir cualquier bloque YAML

- [ ] ¿Hay texto suelto después de un string entre comillas? → Moverlo dentro de las comillas
- [ ] ¿Hay claves duplicadas en el mismo nivel? → Añadir discriminador o consolidar
- [ ] ¿Hay strings con `:`, `(`, `,`, emojis sin comillas? → Envolver en `"..."`
- [ ] ¿Las versiones numéricas están entre comillas (`"1.0"`, `"14.0.0"`)? → Sí
- [ ] ¿Las listas de un elemento usan `- valor`, no `valor` directamente? → Sí
- [ ] ¿La indentación usa exactamente 2 espacios por nivel? → Sin tabs
