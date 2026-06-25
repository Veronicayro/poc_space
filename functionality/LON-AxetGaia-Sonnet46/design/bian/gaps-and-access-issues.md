# BIAN Gaps and Access Issues — LON (Sistema de Originación de Créditos)
<!-- Phase 1 output: bian-service-domain-evaluator skill -->

## Resumen

| Service Domain | Baseline verificado | Tipo de alineación | Gaps críticos |
|----------------|--------------------|--------------------|---------------|
| CustomerOffer | ✅ Sí | adapted (0.92) | State machine 12 estados es extensión LON |
| Underwriting | ✅ Sí | adapted (0.90) | DTI ratio y lógica de comité son extensiones |
| CustomerCreditRating | ✅ Sí | adapted (0.88) | Caché Redis y consentimiento son extensiones |
| Disbursement | ✅ Sí | direct (0.95) | Sin gaps críticos |

**Gate BIAN: PASS** — No hay problemas de acceso a baselines. No hay gaps bloqueantes.

---

## Gaps de alineación BIAN (no bloqueantes)

### BIAN-GAP-LON-001: State machine de 12 estados sin equivalente directo en CustomerOffer
- **Service Domain afectado:** CustomerOffer
- **Descripción:** BIAN CustomerOffer CR define un ciclo de vida simplificado
  (Initiated → Processed → Completed). LON requiere 12 estados detallados
  (DRAFT, SUBMITTED, UNDER_REVIEW, RISK_ASSESSED, PENDING_APPROVAL,
  PENDING_COMMITTEE, APPROVED, REJECTED, PENDING_DISBURSEMENT,
  DISBURSED, CANCELLED, EXPIRED).
- **Decisión:** Extensión de dominio LON documentada. Los estados LON se mapean
  al ciclo de vida del CR de CustomerOffer mediante extensiones. Documentado
  en ADR-004 (state machine explícita).
- **Severidad:** INFO — no bloquea la adopción BIAN; la extensión está justificada.

### BIAN-GAP-LON-002: Escalado a Comité sin equivalente en CustomerOffer/Underwriting
- **Service Domain afectado:** CustomerOffer, Underwriting
- **Descripción:** El escalado automático al Comité de Créditos (PENDING_COMMITTEE)
  y la lógica de atribución multinivel no tienen equivalente en los SD BIAN
  de Release 14.
- **Decisión:** Extensión de dominio LON. Los umbrales de escalado son
  parámetros externalizables (DDA-004). El workflow de comité se implementa
  como extensión del CustomerOffer CR.
- **Severidad:** INFO — extensión justificada por política crediticia del banco.

### BIAN-GAP-LON-003: DTI ratio no definido en Underwriting BIAN
- **Service Domain afectado:** Underwriting
- **Descripción:** BIAN Underwriting no define explícitamente el cálculo de
  DTI (Debt-to-Income) ratio como parte del proceso de evaluación.
- **Decisión:** Extensión de campo en el schema de UnderwritingAssessment.
  El DTI es calculado internamente por LON usando datos del bureau y el
  monto solicitado.
- **Severidad:** INFO — extensión de campo menor; no afecta la estructura del CR.

### BIAN-GAP-LON-004: Política de caché Redis no definida en CustomerCreditRating
- **Service Domain afectado:** CustomerCreditRating
- **Descripción:** BIAN CustomerCreditRating no define mecanismos de caché
  con TTL para los reportes del bureau. Esta es una decisión de implementación
  de LON (DDA-003, ADR-005).
- **Decisión:** Capa de caché Redis (TTL 24h) implementada como infraestructura
  del CreditBureauIntegrationAdapter; transparente para el SD BIAN.
- **Severidad:** INFO — decisión de implementación sin impacto en el contrato BIAN.

### BIAN-GAP-LON-005: Registro de consentimiento bureau no en CustomerCreditRating
- **Service Domain afectado:** CustomerCreditRating
- **Descripción:** El registro del consentimiento del cliente para la consulta
  al bureau (requerimiento GDPR/regulación local) no está definido en el SD BIAN.
- **Decisión:** Campo adicional `bureau_consent_ref` en los schemas de
  CreditRequest y CustomerCreditRating derivados para LON.
- **Severidad:** INFO — extensión de compliance; no contradice el SD BIAN.

---

## Problemas de acceso a baselines BIAN

**No se identificaron problemas de acceso.**

Todos los archivos baseline requeridos están presentes en el caché local:
- ✅ `architecture/cache/bian/release14.0.0/oas3/yamls/CustomerOffer.yaml` (234 KB)
- ✅ `architecture/cache/bian/release14.0.0/oas3/yamls/Underwriting.yaml` (84 KB)
- ✅ `architecture/cache/bian/release14.0.0/oas3/yamls/CustomerCreditRating.yaml` (54 KB)
- ✅ `architecture/cache/bian/release14.0.0/oas3/yamls/Disbursement.yaml` (156 KB)

---

## Conclusión

La alineación BIAN para LON es **VÁLIDA**. Los 4 Service Domains seleccionados
tienen alta cobertura (fit scores: 0.88–0.95) y los gaps identificados son todos
extensiones de dominio documentadas y justificadas, no contradicciones del estándar.

El gate BIAN está **PASS**. Se puede proceder con el diseño de APIs y contratos.
