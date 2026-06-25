# ADR-LON-004: Máquina de Estados Explícita para el Ciclo de Vida de Solicitudes

**Status:** Accepted
**Date:** 2026-06-17
**Functionality:** LON — Sistema de Originación de Créditos
**Phase:** api-architecture-decisions / adr-generation

---

## Contexto

El proceso de originación de crédito tiene **12 estados posibles** y transiciones controladas por:
- **Rol del actor:** Solo actores con el rol adecuado pueden ejecutar ciertas transiciones
- **Estado actual:** Solo ciertas transiciones son válidas desde cada estado
- **Nivel de atribución:** El monto del crédito determina si va al gerente o al comité
- **Score de riesgo:** Un score bajo puede bloquear o redirigir el flujo

Sin una state machine explícita, la lógica de transición se dispersa en múltiples servicios y endpoints, creando inconsistencias y dificultando la auditoría del proceso crediticio.

## Decisión

**Implementar una state machine centralizada en `CreditWorkflowService` (dentro de `credit-request-api`) con tabla de transiciones permitidas parametrizable.**

### Estados del workflow:

```
DRAFT → SUBMITTED → UNDER_REVIEW → RISK_ASSESSED → PENDING_APPROVAL
                                                          ↓           ↓
                                                       APPROVED   PENDING_COMMITTEE
                                                          ↓              ↓
                                              PENDING_DISBURSEMENT    APPROVED/REJECTED
                                                          ↓
                                                       DISBURSED

Terminales: REJECTED, CANCELLED, EXPIRED, DISBURSED
```

### Tabla de transiciones (fuente de verdad):

| From | To | Actor Requerido | Condición Adicional |
|------|----|----------------|---------------------|
| DRAFT | SUBMITTED | CREDIT_OFFICER | docs_obligatorios_completos = true |
| SUBMITTED | UNDER_REVIEW | RISK_ANALYST | - |
| UNDER_REVIEW | RISK_ASSESSED | RISK_ANALYST | score registrado |
| RISK_ASSESSED | PENDING_APPROVAL | system (auto) | - |
| PENDING_APPROVAL | APPROVED | CREDIT_MANAGER | monto <= limite_atribución |
| PENDING_APPROVAL | PENDING_COMMITTEE | CREDIT_MANAGER | monto > limite_atribución OR riesgo = HIGH/CRITICAL |
| PENDING_COMMITTEE | APPROVED | CREDIT_COMMITTEE | - |
| PENDING_APPROVAL | REJECTED | CREDIT_MANAGER | motivo_rechazo required |
| PENDING_COMMITTEE | REJECTED | CREDIT_COMMITTEE | motivo_rechazo required |
| APPROVED | PENDING_DISBURSEMENT | system (auto) | - |
| PENDING_DISBURSEMENT | DISBURSED | DISBURSEMENT_OFFICER | confirmación core bancario |
| ANY | CANCELLED | CREDIT_OFFICER | solo desde DRAFT |
| SUBMITTED | EXPIRED | system (scheduler) | > 48h sin evaluación |

### Implementación:

```python
# Pseudocódigo — CreditWorkflowService
class CreditWorkflowService:
    ALLOWED_TRANSITIONS = {
        ("DRAFT", "SUBMITTED"): [
            Condition(actor_role="CREDIT_OFFICER"),
            Condition(docs_complete=True)
        ],
        ("PENDING_APPROVAL", "APPROVED"): [
            Condition(actor_role="CREDIT_MANAGER"),
            Condition(amount_within_limit=True)
        ],
        # ...
    }
    
    def transition(self, credit_request, to_state, actor):
        key = (credit_request.status, to_state)
        if key not in self.ALLOWED_TRANSITIONS:
            raise InvalidTransitionError(...)
        
        self.validate_conditions(key, credit_request, actor)
        credit_request.status = to_state
        self.audit_log.record(credit_request, to_state, actor)
```

### Cada transición registra en AuditLog:
- `actor_id`, `actor_role`
- `previous_state`, `new_state`
- `timestamp`
- `metadata` (condiciones de aprobación, motivo de rechazo, etc.)

## Consecuencias

**Positivas:**
- Centralización de lógica de transición — una única fuente de verdad
- Prevención de transiciones inválidas a nivel de dominio (no solo validación HTTP)
- Trazabilidad completa del proceso crediticio para auditoría regulatoria
- Facilita alertas automáticas: solicitudes en SUBMITTED > 48h sin evaluación
- Escalado automático basado en umbrales parametrizables (sin cambios de código)
- Tabla de transiciones almacenable como configuración externalizable

**Negativas:**
- Complejidad adicional en pruebas: cobertura de todos los estados y transiciones
- Cuidado con race conditions en transiciones concurrentes (mitigado por ACID PostgreSQL)
- Tabla de transiciones debe versionarse y auditarse ante cambios de política

## Alternativas Consideradas

| Alternativa | Razón de Rechazo |
|-------------|-----------------|
| Lógica de transición distribuida en cada servicio | Inconsistencias, difícil de auditar, riesgo de transiciones inválidas |
| Workflow engine externo (Camunda, Temporal) | Overhead infraestructural; el scope no justifica un workflow engine completo |
| Flags booleanos de estado | No escala para 12 estados; no previene transiciones inválidas |

## Referencias

- Source: `functionality/LON-AxetGaia-Sonnet46/input.yaml` → ADR-004, DDA-001
- BIAN: CustomerOffer CR lifecycle state management
- Pattern: State Machine / Finite State Automaton
