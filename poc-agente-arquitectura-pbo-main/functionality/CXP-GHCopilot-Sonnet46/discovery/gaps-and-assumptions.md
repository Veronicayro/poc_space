schema_version: "1.0"
functionality_id: CXP-GHCopilot-Sonnet46

gaps: []
assumptions:
  - id: ASS-001
    description: No existe sistema CXP previo; la implementación es net-new.
    impact: low

  - id: ASS-002
    description: El ERP expone una API REST con endpoints para validación de proveedores y registro de asientos.
    impact: medium

  - id: ASS-003
    description: El sistema bancario expone webhooks para confirmación de pagos con capacidad de reintento.
    impact: medium

  - id: ASS-004
    description: La autenticación OAuth2/OIDC ya está disponible como servicio corporativo existente.
    impact: low
