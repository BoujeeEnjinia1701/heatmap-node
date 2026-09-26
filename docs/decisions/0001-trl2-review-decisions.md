---
doc_id: HMN-DDR-001
title: HeatMap Node TRL 2 review decisions
project: HeatMap Node
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted for D1 to D8. On 2026-09-25 Amish wrote "i accept all your recommendations, go with them across all repos", so D1 to D8 are decided by Amish, 2026-09-25: go with recommendation (see HMN-DDR-002). Items O1 and O2 had no recommendation and remain "Proposed, awaiting Amish".

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed nine items as "Proposed, awaiting Amish", and the design precis HMN-PRC-001 v0.2 listed seven key design choices. On 2026-09-25 Amish asked for this batch of repos to go through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's items one by one. Every item that carried a recommendation is therefore adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Items without a recommendation stay open. Version 0.1 recorded nothing as decided by Amish. Version 0.2 records Amish's later 2026-09-25 acceptance of all recommendations: D1 to D8 are now decided; O1 and O2 are unchanged.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in HMN-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item | Recommendation adopted | Status |
| --- | --- | --- | --- |
| D1 | Budget (R13) | Option (a): the FieldNode core is a shared component costed and budgeted in the FieldNode repo; HeatMap Node's $120 `budget_usd` covers the sensor head only. R13 is redefined as "sensor head $120 or less". No new `budget_usd` figure was recommended, so `project.yaml` keeps $120. | Decided by Amish, 2026-09-25: go with recommendation |
| D2 | Measurement height (R9) | Option (a): arm at about 2.8 m on city poles, with the height correction studied at TRL 3 (HMN-CAL-001, section E) and a later short pilot comparing 2.0 and 2.8 m. The R9 target is unchanged, so R9 stays not met. | Decided by Amish, 2026-09-25: go with recommendation |
| D3 | Globe size | Standard 150 mm black globe, not a 38 to 40 mm table tennis ball globe. | Decided by Amish, 2026-09-25: go with recommendation |
| D4 | Wind | A cup anemometer on the arm, not a sonic anemometer or wind from the nearest official station. | Decided by Amish, 2026-09-25: go with recommendation |
| D5 | Shield | Naturally ventilated multi-plate shield, not fan-aspirated. HMN-CAL-001 showed R1 is not met with it; the later fan recommendation, also accepted, supersedes this item (HMN-DDR-002, item N2). | Decided by Amish, 2026-09-25: go with recommendation |
| D6 | WBGT method | WBGT derived by the Liljegren method from air temperature, humidity, globe temperature and wind, not a wetted natural wet-bulb sensor. | Decided by Amish, 2026-09-25: go with recommendation |
| D7 | Platform | Build on the FieldNode core; send data through a TwinKit gateway or a public LoRaWAN network. | Decided by Amish, 2026-09-25: go with recommendation |
| D8 | Data policy | Open data under an open license, environmental channels only (R12). The publisher and host stay open (O2). | Decided by Amish, 2026-09-25: go with recommendation |

*Table 2. Items that remain open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First partner and city for co-design and a pilot network. No preference was stated and no recommendation was made. | Proposed, awaiting Amish |
| O2 | Who publishes and hosts the data (TwinKit, CityTwin or a public platform); to be agreed with the first partner. No recommendation was made. | Proposed, awaiting Amish |

## Consequences

- `project.yaml`: only the TRL fields and evidence list change. `budget_usd` stays at $120 (D1 redefines what it covers rather than changing the figure). No reworded pitch or problem line was recommended, so the pitch and problem in `project.yaml` and `README.md` are unchanged.
- HMN-REQ-001 v0.3: R13 now reads "sensor head $120 or less"; the full-node figure is reported for information against the FieldNode budget. No other target changes.
- HMN-PRB-001 and HMN-PRC-001 v0.3: the design choices are no longer "proposed"; they are adopted for TRL 3 pending Amish's review. In v0.4 of both they are decided by Amish.
- HMN-CAL-001 found that the sensor head costs $130 against the $120 budget, that the complete node weighs 4.68 kg against 4.0 kg, and that the shield misses R1. The TRL 3 work added two parts (secondary retention lanyards and a wider pole adapter for the FieldNode core). New proposals arising from these results were listed in `docs/REVIEW.md`; Amish accepted them on 2026-09-25 and they are recorded in HMN-DDR-002.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
