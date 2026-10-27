---
title: "Servers"
description: "The computers themselves, and how long they stay in service before being replaced."
maturity: seedling
zoom_level: 4
component: [servers]
owner: ""
drafted_by: "agent: Claude"
verified_by: ""
tags: [component]
---

The computers themselves, and how long they stay in service before being replaced.

**Zoom level 4** · **Parts:** Chassis, motherboard, CPUs and GPUs, memory, storage, power supplies, fans

## Impacts

| Impact | What happens | Branch |
| --- | --- | --- |
| Operational energy | Most IT electricity is drawn by servers | [[branches/data-operations]] |
| Embodied carbon | Manufacturing emissions grow in share as grids get cleaner | [[branches/engineering]] |
| Refresh decisions | Replacing servers sooner can cut energy per task but adds embodied carbon and e-waste | [[branches/engineering]] |
| Utilization | Idle capacity still draws power and still carries embodied impacts | [[branches/data-operations]] |

## Sourced facts

- As operational emissions fall, hardware manufacturing becomes the dominant part of computing's carbon footprint ([Gupta et al., Chasing Carbon](https://arxiv.org/abs/2011.02839v1)).
- Open server impact data and an API: [BoaviztAPI](https://github.com/Boavizta/boaviztapi).

## Open questions

- Which numbers belong here, and from which source? (Owner to fill in.)
