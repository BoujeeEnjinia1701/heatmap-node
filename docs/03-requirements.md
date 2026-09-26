---
doc_id: HMN-REQ-001
title: HeatMap Node requirements
project: HeatMap Node
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept estimates
---

# HeatMap Node requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with users, and will be checked by calculation at TRL 3 and revised after co-design sessions (see HMN-PRB-001). Status is judged against the first-order estimates in HMN-PRC-001; nothing has been tested.

Three requirements are **not met** by the concept as drawn (R4 at low wind, R9 and R13 for the full node), and three are **at risk** (R1, R5 and R15). See Table 2.

*Table 1. Requirements.*

| ID | Requirement | Target | Verification (TRL 3 or later) |
| --- | --- | --- | --- |
| R1 | Air temperature accuracy in the street | ±0.5 °C against a reference aspirated thermometer, in full sun at wind speeds of 1 m/s or more; ±1.0 °C below 1 m/s | Shield error estimate; later side-by-side field comparison |
| R2 | Relative humidity accuracy | ±3 %RH from 20 to 80 %RH at 15 to 40 °C | Datasheet; CalRig salt fixed points |
| R3 | Globe temperature | Standard 150 mm black globe (emissivity about 0.95); probe ±0.3 °C after calibration; 90 % response within 30 min | Calibration in CalRig; response estimate |
| R4 | Wind speed | 0.5 to 20 m/s; ±0.5 m/s or ±10 %, whichever is larger | Datasheet of the chosen anemometer; later wind comparison |
| R5 | Derived heat stress | Mean radiant temperature and outdoor WBGT computed per ISO 7243 definitions with the Liljegren method; WBGT within ±1.0 °C of a reference WBGT meter | Calculation note; later collocation with a reference meter |
| R6 | Reporting | 15 min means of all channels by default (adjustable 5 to 60 min); data at the gateway within 30 min; 7 days stored on the node for resend | FieldNode firmware design; airtime calculation |
| R7 | Power autonomy | No mains; 5 days without sun at the default reporting interval | FieldNode energy budget plus the sensor load in HMN-PRC-001 |
| R8 | Outdoor survival | Electronics IP65; operate at -20 to +60 °C at the node; UV-stable plastics; sensors survive driving rain and dust | Design review; datasheets |
| R9 | Measurement height | Sensors at pedestrian height (1.1 to 2.0 m) | Mounting review with pole owners |
| R10 | Fit to existing poles | Stainless band clamps for 60 to 200 mm round poles; no drilling; fitted from a ladder or lift by two people in 30 min or less | Design review; later timed trial |
| R11 | Wind survival | No failure at a 35 m/s gust; arm deflection under 10 mm at 20 m/s | Wind load calculation |
| R12 | Privacy | Environmental data only: no camera, microphone, Wi-Fi or Bluetooth scanning, or any personal data | Design review of hardware and firmware |
| R13 | Cost | Sensor head $120 or less; full node including the FieldNode core $120 or less (the `budget_usd` in `project.yaml`) | Priced BOM |
| R14 | Traceable data | Each node carries a calibration record from CalRig; readings published in an open, documented format with node location and height | Documentation review |
| R15 | Mass and loading on the pole | 4 kg or less for the complete node; no part larger than 300 mm across other than the arm | Mass estimate |

*Table 2. Status against the concept estimates (HMN-PRC-001).*

| ID | Estimate | Status |
| --- | --- | --- |
| R1 | Passive multi-plate shields can read about 1 °C or more high in strong sun and calm air (estimate, to be quantified) | **At risk** below about 1 m/s |
| R2 | SHT45-class sensor behind a membrane | Met by design, to be confirmed |
| R3 | 150 mm globe, NTC at center; response time about 20 to 30 min (estimate) | Met by design, to be confirmed |
| R4 | Low-cost cup anemometers typically start at about 0.8 m/s (to be confirmed) | **Not met** from 0.5 to 0.8 m/s |
| R5 | A 0.5 m/s wind error at 1 m/s shifts mean radiant temperature by about 6 to 8 °C in the worked example | **At risk** in calm air |
| R6 | 96 uplinks a day at about 20 B | Met by design |
| R7 | Sensor load under 1 mW against about 115 mW allowed by FieldNode | Met, with a wide margin |
| R8 | Stock IP65 enclosure and M12 connectors | Met by design, to be confirmed |
| R9 | Arm at about 2.8 m to limit tampering | **Not met**; correction or a lower arm proposed, awaiting Amish |
| R10 | Longer bands than FieldNode's 40 to 60 mm kit | Met by design, to be confirmed |
| R11 | About 110 N total at 35 m/s; about 17 N·m at the arm root | Met by estimate |
| R12 | No imaging or audio parts in the BOM | Met |
| R13 | Sensor head about $120; full node about $246 | Sensor head met with no margin; **full node not met** |
| R14 | CalRig procedure not yet written | Open |
| R15 | About 3.3 kg | Met; **at risk** if a larger panel is needed in cloudy climates |

## Assumptions

- The FieldNode core performs as stated in its README and precis (about 115 mW sensor allowance, 5 days without sun).
- WBGT is derived, not measured with a wetted wick, because a natural wet-bulb sensor needs a water reservoir that would need refilling at every node.
- Pole owners permit clamped attachments at the proposed height.
