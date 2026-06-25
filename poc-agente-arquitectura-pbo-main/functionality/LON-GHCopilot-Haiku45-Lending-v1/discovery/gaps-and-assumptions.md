# Digital Personal Loan Origination — Gaps & Assumptions

## Gaps

### G-001: KYC Integration Interface
**Description:** No se ha definido cómo se valida o consulta el estado KYC del cliente en el sistema existente.
**Impact:** BR-001 requiere validación de KYC, pero el punto de integración es incierto.
**Resolution:** Se resolverá en Phase 2 (existing-landscape-analyzer) al analizar sistema de KYC existente.

### G-002: Credit Scoring Configuration
**Description:** Los umbrales configurables (BR-004, BR-005) no se han especificado con valores concretos.
**Impact:** Medium — se necesita para implementación, pero son configurables.
**Resolution:** Se definirán en Phase 6 durante el diseño de componentes backend.

### G-003: Regulatory Compliance Details
**Description:** La definición exacta de tasas máximas regulatorias (BR-006) y estándares de firma (BR-009) dependen de jurisdicción.
**Impact:** Critical — impacta decisiones de NFR y compliance.
**Resolution:** Se validará en Phase 5 (security-nfr-observability-designer).

### G-004: Document Types & Validation Rules
**Description:** No se ha especificado qué tipos de documentos se aceptan ni las reglas de validación.
**Impact:** Medium — UC-002 requiere captura de "comprobante de ingresos + documento de identidad", pero formato/validación no especificado.
**Resolution:** Se cubrirá en UC-002 (Carga de documentos) durante Phase 6.

### G-005: Pricing Policy Engine
**Description:** La política de precios (tasas, plazos, cuotas) no se detalla; asume un motor configurable.
**Impact:** High — UC-004 (Generación de oferta) depende de esto.
**Resolution:** Se definirá la integración con ReferenceDataDirectory (BIAN) en Phase 4 y componentes en Phase 6.

### G-006: Core Banking Disbursement Details
**Description:** Detalles exactos de formato de instrucción de desembolso no especificados.
**Impact:** High — UC-007 requiere integración con core.
**Resolution:** Se derivará del análisis del sistema core existente en Phase 2 y se diseñará en Phase 6.

## Assumptions

### A-001: Regulatory Framework
**Assumption:** La jurisdicción es país latinoamericano con regulación similar a Colombia (Superintendencia Financiera).
**Rationale:** Mención de "GDPR/LGPD" sugiere mercado regulado; se asume estándares de conformidad de crédito de consumo.
**Impact:** Shapes security (eIDAS-equivalent signature), compliance rules (BR-006).

### A-002: Default Execution Mode
**Assumption:** `Execution mode override: standard` → se diseñarán interfaces REST synchronous, con async solo para notificaciones (UC-008).
**Rationale:** Scoring + credit decision deben ser responsivos (latencia < 3s per NFR).

### A-003: Technology Stack
**Assumption:** `Technology override: Java` → backend diseñado en Java (Spring Boot o similar).
**Rationale:** Explícitamente provisto por el usuario.

### A-004: Single Functionality Scope
**Assumption:** Esta funcionalidad cubre SOLO origination (solicitud → desembolso), NO servicing (repayment, restructuring, collections).
**Rationale:** Explícitamente en "Out of scope".

### A-005: Customer Authentication
**Assumption:** Clientes digitales ya están autenticados vía sistema de identidad/OAuth2 existente cuando inician UC-001.
**Rationale:** Implícito en "Given: cliente autenticado en canal digital".

### A-006: Offer Expiration Enforcement
**Assumption:** El sistema envía notificación (UC-008) antes de expiración y rechaza aceptación post-72h automáticamente.
**Rationale:** BR-007 requiere expiración; mecanismo asumido es webhook + scheduled task.

### A-007: Manual Review SLA
**Assumption:** Los casos REFERRED (BR-005, UC-006) se revisan dentro de 4-8 horas hábiles.
**Rationale:** No especificado en los requisitos; se asume para operación realista.

### A-008: Document Storage Encryption
**Assumption:** DOCUMENT_STORAGE ya tiene cifrado en reposo (cumple BR-012); componente confía en su conformidad.
**Rationale:** Requisito de compliance ya asumido en external system.

### A-009: Audit Log Availability
**Assumption:** Audit & Compliance Log system (INT-002) es de alto rendimiento y siempre disponible.
**Rationale:** BR-010 es CRITICAL; no hay fallback definido.

### A-010: Catalog Collision Resolution
**Assumption:** `CreditApplicationAPI v1.3` existente será evaluado en Phase 4 para determinar REUSE/EXTEND.
**Rationale:** COLLISION_DETECTED; será resuelto por api-landscape-governance skill.

---

## Notes

- Todas las integraciones externas críticas (CREDIT_BUREAU, SCORING_ENGINE, CORE_BANKING, DIGITAL_SIGNATURE_PROVIDER) asumen **high availability y bajo latency** (~100ms SLA).
- BR-003 (obligatoria consulta a buró) y BR-009 (firma electrónica) requieren integración **sin fallback**, lo que implica una arquitectura con **circuit breaker y retry logic** pero sin degradation automática.
- Las notificaciones (UC-008, EXT-005) son **async best-effort**; no bloquean la progresión de estados.
