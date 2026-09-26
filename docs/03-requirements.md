---
doc_id: HMN-REQ-001
title: HeatMap Node requirements
project: HeatMap Node
doc_type: Requirements
version: "0.3"
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
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: "TRL 3: R13 redefined to the sensor head per HMN-DDR-001 D1; status table replaced by the results of HMN-CAL-001"
---

# HeatMap Node requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with users, and will be revised after co-design sessions (see HMN-PRB-001). Version 0.3 redefines R13 to cover the sensor head only, under HMN-DDR-001 D1 (adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review). No other target changes. Status is from the TRL 3 calculations in HMN-CAL-001; nothing has been tested.

Six requirements are **not met** on paper (R1, R4, R8, R9, R13 and R15), three are **at risk** (R5, R10 and R14), four are met on paper and two are met by design. See Table 2.

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
| R13 | Cost | Sensor head (all parts except the FieldNode core) $120 or less, the `budget_usd` in `project.yaml`. The FieldNode core is costed in the FieldNode repo; the full-node cost is reported for information | Priced BOM |
| R14 | Traceable data | Each node carries a calibration record from CalRig; readings published in an open, documented format with node location and height | Documentation review |
| R15 | Mass and loading on the pole | 4 kg or less for the complete node; no part larger than 300 mm across other than the arm | Mass estimate |

*Table 2. Status from HMN-CAL-001 (TRL 3 calculations).*

| ID | Value (HMN-CAL-001) | Status |
| --- | --- | --- |
| R1 | 1.04 °C at 1 m/s and 2.09 °C at 0.5 m/s in full sun with the naturally ventilated shield; 0.09 °C with a fan (option) | **Not met** (assumption-sensitive) |
| R2 | SHT45 ±1.0 %RH typical | Met by design |
| R3 | Probe ±0.18 °C (±0.26 °C with a maximum-tolerance reference); 90 % response about 12 min | Met on paper |
| R4 | Anemometer start-up about 0.8 m/s (typical, unverified); zero read below it biases MRT by -8.2 °C at a true 0.5 m/s | **Not met** |
| R5 | Input error ±0.59 °C RSS, ±0.88 °C worst case; +0.9 °C in calm air below start-up; Liljegren model error unknown | **At risk** |
| R6 | 20 B payload; 23.7 s/day at SF9; 7 days in 21.5 kB; 16 min latency for 99 % of intervals | Met on paper |
| R7 | Sensor load 0.116 mW, 0.12 % of FieldNode's 100 mW design allowance | Met on paper |
| R8 | FieldNode interior 78.3 °C at 50 °C air and 88.3 °C at 60 °C against a 70 °C rating (FND-CAL-001); sensor head parts within ratings | **Not met** (FieldNode core) |
| R9 | Sensors at 2.67 to 2.71 m; pedestrian-height air 0.2 to 0.8 °C warmer in strong sun | **Not met** |
| R10 | 120° V-saddle fits 60 to 200 mm; 37 min estimated | **At risk** (time) |
| R11 | Arm factor 13.8 on yield; 0.29 mm at 20 m/s; clamp twist factor 2.6 | Met on paper (preload assumed) |
| R12 | No imaging, audio or radio scanning parts; environmental payload only | Met by design |
| R13 | Sensor head $130.00; full node $256.00 | **Not met** (sensor head $10 over) |
| R14 | Probe calibrated before fitting fits a CalRig bay; the assembled 150 mm globe does not; payload format defined | **At risk** |
| R15 | 4.68 kg complete node (FieldNode 2.41 kg); largest part 290 mm | **Not met** (mass) |

## Assumptions

- The FieldNode core performs as stated in FND-CAL-001 (100 mW design sensor allowance, 5.75 days without sun at that load; 2.41 kg; $126.00).
- WBGT is derived, not measured with a wetted wick, because a natural wet-bulb sensor needs a water reservoir that would need refilling at every node.
- Pole owners permit clamped attachments at the proposed height.
