# Experience API Style Evaluation - Cuentas por Pagar (CXP)

**Phase:** api-architecture  
**Date:** 2026-06-17  
**Evaluated API:** accounts-payable-exp-api

---

## Decisión: REST/JSON (BFF Pattern)

| Criterio | Decisión |
|---|---|
| Estilo | REST |
| Versioning | URI `/v1/` |
| Formato | JSON |
| Auth | OAuth2/OIDC Bearer Token |
| Paginación | Cursor-based |
| Filtrado | Query params |
| Errores | RFC 7807 Problem Details |
| Trazabilidad | `X-Correlation-ID` header |

---

## Evaluación de Alternativas

| Estilo | Evaluación | Decisión |
|---|---|---|
| REST | Estándar del proyecto (DDA-002), React Query/Axios compatible, caché HTTP nativa | ✅ ADOPTADO |
| GraphQL | Overkill para CXP; RBAC por campo más complejo | ❌ NO |
| gRPC | No compatible con navegadores directamente | ❌ NO |

---

## Convenciones REST Aplicadas

**Paths:** recursos en plural, kebab-case. Sin verbos — acciones como sub-recursos.

```
GET    /invoices              → listar
POST   /invoices              → crear
GET    /invoices/{id}         → obtener
PUT    /invoices/{id}         → actualizar (PENDING)
POST   /invoices/{id}/approve → aprobar
POST   /invoices/{id}/reject  → rechazar
POST   /invoices/{id}/cancel  → cancelar
POST   /invoices/{id}/schedule-payment → programar
GET    /payments              → listar pagos
GET    /payments/{id}         → detalle pago
```

**Códigos HTTP:**
- `201` Creación exitosa | `200` Éxito | `204` Sin contenido
- `422` Validación fallida | `409` Duplicado | `403` Sin permiso
- `401` No autenticado | `404` No encontrado | `500` Error interno

**Error format (RFC 7807):**
```json
{
  "type": "https://api.cxp.example.com/errors/DUPLICATE_INVOICE",
  "title": "Factura duplicada",
  "status": 409,
  "detail": "Ya existe una factura con ese número para el proveedor",
  "correlation_id": "uuid"
}
```

**Headers requeridos:**
- `Authorization: Bearer {token}`
- `X-Correlation-ID: {uuid}`
- `Content-Type: application/json`
- `X-Idempotency-Key: {uuid}` (solo en operaciones de pago)
