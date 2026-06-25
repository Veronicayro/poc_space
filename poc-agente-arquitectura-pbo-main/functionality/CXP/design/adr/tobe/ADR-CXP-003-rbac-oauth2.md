# ADR-CXP-003: RBAC con OAuth2/OIDC para Control de Acceso

**Status:** Accepted  
**Date:** 2026-06-17  
**Functionality:** CXP - Cuentas por Pagar  
**Ref:** ADR-003 del contexto del task

---

## Contexto

El sistema CXP tiene tres actores con permisos distintos: Analista Financiero, Gerente Financiero y Tesorero. Se requiere un mecanismo de autenticación y autorización que garantice que cada actor solo pueda ejecutar las operaciones permitidas por su rol.

## Decisión

Se implementa **OAuth2/OIDC** con **RBAC** (Role-Based Access Control) para autenticación y autorización:

- **Autenticación:** OAuth2 Authorization Code + PKCE (flujo SPA)
- **Proveedor:** Keycloak (o equivalente compatible con OIDC)
- **Token:** JWT Bearer con claims de rol
- **Enforcement:** Middleware RBAC en `accounts-payable-exp-api`
- **Propagación:** Tokens JWT propagados downstream a APIs de negocio

**Roles y permisos:**
| Rol | Permisos |
|---|---|
| ANALYST | create_invoice, view_invoice, edit_invoice |
| MANAGER | approve_invoice, reject_invoice, view_invoice |
| TREASURER | schedule_payment, execute_payment, view_payment_status |

## Justificación

- Estándar de industria para aplicaciones web empresariales
- PKCE previene CSRF y code injection en SPAs
- JWT permite validación stateless (sin consultar DB por request)
- RBAC granular mapea directamente a los actores del sistema CXP
- Keycloak soporta integración con LDAP/AD corporativo

## Alternativas Consideradas

| Alternativa | Razón de descarte |
|---|---|
| API Keys por servicio | No soporta identidad de usuario; no escalable |
| Basic Auth | Inseguro; no estándar para aplicaciones modernas |
| SAML | Más complejo; menos compatible con SPAs |
| Custom JWT | Requiere mantenimiento de infraestructura propia |

## Consecuencias

- **+** Estándar ampliamente adoptado; interoperabilidad
- **+** Stateless validation reduce latencia
- **+** Soporte para MFA, SSO corporativo
- **-** Dependencia de proveedor de identidad externo
- **-** Requiere gestión de refresh tokens en la SPA
- **Restricción:** Los roles ANALYST, MANAGER, TREASURER deben estar configurados en el proveedor OIDC antes del despliegue
- **Restricción:** El token JWT debe incluir el claim `roles` o `realm_access.roles` con los roles asignados
