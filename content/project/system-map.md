---
title: "System map: impacts, links, loops and stocks"
description: "A first whole-system causal loop and stock-and-flow map linking every impact in our taxonomy to the drivers and decisions that move it."
maturity: seedling
branch: []
component: []
owner: ""
drafted_by: "agent: Claude Opus 5.5"
verified_by: ""
tags: [system-dynamics, loop, map]
---

A first draft of the whole system: all 145 impacts from our impact taxonomy, plus 46 drivers and decisions, joined by 396 signed causal links, 24 named feedback loops, 23 physical parts mapped to impacts, and 10 stock-and-flow sectors.

**Open the interactive map:** [System map explorer](../static/system-map.htm), with views for the causal map, feedback loops, stocks and flows, physical parts and the impact catalogue.

> [!warning] Unverified
> Every link and loop here is an agent's hypothesis. None has a source yet. Treat it as a scaffold to check, not a finding.

## What it is

- **Impacts** come straight from the taxonomy sheet (`data/system-map/impact-taxonomy.tsv`), keeping its domains and the "how it can be known" tag (measured, modelled, qualitative, relational).
- **Drivers and decisions** were added: demand and technology, data center decisions, siting and grid access, policy and governance, external conditions.
- **Links** read "if A rises, B rises (+) / falls (−), all else equal". Some are flagged as having a significant delay.
- **Loop polarity** is computed from the link signs when the model is built (`model.py`), not labelled by hand.
- **Scope:** one region hosting a data center cluster, with links out to the grid, chip and mineral supply chains and the climate. Signs assume a grid where new demand is mostly met by gas. Some links weaken or flip on other grids.

## Feedback loops

| ID | Loop | Type | Path (closes back to the start) | Garden note |
| --- | --- | --- | --- | --- |
| R1 | AI boom flywheel | R | AI capability → AI adoption and usage → AI and cloud revenue → Investor expectations → Data center capex → Planned pipeline → Capacity under construction → Installed IT capacity → National compute capacity |  |
| R2 | Scale and efficiency rebound | R | Cost per unit of compute → Reinvestment of efficiency gains in more computing → Demand for compute → Planned pipeline → Capacity under construction → Installed IT capacity | [[loops/efficiency-rebound\|Efficiency rebound]] |
| R3 | Hub clustering | R | Installed IT capacity → Connectivity → Siting attractiveness → Planned pipeline → Capacity under construction |  |
| R4 | Fiscal capture | R | Installed IT capacity → Local tax revenue → Fiscal dependence on one industry → Data center tax incentives → Siting attractiveness → Planned pipeline → Capacity under construction |  |
| R5 | Secrecy–distrust spiral | R | Developer secrecy → Trust in developers and officials → Conflict and organised opposition |  |
| R6 | Bring-your-own-power | R | Peak load → Interconnection queue → Grid connection wait time → Generation outside the public grid → Power availability at site → Siting attractiveness → Planned pipeline → Capacity under construction → Installed IT capacity |  |
| R7 | Warming raises cooling load | R | Electricity consumed → Gas generation → Operational CO2 → Atmospheric greenhouse gas stock → Climate change → PUE |  |
| R8 | Utility rate-base growth | R | Utility grid investment → Utility rate base → Utility financial health |  |
| R9 | Circular supply security | R | Hardware purchases → Hardware kept in use → Hardware retirement → Material recovery from retired hardware → Secondary material supply → Exposure to supply shocks → Chip and equipment supply |  |
| R10 | Jobs promise | R | Hope for jobs and renewal → Public opinion → Conflict and organised opposition → Zoning limits and moratoria → Land availability → Siting attractiveness → Planned pipeline → Capacity under construction → Construction employment |  |
| B1 | Grid queue brake | B | Installed IT capacity → Peak load → Interconnection queue → Grid connection wait time → Power availability at site → Siting attractiveness → Planned pipeline → Capacity under construction |  |
| B2 | Power price brake | B | Installed IT capacity → Peak load → Wholesale energy price → Siting attractiveness → Planned pipeline → Capacity under construction |  |
| B3 | Ratepayer backlash | B | Household electricity bills → Large-load tariffs → Share of grid costs carried by other customers |  |
| B4 | Tariffs slow growth | B | Installed IT capacity → Peak load → Utility grid investment → Utility rate base → Household electricity bills → Large-load tariffs → Siting attractiveness → Planned pipeline → Capacity under construction |  |
| B5 | Neighbour pushback | B | Installed IT capacity → Continuous sound level → Sleep → Stress and anxiety → Conflict and organised opposition → Zoning limits and moratoria → Land availability → Siting attractiveness → Planned pipeline → Capacity under construction | [[loops/community-pushback\|Community pushback]] |
| B6 | Water scarcity shifts cooling | B | Water lost to evaporation → Municipal supply drawn → Groundwater level → Drought and water scarcity → Evaporative cooling share | [[loops/water-vs-energy\|Water vs energy]] |
| B7 | Corporate clean procurement | B | Clean energy procurement → Renewable generation and storage → Gas generation → Operational CO2 → Corporate climate targets |  |
| B8 | Public clean energy standards | B | Operational CO2 → State and national climate targets → Clean energy standards → Coal generation |  |
| B9 | Leverage limits capex | B | Data center capex → Debt and financial exposure → Cost of capital |  |
| B10 | Mineral cost brake | B | Hardware purchases → Gallium → Critical mineral prices → Cost per unit of compute → Reinvestment of efficiency gains in more computing → Demand for compute → Planned pipeline → Capacity under construction → Installed IT capacity |  |
| B11 | Fab water constraint | B | Hardware purchases → Water embedded in hardware → Drought and water scarcity → Chip and equipment supply |  |
| B12 | Disclosure rebuilds trust | B | Conflict and organised opposition → Disclosure rules → Public availability of contract terms → Trust in developers and officials |  |
| B13 | Security–transparency tension | B | Developer secrecy → Visibility of infrastructure and its labour → Physical attack on facilities |  |
| B14 | Skilled-trades bottleneck | B | Capacity under construction → Construction employment → Availability of skilled trades → Installed IT capacity → Connectivity → Siting attractiveness → Planned pipeline |  |

## Data

All files live in `data/system-map/` in the repo. `model.py` is the single source: edit the link list, loops, parts or stock-flow panels there, then run `python3 model.py impact-taxonomy.tsv` to rebuild `model.json` and the CSVs. `nodes.csv` and `links.csv` import directly into Kumu. The explorer page has the model embedded, so after a rebuild the page needs regenerating too.

## Connections

- Part of loops: [[loops/efficiency-rebound]], [[loops/water-vs-energy]], [[loops/community-pushback]], [[loops/refresh-trade-off]]
- Components: [[components/index|Components]]
- Branches: [[branches/index|Branches]]

## Open questions

- Which links does the literature support, which are contested, and which are wrong? Each needs a source before the note can be promoted.
- Which signs flip on grids that are mostly hydro, nuclear or renewables?
- Which loops should we simulate first? The AI boom flywheel (R1) against the grid queue (B1) and ratepayer (B3/B4) brakes looks like the core overshoot story.
- Which host region should parameterise the stock-and-flow chains first?
