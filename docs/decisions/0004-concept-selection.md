---
doc_id: HMN-DDR-004
title: HeatMap Node concept selection
project: HeatMap Node
doc_type: Design decision record
version: "0.1"
status: Draft
date: 2026-11-01
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: 2026-11-01
  author: Amish Chadha
  change: "Concept selection between option A and option B proposed at the kit 1.9.1 upgrade; awaiting Amish"
---

# 0004: Concept selection

- **Date:** 2026-11-01
- **Status:** proposed. Awaiting Amish. No choice has been made; `concept_chosen` in `project.yaml` is "A (proposed)", which only records that option A is the current design.

## Context

The design before this upgrade is a fan-aspirated shield with a black globe and a cup anemometer, and the WBGT is computed (HMN-DDR-001, HMN-DDR-002). Kit 1.8 asks every repo to compare at least two options with different working principles against the user requirements (HMN-URS-001). The current design is option A and is not redesigned. Option B is a direct natural wet-bulb head: a wetted wick on a small reservoir, with no fan and no anemometer, so the WBGT is measured as ISO 7243 defines it (HMN-OPT-001).

## Options considered

| Option | Weighted score of 180 | Strengths | Weaknesses |
| --- | --- | --- | --- |
| A, fan-aspirated shield, globe and anemometer | 140 | Wind measured; no water at the node; priced BOM, drawing and build plan exist; visit about every 6 months | Derived WBGT of unknown street error (PR-005 at risk); 35 mW fan; USD 6 over target |
| B, direct natural wet-bulb head | 129 | Measured wet bulb; no fan load; about USD 101 (estimate) | Water every 5 to 7 days; freezing (K1); wick fouling; no wind channel |

The totals differ by 7.9 %, inside the 10 % band, so the scoring does not separate them.

## Decision

**Proposed, awaiting Amish.** The recommendation is to keep option A as the design of record and to treat B's direct wet-bulb reading as a reference head on a few collocated poles, to test the Liljegren model in the field at TRL 4 (HMN-OPT-001, Recommendation). Amish may instead choose B, choose A alone, or ask for a hybrid.

## Consequences

- If A is chosen: nothing changes; `concept_chosen` becomes "A" and the build plan, BOM and drawing stand.
- If B is chosen: the BOM, build plan, drawing and calculation note must be redone for the wick head; B is modelled to D3 but has no priced BOM, no build plan and no sizing beyond the STEM check rows S31 to S37.
- The fixes K1, K1b (option B) and K2 (a restated claim) were made under Amish's standing instruction of 2026-10-23 and are recorded in HMN-DEC-001.
