# ADR-LON-001: Uso de PostgreSQL como Base de Datos Principal

**Status:** Accepted
**Date:** 2026-06-17
**Functionality:** LON — Sistema de Originación de Créditos
**Phase:** api-architecture-decisions / adr-generation

---

## Contexto

El proceso de originación de crédito requiere consistencia transaccional fuerte. Una solicitud no puede estar en dos estados simultáneamente, y las evaluaciones de riesgo deben ser atómicas con los cambios de estado. El sistema maneja 12 estados de workflow con transiciones controladas por múltiples actores.

Los datos críticos del sistema incluyen:
- Solicitudes de crédito con sus estados (inmutabilidad requerida post-decisión)
- Evaluaciones de riesgo vinculadas a solicitudes
- Decisiones crediticias con trazabilidad completa
- Registros de desembolso con referencias del core bancario
- Audit logs inmutables para cumplimiento ISO 27001 / Basel III

## Decisión

**Base de datos relacional PostgreSQL con ACID compliance.**

Se implementará un único schema PostgreSQL para el dominio LON con las siguientes características:
- **Transacciones ACID** para cambios de estado y decisiones crediticias
- **Integridad referencial** vía foreign keys entre entidades relacionadas
- **Particionamiento por año** en la tabla `credit_requests` para escalabilidad histórica
- **Row-Level Security (RLS)** para control de acceso a nivel de datos
- **Audit trail tables** inmutables (append-only) para `audit_logs`
- **Índices compuestos** en `(status, created_at)`, `(customer_id, status)`, `(assigned_officer_id, status)`

## Consecuencias

**Positivas:**
- Fuerte integridad referencial entre solicitudes, evaluaciones y desembolsos
- Soporte nativo de transacciones serializables para cambios de estado atómicos
- Madurez y soporte empresarial probado en entornos bancarios
- Cumplimiento de retención de datos (7 años) con particionamiento nativo
- Soporte para JSON/JSONB para el campo `metadata` de AuditLog sin overhead NoSQL

**Negativas:**
- Menor flexibilidad que NoSQL para esquemas dinámicos de documentos
- Particionamiento por año requerido desde el inicio para evitar migración futura
- Requiere gestión de conexiones con connection pooling (PgBouncer recomendado)

## Alternativas Consideradas

| Alternativa | Razón de Rechazo |
|-------------|-----------------|
| MongoDB | Sin ACID nativo para transacciones multi-documento en versiones anteriores; riesgo de inconsistencia en cambios de estado |
| MySQL | Menor soporte para funciones avanzadas de auditoría y particionamiento |
| CockroachDB | Overhead distribuido innecesario; LON no requiere distribución geográfica |

## Implementación

```sql
-- Ejemplo de transacción atómica para cambio de estado
BEGIN;
  UPDATE credit_requests 
    SET status = 'APPROVED', updated_at = NOW() 
    WHERE id = $1 AND status = 'PENDING_APPROVAL';
  
  INSERT INTO audit_logs (entity, entity_id, action, previous_state, new_state, actor_id, actor_role, timestamp)
    VALUES ('credit_request', $1, 'STATUS_CHANGE', 'PENDING_APPROVAL', 'APPROVED', $2, 'CREDIT_MANAGER', NOW());
COMMIT;
```

## Referencias

- Source: `functionality/LON-AxetGaia-Sonnet46/input.yaml` → ADR-001
- BIAN: CustomerOffer lifecycle state management requirements
