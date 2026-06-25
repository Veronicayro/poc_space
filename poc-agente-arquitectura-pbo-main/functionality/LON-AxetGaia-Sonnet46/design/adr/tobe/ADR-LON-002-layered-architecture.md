# ADR-LON-002: Arquitectura en Capas con Separación de Responsabilidades

**Status:** Accepted
**Date:** 2026-06-17
**Functionality:** LON — Sistema de Originación de Créditos
**Phase:** api-architecture-decisions / adr-generation

---

## Contexto

La lógica de negocio crediticio es compleja y combina múltiples tipos de responsabilidades:
- **Reglas de dominio:** state machine, políticas de riesgo, umbrales de aprobación
- **Orquestación de integraciones externas:** bureau de crédito, core bancario, DMS
- **Exposición HTTP:** validación de entrada, serialización, seguridad
- **Persistencia:** acceso a base de datos, queries, transacciones

Mezclar estas responsabilidades en un solo componente dificulta el testing, el mantenimiento y la evolución independiente de cada aspecto.

## Decisión

**Arquitectura en capas explícita con separación de servicios por responsabilidad**, implementando el patrón Layered Architecture con las siguientes capas:

```
┌─────────────────────────────────────┐
│   Controller Layer (HTTP)           │  ← Validación entrada, mapeo DTO, HTTP
├─────────────────────────────────────┤
│   Application Service Layer         │  ← Orquestación de casos de uso
├─────────────────────────────────────┤
│   Domain Service Layer              │  ← Reglas de negocio, state machine
├─────────────────────────────────────┤
│   Integration Adapter Layer         │  ← Sistemas externos (bureau, core, DMS)
├─────────────────────────────────────┤
│   Repository Layer                  │  ← Persistencia, PostgreSQL
└─────────────────────────────────────┘
```

### Mapeo de componentes del input.yaml a capas:

| Componente (input.yaml) | Capa Target | API LON |
|-------------------------|-------------|---------|
| SolicitudCreditoController | Controller | credit-request-api (controller) |
| SolicitudCreditoService | Application Service | credit-request-api (service) |
| RiskAssessmentService | Application Service | risk-assessment-api (service) |
| CreditWorkflowService | Domain Service | credit-request-api (domain) |
| DisbursementService | Application/Domain Service | disbursement-api |
| CreditIntegrationAdapter | Integration Adapter | credit-bureau-adapter-api, core-banking-adapter-api, dms-adapter-api |

### Patrones adicionales:
- **DTO / Mapper:** Separación entre modelos de dominio y modelos de API
- **Validation Pipeline:** Validación declarativa en la capa Controller
- **Strategy Pattern:** Políticas de aprobación parametrizables por segmento de crédito (monto, tipo, riesgo)
- **Repository Pattern:** Abstracción de persistencia en la capa inferior

## Consecuencias

**Positivas:**
- Mayor testeabilidad: cada capa puede probarse de forma independiente con mocks
- Facilita evolución independiente de cada capa sin afectar a las demás
- Separación clara de responsabilidades reduce la complejidad cognitiva
- El Strategy Pattern permite modificar políticas de aprobación sin cambios de código
- Compatible con inyección de dependencias (DI) para facilitar testing

**Negativas:**
- Complejidad inicial de estructura de proyecto (más clases/archivos)
- Overhead de mapeo DTO entre capas
- Riesgo de "anemic domain model" si la lógica de negocio migra a la capa de servicio

## Alternativas Consideradas

| Alternativa | Razón de Rechazo |
|-------------|-----------------|
| Hexagonal Architecture (Ports & Adapters) | Mayor complejidad conceptual; el equipo tiene mayor familiaridad con Layered |
| CQRS + Event Sourcing | Overhead arquitectónico excesivo para el scope actual; podría considerarse en v2 |
| Monolito sin capas | No permite testing independiente; dificulta evolución del sistema |

## Referencias

- Source: `functionality/LON-AxetGaia-Sonnet46/input.yaml` → ADR-002, DDA-002
- Patterns: Fowler - Patterns of Enterprise Application Architecture
- BIAN: Layered service domain architecture principle
