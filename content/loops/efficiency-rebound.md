---
title: "Efficiency rebound"
description: "Efficiency gains make each unit of computing cheaper, which can raise total demand enough to grow total energy use."
maturity: seedling
loop_type: "R (reinforcing)"
owner: ""
drafted_by: "agent: Claude"
verified_by: ""
tags: [loop]
---

Efficiency gains make each unit of computing cheaper, which can raise total demand enough to grow total energy use.

**Loop type:** R (reinforcing)

```mermaid
flowchart LR
  E[Hardware and software efficiency] -->|"−"| C[Cost per unit of compute]
  C -->|"−"| D[Demand for compute]
  D -->|"+"| T[Total electricity use]
  D -->|"+"| I[Investment in new capacity]
  I -->|"+"| E
```

Read "+" as "more of A leads to more of B" and "−" as "more of A leads to less of B". Every arrow needs a source before this note becomes 🌿 budding.

## Connected notes

- [[branches/data-operations]]
- [[branches/economics]]
- [[components/servers]]

## Evidence so far

- Masanet et al. (2020) show efficiency held global energy growth down for years ([Science](https://eta-publications.lbl.gov/publications/recalibrating-global-data-center)).
- Bashir et al. (2024) argue a siloed focus on efficiency leads instead to increased adoption ([MIT](https://impactclimate.mit.edu/2024/04/10/considering-the-environmental-impacts-of-generative-ai-to-spark-responsible-development/)).

## Could become a model

Demand elasticity slider: how much does demand respond to cheaper compute?

## Open questions

- Which arrows are well established, and which are hypotheses?
