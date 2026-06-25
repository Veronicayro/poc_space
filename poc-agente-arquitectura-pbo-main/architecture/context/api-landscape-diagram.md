# API Landscape — Diagrama por Capas
<!-- Versión: 1.0 | Fecha: 2026-06 -->
<!-- Responsabilidad: visualización del landscape arquitectural por capas -->
<!-- Inventario de APIs: architecture/context/api-landscape-inventory.yaml -->
<!-- Escenarios:         architecture/context/api-landscape-scenarios.md -->

Este diagrama muestra la arquitectura por capas del landscape de APIs del banco,
con las decisiones de reutilización (`R`), extensión (`E`) y creación (`C`)
aplicadas sobre cada componente.

**Leyenda de decisiones:**
- 🟢 `R` = Reutilizar — existe en catálogo, cubre el caso
- 🟡 `E` = Extender — existe pero requiere nuevo endpoint backward-compatible
- 🔴 `C` = Crear — GAP confirmado, no existe en catálogo
- ⬜ `N/A` = La capa no aplica para este flujo

---

## Diagrama completo del landscape (todas las APIs del catálogo)

```mermaid
flowchart TD

  subgraph EXP["🔵 CAPA DE EXPERIENCIA — BFF / Experience APIs"]
    direction LR
    EXP1["ChannelSessionAPI v2.1 🟢R"]
    EXP2["CardManagementAPI v1.5 🟢R"]
    EXP3["CustomerNotificationPreferencesAPI v1.1 🟢R"]
    EXP4["[pbco-bmo-api-experience-{flujo}] 🔴C"]
  end

  subgraph BUS["🟣 CAPA DE NEGOCIO — Business / Process APIs"]
    direction LR
    BUS1["CustomerProfileAPI v1.2 🟢R"]
    BUS2["CustomerIdentityAPI v1.1 🟢R"]
    BUS3["AccountManagementAPI v1.3 🟡E"]
    BUS4["PaymentsProcessingAPI v2.4 🟢R ⚠OVL-001"]
    BUS5["InstantTransfersAPI v1.6 🟢R ⚠OVL-001"]
    BUS6["LoanServicingAPI v2.2 🟢R"]
    BUS7["CreditApplicationAPI v1.3 🟡E"]
    BUS8["NotificationDispatchAPI v1.7 🟢R"]
    BUS9["[pbco-bmo-api-business-{capacidad}] 🔴C"]
  end

  subgraph DOM["🟠 CAPA DE DOMINIO — Domain APIs / BIAN R14"]
    direction LR
    DOM1["AccountTransactionsAPI v2.1 🟢R\nPositionKeeping · cov:A"]
    DOM2["AccountManagementAPI v1.3 🟡E\nCurrentAccount · cov:P"]
    DOM3["StatementDeliveryAPI v1.0 🟡E\nCorrespondence · cov:P"]
    DOM4["CardAuthorizationAPI v2.0 🟢R\nCardAuthorization · cov:A"]
    DOM5["FXRatesAPI v1.4 🟢R\nCurrencyExchange · cov:P"]
    DOM6["KYCScreeningAPI v3.0 🟢R\nPartyLifecycleManagement · cov:P"]
    DOM7["FraudDecisioningAPI v1.8 🟢R\nFraudEvaluation · cov:A"]
    DOM8["CreditDecisioningAPI v2.0 🟢R\nCustomerCreditRating · cov:A"]
    DOM9["DisbursementAPI v1.1 🟢R\nDisbursement · cov:A"]
    DOMG1["[pbco-api-domain-standingorder] 🔴C\nStandingOrder · GAP-001"]
    DOMG2["[pbco-api-domain-termdeposit] 🔴C\nTermDeposit · GAP-003"]
  end

  subgraph SUP["⚫ CAPA DE SOPORTE — Adaptadores / ACL"]
    direction LR
    SUP1["pbco-adp-core-accounts 🟢R\nCoreBank: ObtenerCuentas, Movimientos"]
    SUP2["pbco-adp-core-payments 🟢R\nCoreBank: ProcesarPago, Revertir"]
    SUP3["pbco-adp-core-loans 🟢R\nCoreBank: Préstamo, Desembolso"]
    SUP4["pbco-adp-notification-gateway 🟢R\nFirebase/SNS: Push, SMS, Email"]
    SUP5["pbco-adp-kyc-provider 🟢R\nKYCProvider: Identity, PEP, Sanctions"]
    SUPG1["[pbco-adp-core-payments-scheduler] 🔴C\nCoreBank: ProgramarPago"]
  end

  subgraph CORE["⬛ CORE / SISTEMAS EXTERNOS"]
    direction LR
    CORE1[("CoreBancario\n(Legado)")]
    CORE2[("NotificationGateway\n(Cloud)")]
    CORE3[("KYCProvider\n(Externo)")]
    CORE4[("CardProcessor\nVisa / MC")]
    CORE5[("FX Market Feed\n(Externo)")]
  end

  EXP --> BUS
  BUS --> DOM
  DOM --> SUP
  SUP --> CORE1
  SUP4 --> CORE2
  SUP5 --> CORE3
  DOM4 -.->|"integración directa"| CORE4
  DOM5 -.->|"integración directa"| CORE5
```

---

## Escenario A — Diagrama: Consultar cuenta + movimientos (4 capas activas)

