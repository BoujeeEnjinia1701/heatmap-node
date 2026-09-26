---
doc_id: HMN-DDR-002
title: HeatMap Node recommendations accepted
project: HeatMap Node
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-26'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.2"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget top-up to $130 decided by Amish (N7)
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Every item listed in Tables 1 and 2 is decided by Amish, 2026-09-25: go with recommendation. Item N7 in Table 4 is decided by Amish, 2026-09-26 (budget top-up); the other items in Table 4 remain "Proposed, awaiting Amish".

## Context

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Before that, HMN-DDR-001 v0.1 held eight TRL 2 items (D1 to D8) adopted as recommended for TRL 3 and open for his review, and the TRL 3 session of `docs/REVIEW.md` listed six new items with a recommendation (items 3 to 8 of "Still awaiting Amish"). Items without a recommendation stay open. Where a recommendation offered several options, the recommended option is the decision. Work that needs TRL 4 (building, testing, measuring, trials, purchasing, firmware beyond a sketch) is recorded as decided but on hold, because TRL 4 is on hold by Amish's instruction.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (sessions 2026-09-25, /populate and TRL 3) and in HMN-DDR-001.

## Decision

*Table 1. HMN-DDR-001 items now decided (no further change to the repo beyond wording).*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| D1 | Budget scope | The $120 `budget_usd` covers the sensor head; the FieldNode core is budgeted in its own repo | Wording only; extended by N1 below |
| D2 | Measurement height | Arm at about 2.8 m with a height correction; a pilot comparing 2.0 and 2.8 m | Wording only; the pilot is TRL 4, decided but on hold |
| D3 | Globe | Standard 150 mm black globe | Wording only |
| D4 | Wind | Cup anemometer | Wording only |
| D5 | Shield | Naturally ventilated shield | Superseded by N2 (fan-aspirated), which Amish accepted in the same instruction |
| D6 | WBGT method | Derived by the Liljegren method | Wording only |
| D7 | Platform | FieldNode core, TwinKit gateway or a public LoRaWAN network | Wording only |
| D8 | Data policy | Open data, environmental channels only | Wording only |

*Table 2. TRL 3 review items now decided.*

| # | Item | Decision (recommended option) | What changed in the repo |
| --- | --- | --- | --- |
| N1 | Sensor head budget (R13) | Option (c): count the FieldNode pole adapter against FieldNode, plus option (b): find the remaining saving; `budget_usd` stays $120 | R13 restated to exclude the core and its adapter (HMN-REQ-001 v0.4). BOM line 8 is now a formed 3 mm sheet saddle, $8.00 to $5.00 and 0.57 to 0.40 kg; `saddle_wall` 5 to 3 mm in `model.py`. Before the fan these bring the head from $130.00 to $120.00. Cross-repo action: FieldNode large-pole kit variant |
| N2 | Shield (R1, R5) | Option (b): a small fan run before each reading | BOM line 13 added (60 mm 5 V fan and printed cowl, $7.00). Model: 56 mm hole in the top plate, fan and cowl, shield hung 25 mm lower (`shield_gap` 20 to 45 mm). Firmware rule (sketch level): 6 s of fan every 3 min, air read at the end of each run. HMN-CAL-001 v0.2: shield error 1.04 °C at 1 m/s to 0.43 °C at any wind; WBGT input budget ±0.59 to ±0.30 °C; sensor load 0.116 to 35.4 mW. R1 not met to met on paper |
| N3 | Mass (R15) | Option (b): 4 kg for the sensor head only | R15 restated. Head 2.03 to 1.91 kg; complete node 4.68 to 4.70 kg for information. R15 not met to met on paper |
| N4 | R8 range and FieldNode shield | Set R8 to +50 °C and fit FieldNode's hot-climate sun shield | R8 restated (+60 to +50 °C). BOM line 1 now the hot-climate FieldNode, $126.00 to $134.00, 2.41 to 2.55 kg; shield envelope added to the model. Core interior at 50 °C air 78.3 to 57.2 °C. R8 not met to met on paper |
| N5 | Arm orientation | Point the arm toward the equator with the FieldNode core below it; check panel shading at the first site | Model: arm along +X toward the equator, FieldNode core turned to face +X below the arm (`fn_azimuth` 90°), harness rerouted; HMN-DWG-001 to Rev P2. Pole shading of the globe near midday removed. HMN-CAL-001 v0.2 section E adds a paper check of panel shading (16 to 44 % near noon, see Table 4, N8). The site check is TRL 4, decided but on hold |
| N6 | Anemometer (R4) | Option (a): relax R4 to 0.8 to 20 m/s and flag biased intervals with the calm-share byte | R4 restated. Server rule: flag MRT and WBGT when 20 % or more of an interval is below start-up. R4 not met to met on paper (start-up unverified) |

