# Gaps and Assumptions — LON (Sistema de Originación de Créditos)
<!-- Derived from input.yaml – DDA, NFR, External Systems sections -->

## Gaps identificados

### GAP-LON-001: Contrato API del Bureau de Crédito no especificado
- **Descripción:** El input.yaml define la integración con el bureau de crédito (Equifax/TransUnion/Experian) como REST API síncrona, pero no especifica el contrato ni el schema del bureau.
- **Impacto:** El diseño del `credit-bureau-integration-api` usará un schema interno adaptado. El contrato real debe confirmarse con el proveedor del bureau.
- **Acción requerida:** Obtener documentación del contrato REST del bureau seleccionado.
- **Severidad:** MEDIUM — no bloquea el diseño interno; impacta la integración.

### GAP-LON-002: Contrato API del Core Bancario no especificado
- **Descripción:** El core bancario (KYC, creación de producto, desembolso) es referenciado como REST API / Batch Sync, pero no se proporciona el contrato del core.
- **Impacto:** El `core-banking-integration-api` usará un schema adaptado basado en las responsabilidades descritas.
- **Acción requerida:** Obtener documentación API del core bancario para: validación KYC, creación de producto crédito, ejecución de desembolso, tabla de amortización.
- **Severidad:** MEDIUM — no bloquea el diseño; impacta la implementación de la capa de integración.

### GAP-LON-003: Umbrales de atribución y score no definidos numéricamente
- **Descripción:** El input.yaml menciona umbrales de monto de atribución del gerente y score mínimo como "configurables", pero no proporciona valores por defecto o rangos.
- **Impacto:** El diseño asumirá que estos umbrales son parámetros externalizables en una tabla de configuración. Los valores exactos son decisión operacional del banco.
- **Acción requerida:** El equipo de negocio debe definir los valores iniciales de configuración.
- **Severidad:** LOW — el diseño soporta la externalización; valores son operacionales.

### GAP-LON-004: Política de notificación al cliente no especificada
- **Descripción:** DisbursementService menciona "notificación al cliente por canal configurado", pero no se especifica qué canales (email, SMS, push notification) ni el sistema de notificaciones.
- **Impacto:** El diseño incluirá un punto de extensión de notificación (event/webhook) pero el canal específico depende del sistema de notificaciones del banco.
- **Acción requerida:** Confirmar si existe un sistema de notificaciones centralizado y su mecanismo de integración.
- **Severidad:** LOW — punto de extensión incluido; implementación depende del canal disponible.

### GAP-LON-005: Identity Provider corporativo no especificado
- **Descripción:** ADR-003 requiere OAuth2/OIDC con Identity Provider corporativo para RBAC, pero el IDP específico no está identificado.
- **Impacto:** El diseño asumirá un IDP estándar compatible con OAuth2/OIDC (Keycloak, Okta, Azure AD, etc.).
- **Acción requerida:** Confirmar el IDP corporativo existente para integración RBAC.
- **Severidad:** LOW — el diseño es agnóstico al proveedor de IDP.

### GAP-LON-006: Figma/UI design no disponible
- **Descripción:** El input.yaml indica `Figma Reference: N/A`. Solo se dispone de notas descriptivas del UI.
- **Impacto:** El diseño de la capa de experiencia se basará en las notas UI del input.yaml.
- **Acción requerida:** No bloqueante para el diseño de APIs.
- **Severidad:** INFO — no afecta el diseño de backend.

### GAP-LON-007: Inventario de sistemas existentes no disponible
- **Descripción:** No existe un inventario de APIs o módulos existentes para LON (no hay sistema previo documentado).
- **Impacto:** Se asume diseño greenfield. El `existing-component-impact.yaml` reflejará impacto nulo de sistemas previos.
- **Acción requerida:** Confirmar si existe algún sistema legado de originación que requiera migración.
- **Severidad:** LOW — asunción de greenfield es conservadora y segura.

---

## Asunciones

| ID | Asunción | Impacto si es incorrecta |
|----|----------|--------------------------|
| ASM-LON-001 | Diseño greenfield: no existen APIs LON previas | Requeriría análisis de impacto de migración |
| ASM-LON-002 | El Core Bancario expone REST API para KYC y desembolso | Requeriría adaptar la capa de integración |
| ASM-LON-003 | Redis estará disponible como infraestructura de caché | Requeriría alternativa de caché (in-memory, Memcached) |
| ASM-LON-004 | PostgreSQL es la base de datos seleccionada (confirmado en ADR-001) | No aplica — decisión confirmada |
| ASM-LON-005 | Los bureaus de crédito soportan REST API (no SOAP/legacy) | Requeriría adaptador adicional para SOAP |
| ASM-LON-006 | Un solo servicio de bureau por instancia (aunque puede cambiar por segmento) | Requeriría estrategia multi-bureau |
| ASM-LON-007 | Los documentos del DMS son accesibles por referencia (no se copian al sistema LON) | Requeriría almacenamiento local de documentos |
| ASM-LON-008 | El proceso de aprobación es siempre unipersonal (gerente) o colegiado (comité); no se prevén otros niveles en esta versión | Requeriría extensión de la state machine |