```mermaid
flowchart TD

  U(["👤 Usuario\nMobileApp / WebApp"])

  subgraph EXP["🔵 EXPERIENCIA"]
    A1["pbco-bmo-api-exp-account-detail 🔴C\n(nueva BFF)"]
  end

  subgraph BUS["🟣 NEGOCIO"]
    B1["AccountManagementAPI v1.3 🟡E\n+ GET /accounts/{id}/summary"]
  end

  subgraph DOM["🟠 DOMINIO"]
    D1["AccountManagementAPI v1.3 🟡E\nCurrentAccount · cov:P\n+ GET /current-accounts/{crRef}/retrieve"]
    D2["AccountTransactionsAPI v2.1 🟢R\nPositionKeeping · cov:A\nGET /accounts/{id}/transactions"]
  end

  subgraph SUP["⚫ SOPORTE"]
    S1["pbco-adp-core-accounts 🟢R\nObtenerCuentas · ObtenerMovimientos"]
  end

  CORE1[("⬛ CoreBancario")]

  U --> A1
  A1 --> B1
  B1 --> D1
  B1 --> D2
  D1 --> S1
  D2 --> S1
  S1 --> CORE1
```

---

## Escenario B — Diagrama: Consulta FX simple (business N/A, support N/A)

```mermaid
flowchart TD

  U(["👤 Usuario\nMobileApp"])

  subgraph EXP["🔵 EXPERIENCIA"]
    A1["pbco-bmo-api-exp-fx-rates 🔴C\n(nueva BFF)"]
  end

  BUS["🟣 NEGOCIO\n⬜ N/A — 1 solo SD, sin orquestación"]

  subgraph DOM["🟠 DOMINIO"]
    D1["FXRatesAPI v1.4 🟢R\nCurrencyExchange · cov:P\nGET /fx-rates/{currencyPair}"]
  end

  SUP["⚫ SOPORTE\n⬜ N/A — integración cloud directa"]

  FEED[("⬛ FX Market Feed\nExterno / Cloud")]

  U --> A1
  A1 -->|"directo"| D1
  D1 -.->|"integración directa"| FEED
```

---

## Escenario C — Diagrama: Standing Orders / GAP total (todo se crea)

```mermaid
flowchart TD

  U(["👤 Usuario\nMobileApp"])

  subgraph EXP["🔵 EXPERIENCIA"]
    A1["pbco-bmo-api-exp-standing-orders 🔴C\n(nueva BFF)"]
  end

  subgraph BUS["🟣 NEGOCIO"]
    B1["pbco-bmo-api-business-standing-order-mgmt 🔴C\n(nueva — orquesta GAP-001)"]
  end

  subgraph DOM["🟠 DOMINIO"]
    D1["pbco-api-domain-standingorder 🔴C\nStandingOrder · GAP-001\nIniciado desde BIAN R14"]
    D2["PaymentLimitsAPI v1.0 🟢R\nCustomerAccessEntitlement · cov:P\n(dependencia existente)"]
  end

  subgraph SUP["⚫ SOPORTE"]
    S1["pbco-adp-core-payments-scheduler 🔴C\n(nuevo adaptador)"]
  end

  CORE1[("⬛ CoreBancario\nScheduler de Pagos")]

  U --> A1
  A1 --> B1
  B1 --> D1
  B1 --> D2
  D1 --> S1
  S1 --> CORE1
```

---

## Escenario D — Diagrama: Consultar tarjeta (reutilización total)

```mermaid
flowchart TD

  U(["👤 Usuario\nMobileApp"])

  subgraph EXP["🔵 EXPERIENCIA"]
    A1["CardManagementAPI v1.5 🟢R\nGET /cards/{id}/status"]
  end

  subgraph BUS["🟣 NEGOCIO"]
    B1["CardManagementAPI v1.5 🟢R\nGET /cards/{id}"]
  end

  subgraph DOM["🟠 DOMINIO"]
    D1["CardManagementAPI v1.5 🟢R\nCreditCard · cov:A\nGET /cards/{crRef}/retrieve"]
  end

  SUP["⚫ SOPORTE\n⬜ N/A — integración directa con procesador"]

  CARD[("⬛ CardProcessor\nVisa / MC")]

  U --> A1
  A1 --> B1
  B1 --> D1
  D1 -.->|"integración directa"| CARD
```

---

## Escenario E — Diagrama: Notificaciones event-driven (experience N/A, domain N/A)

```mermaid
flowchart TD

  EVT(["⚡ Evento Interno\n(PaymentsAPI, LoanAPI, etc.)"])

  EXP["🔵 EXPERIENCIA\n⬜ N/A — no hay usuario iniciador"]

  subgraph BUS["🟣 NEGOCIO"]
    B1["NotificationDispatchAPI v1.7 🟢R\nPOST /notifications/dispatch"]
  end

  DOM["🟠 DOMINIO\n⬜ N/A — cov:N, capacidad propietaria"]

  subgraph SUP["⚫ SOPORTE"]
    S1["pbco-adp-notification-gateway 🟢R\nSendPush · SendSMS · SendEmail"]
  end

  GW[("⬛ NotificationGateway\nFirebase / AWS SNS")]

  EVT --> B1
  B1 --> S1
  S1 --> GW
