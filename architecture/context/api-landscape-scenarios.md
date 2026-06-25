# API Landscape — Escenarios de Referencia

> Inventario → `api-landscape-inventory.yaml` · Diagramas → `api-landscape-diagram.md`

---

## Escenario A — Las 4 capas participan

> _Consultar detalle de cuenta corriente con movimientos recientes_

| Capa | API | Acción |
|------|-----|--------|
| experience | `pbco-bmo-api-experience-account-detail` | 🔴 crear |
| business | `AccountManagementAPI v1.3` | 🟡 extender — añadir `GET /accounts/{id}/summary` |
| domain | `AccountManagementAPI v1.3` · CurrentAccount | 🟡 extender — añadir `GET /current-accounts/{crRef}/retrieve` |
| domain | `AccountTransactionsAPI v2.1` · PositionKeeping | 🟢 reutilizar |
| support | `pbco-adp-core-accounts` | 🟢 reutilizar |

---

## Escenario B — Business y Support no aplican

> _Consultar tipo de cambio FX para mostrar en pantalla_

| Capa | API | Acción |
|------|-----|--------|
| experience | `pbco-bmo-api-experience-fx-rates` | 🔴 crear |
| business | — | ⬜ no aplica — consulta directa a un solo dominio |
| domain | `FXRatesAPI v1.4` | 🟢 reutilizar |
| support | — | ⬜ no aplica — proveedor cloud, sin legado |

---

## Escenario C — GAP total, todo se crea

> _Configurar pagos programados / recurrentes_

| Capa | API | Acción |
|------|-----|--------|
| experience | `pbco-bmo-api-experience-standing-orders` | 🔴 crear |
| business | `pbco-bmo-api-business-standing-order-mgmt` | 🔴 crear |
| domain | `pbco-api-domain-standingorder` | 🔴 crear — derivar de BIAN R14 StandingOrder |
| domain | `PaymentLimitsAPI v1.0` | 🟢 reutilizar — dependencia de validación |
| support | `pbco-adp-core-payments-scheduler` | 🔴 crear |

---

## Escenario D — Reutilización total

> _Consultar estado y límite de tarjeta de crédito_

| Capa | API | Acción |
|------|-----|--------|
| experience | `CardManagementAPI v1.5` | 🟢 reutilizar |
| business | `CardManagementAPI v1.5` | 🟢 reutilizar ¹ |
| domain | `CardManagementAPI v1.5` | 🟢 reutilizar ¹ |
| support | — | ⬜ no aplica — procesador externo, sin legado |

> ¹ Una sola API puede cubrir experience + business + domain cuando tiene cobertura completa del estándar BIAN. Las capas divergen en APIs distintas cuando la cobertura es parcial (ver Escenario A).

---

## Cuándo una capa no aplica

| Capa | No aplica cuando… |
|------|-------------------|
| business | La funcionalidad consulta un solo dominio sin orquestación |
| support | El sistema externo es cloud / SaaS sin legado on-prem |

---

## Selección de escenario

```
¿El banco ya tiene APIs que cubren esto?
├── Sí, cubren todo    →  D  reutilizar todo
├── Sí, cubren parte   →  ¿1 dominio simple?  →  B
│                          ¿varios dominios?   →  A  extender lo que falta
└── No existe nada     →  C  crear todo
