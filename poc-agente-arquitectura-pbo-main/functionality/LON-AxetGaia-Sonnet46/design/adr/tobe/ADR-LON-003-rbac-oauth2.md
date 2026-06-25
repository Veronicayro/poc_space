# ADR-LON-003: RBAC con OAuth2 / OpenID Connect

**Status:** Accepted
**Date:** 2026-06-17
**Functionality:** LON — Sistema de Originación de Créditos
**Phase:** api-architecture-decisions / adr-generation

---

## Contexto

El sistema LON involucra 5 actores con permisos distintos y niveles de atribución diferenciados. El control de acceso debe ser:
- **Granular:** cada rol tiene un conjunto específico de operaciones permitidas
- **Auditable:** cada acción debe registrar el actor y su rol para trazabilidad
- **Estándar bancario:** alineado con regulaciones de seguridad (ISO 27001)
- **Escalable:** nuevos roles o cambios de permisos sin redespliegue de código

Las operaciones sensibles como `approve_credit_request` y `execute_disbursement` deben estar protegidas con control estricto; un error de autorización podría comprometer el proceso crediticio.

## Decisión

**Role-Based Access Control (RBAC) con tokens JWT emitidos por Identity Provider corporativo, usando OAuth2 / OpenID Connect.**

### Roles definidos:

| Rol (claim) | Actor | Operaciones críticas |
|-------------|-------|---------------------|
| `CREDIT_OFFICER` | Oficial de Crédito | create, edit, submit, upload_documents |
| `RISK_ANALYST` | Analista de Riesgo | submit_risk_assessment, view_bureau_report |
| `CREDIT_MANAGER` | Gerente de Créditos | approve, reject, escalate_to_committee |
| `CREDIT_COMMITTEE` | Comité de Créditos | approve, reject, add_conditions |
| `DISBURSEMENT_OFFICER` | Oficial de Desembolso | execute_disbursement, confirm_disbursement |

### Implementación:

```yaml
# JWT claims structure
{
  "sub": "user-uuid",
  "roles": ["CREDIT_MANAGER"],
  "permissions": ["approve_credit_request", "reject_credit_request", "view_risk_assessment"],
  "exp": <short-lived>,
  "iss": "https://idp.bank.com",
  "aud": "lon-api"
}
```

### Flujo de autenticación:
1. Usuario se autentica en el Identity Provider corporativo (IdP)
2. IdP emite JWT con roles y claims
3. Frontend incluye JWT en `Authorization: Bearer <token>` en cada request
4. El BFF (`credit-origination-exp-api`) valida el JWT y aplica filtros RBAC
5. Las APIs downstream verifican el token en requests inter-servicio (service-to-service OAuth2)

### Configuración de scopes OAuth2:
```
credit:read       — Consultar solicitudes (todos los roles)
credit:write      — Crear/editar solicitudes (CREDIT_OFFICER)
credit:approve    — Aprobar/rechazar (CREDIT_MANAGER, CREDIT_COMMITTEE)
risk:read         — Ver evaluación de riesgo
risk:write        — Registrar evaluación (RISK_ANALYST)
disbursement:execute — Ejecutar desembolso (DISBURSEMENT_OFFICER)
```

## Consecuencias

**Positivas:**
- Seguridad reforzada con tokens de corta duración (recomendado: 15 minutos + refresh)
- Separación clara entre autenticación (IdP) y autorización (LON)
- Auditoría de todas las acciones con actor y rol registrados automáticamente
- Escalable: cambios de roles gestionados centralmente en el IdP
- Compatible con GDPR: identidad del decisor crediticio trazable

**Negativas:**
- Necesidad de integración con Identity Provider corporativo (dependencia externa)
- Gestión centralizada de roles requiere coordinación con equipo de IAM
- Tokens expirados requieren mecanismo de refresh (UX impact en sesiones largas)

## Alternativas Consideradas

| Alternativa | Razón de Rechazo |
|-------------|-----------------|
| API Keys por rol | No auditable a nivel de usuario; no estándar bancario |
| LDAP directo | Sin estándar moderno de tokens; difícil de usar en SPAs |
| mTLS | Válido para service-to-service pero no para usuarios de frontend |

## Notas de Seguridad Adicionales

- **Enmascaramiento en logs:** NID (número de identificación) y datos bancarios enmascarados
- **TLS 1.2+** obligatorio en todos los endpoints
- **AES-256** para datos sensibles en reposo (claves manejadas por KMS)
- **Consentimiento del cliente:** Registro explícito antes de consulta al bureau de crédito

## Referencias

- Source: `functionality/LON-AxetGaia-Sonnet46/input.yaml` → ADR-003
- Standard: OAuth2 RFC 6749, OpenID Connect Core 1.0
- Compliance: ISO 27001, Basel III, GDPR/regulación local
