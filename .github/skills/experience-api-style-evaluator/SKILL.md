# Skill: Experience API Style Evaluator

## Goal

Decide whether each Experience API should use REST, GraphQL, or both.

## Inputs

- `design/api-landscape.yaml`
- `design/semantic-dictionary.yaml`

## Output

Write:

```text
design/experience-api-style-evaluation.md
```

## Required content per Experience API

- experience_api_name
- candidate_styles: REST, GraphQL, both
- selected_style
- rationale
- query_shape_dynamics
- composition_needs
- caching_implications
- governance_implications
- notes

## Rules

- Prefer REST for stable operation-centric interactions and standard API governance.
- Consider GraphQL for dynamic UI projection, composition-heavy journeys, or material over-fetching/under-fetching.
- Do not choose both without explicit justification.