*Table 3. Decided but on hold (TRL 4).*

| Item | Why on hold |
| --- | --- |
| D2 pilot comparing 2.0 and 2.8 m | Field trial |
| N5 panel shading check at the first site | Site work |
| N2 fan part choice, flow and life test, shield error test against an aspirated reference | Purchasing and testing |
| N2 and N6 firmware (fan timing, calm-share rule) beyond the sketch in HMN-CAL-001 | Firmware |

## Consequences

- `project.yaml`: `budget_usd` stays $120 (N1 redefines what it covers; no new figure was recommended); pitch and problem unchanged, as no rewording was recommended; the evidence list adds this record. `trl` and `trl_target` stay 3.
- Requirement status (HMN-CAL-001 v0.2): 2 not met (R9, R13), 3 at risk (R5, R10, R14), 8 met on paper, 2 met by design; before, 6 not met, 3 at risk, 4 met on paper, 2 met by design.
- Documents revised: HMN-PRB-001 v0.4, HMN-PRC-001 v0.4, HMN-REQ-001 v0.4, HMN-CAL-001 v0.2, HMN-DDR-001 v0.2; HMN-DWG-001 Rev P2; `bom/bom.csv`, `bom/bom-notes.md`, `cad/src/model.py`, STEP and STL, `cad/src/sheets.py`, `cad/src/concept_media.py` and `media/`; `README.md`.
- Two effects of the decisions taken together needed Amish (Table 4): the fan put the head $7 over budget, which Amish settled on 2026-09-26 with a budget top-up to $130 (N7), and the new orientation shades the FieldNode panel (N8, still open).
- Budget top-up to $130: decided by Amish, 2026-09-26. After it, requirement status is 1 not met (R9), 3 at risk, 9 met on paper and 2 met by design (HMN-CAL-001 v0.3).

*Table 4. Items still open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First partner and city for co-design and a pilot. No preference stated, no recommendation | Proposed, awaiting Amish |
| O2 | Data publisher and host. No recommendation | Proposed, awaiting Amish |
| N7 | Sensor head $127.00 against $120 after the fan. Options: (a) raise `budget_usd` to $130; (b) keep $120 and cut $7 more (for example a cheaper anemometer class, at the cost of R4); (c) count the fan against a separate accuracy option. Recommendation: (a), since the fan is a deliberate accuracy fix | Budget top-up to $130: decided by Amish, 2026-09-26 (option a). `budget_usd` $120 to $130; HMN-REQ-001 v0.5 and HMN-CAL-001 v0.3: R13 not met to met on paper ($3 margin) |
| N8 | FieldNode panel shaded 16 to 44 % near noon by the sensor head. Options: (a) mount the core above the arm, so that its shadow falls on the pole side; (b) keep it below and accept the loss, pending FieldNode's bypass diode layout; (c) move the core to the pole's east or west face. Recommendation: (a) | Proposed, awaiting Amish |

> **Safety:** The added fan starts on its own every 3 min. Unplug the sensor lead before working on the shield. The FieldNode sun shield is part of keeping the LiFePO4 cell within its charge limits at hot sites and must not be left off HeatMap nodes.
