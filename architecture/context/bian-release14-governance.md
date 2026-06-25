# BIAN Release 14 Governance Context

## Baseline rule

BIAN Release 14 is the only allowed BIAN version for this workflow.

## Source rule

Business and Domain Service Domains must be selected only from `design/bian/bian-release14-source-index.yaml`.

## Contract derivation rule

Business and Domain API contracts must be derived from inspected BIAN Release 14 OAS3 or AsyncAPI baseline bodies.

## Blocking conditions

Block Business and Domain API contract generation when:

- the BIAN source index is missing;
- the selected Service Domain is absent from the index;
- the selected baseline body cannot be read;
- no acceptable Service Domain fit exists;
- source file references are missing from `contract/bian-adoption.yaml`.

## Alignment types

- `direct`: selected BIAN Service Domain and operations match the use case closely.
- `adapted`: BIAN semantics fit but target contract narrows or adjusts the operation shape.
- `partial`: BIAN provides partial semantic coverage; gaps require review.
- `unresolved`: no reliable fit can be established.
