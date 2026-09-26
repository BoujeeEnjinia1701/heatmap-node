---
doc_id: HMN-DDR-001
title: HeatMap Node TRL 2 review decisions
project: HeatMap Node
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, and the items that remain open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** proposed. Items D1 to D8 carry a recommendation that is adopted for TRL 3 work pending Amish's review; items O1 and O2 remain "Proposed, awaiting Amish".

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed nine items as "Proposed, awaiting Amish", and the design precis HMN-PRC-001 v0.2 listed seven key design choices. On 2026-09-25 Amish asked for this batch of repos to go through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's items one by one. Every item that carried a recommendation is therefore adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Items without a recommendation stay open. Nothing here is recorded as decided or approved by Amish.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in HMN-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Items adopted as recommended for TRL 3.*

| # | Item | Recommendation adopted | Status |
| --- | --- | --- | --- |
| D1 | Budget (R13) | Option (a): the FieldNode core is a shared component costed and budgeted in the FieldNode repo; HeatMap Node's $120 `budget_usd` covers the sensor head only. R13 is redefined as "sensor head $120 or less". No new `budget_usd` figure was recommended, so `project.yaml` keeps $120. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D2 | Measurement height (R9) | Option (a): arm at about 2.8 m on city poles, with the height correction studied at TRL 3 (HMN-CAL-001, section E) and a later short pilot comparing 2.0 and 2.8 m. The R9 target is unchanged, so R9 stays not met. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D3 | Globe size | Standard 150 mm black globe, not a 38 to 40 mm table tennis ball globe. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D4 | Wind | A cup anemometer on the arm, not a sonic anemometer or wind from the nearest official station. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D5 | Shield | Naturally ventilated multi-plate shield, not fan-aspirated. HMN-CAL-001 shows R1 is not met with it; a fan option is proposed anew in `docs/REVIEW.md`. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D6 | WBGT method | WBGT derived by the Liljegren method from air temperature, humidity, globe temperature and wind, not a wetted natural wet-bulb sensor. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D7 | Platform | Build on the FieldNode core; send data through a TwinKit gateway or a public LoRaWAN network. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D8 | Data policy | Open data under an open license, environmental channels only (R12). The publisher and host stay open (O2). | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |

*Table 2. Items that remain open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First partner and city for co-design and a pilot network. No preference was stated and no recommendation was made. | Proposed, awaiting Amish |
| O2 | Who publishes and hosts the data (TwinKit, CityTwin or a public platform); to be agreed with the first partner. No recommendation was made. | Proposed, awaiting Amish |

## Consequences

- `project.yaml`: only the TRL fields and evidence list change. `budget_usd` stays at $120 (D1 redefines what it covers rather than changing the figure). No reworded pitch or problem line was recommended, so the pitch and problem in `project.yaml` and `README.md` are unchanged.
- HMN-REQ-001 v0.3: R13 now reads "sensor head $120 or less"; the full-node figure is reported for information against the FieldNode budget. No other target changes.
- HMN-PRB-001 and HMN-PRC-001 v0.3: the design choices are no longer "proposed"; they are adopted for TRL 3 pending Amish's review.
- HMN-CAL-001 found that the sensor head costs $130 against the $120 budget, that the complete node weighs 4.68 kg against 4.0 kg, and that the shield misses R1. The TRL 3 work added two parts (secondary retention lanyards and a wider pole adapter for the FieldNode core). New proposals arising from these results are in `docs/REVIEW.md` and await Amish; this record does not decide them.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
