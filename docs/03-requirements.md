---
doc_id: HMN-REQ-001
title: HeatMap Node requirements
project: HeatMap Node
doc_type: Requirements
version: "0.5"
status: Draft
date: '2026-09-26'
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
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget top-up approved by Amish
---

# HeatMap Node requirements

These are first-pass requirements for the concept. Targets are not yet validated with users and will be revised after co-design sessions (see HMN-PRB-001). Version 0.4 applies the decisions Amish accepted on 2026-09-25 (HMN-DDR-001 and HMN-DDR-002): R4 now covers 0.8 to 20 m/s with calm intervals flagged, R8 now asks for +50 °C at the node, R13 now excludes the FieldNode core and its pole adapter, and R15 now applies to the sensor head only. R1 keeps its ±0.5 °C target, which the fan-aspirated shield is meant to meet. Version 0.5 raises the R13 target from $120 to $130 after Amish approved the budget top-up on 2026-09-26 (HMN-DDR-002 v0.2). Status is from the TRL 3 calculations in HMN-CAL-001 v0.3; nothing has been tested.

One requirement is **not met** on paper (R9), three are **at risk** (R5, R10 and R14), nine are met on paper and two are met by design. See Table 2.

*Table 1. Requirements.*

| ID | Requirement | Target | Verification (TRL 3 or later) |
| --- | --- | --- | --- |
| R1 | Air temperature accuracy in the street | ±0.5 °C against a reference aspirated thermometer, in full sun at wind speeds of 1 m/s or more; ±1.0 °C below 1 m/s (met at all wind speeds with the fan-aspirated shield, HMN-DDR-002) | Shield error estimate; later side-by-side field comparison |
| R2 | Relative humidity accuracy | ±3 %RH from 20 to 80 %RH at 15 to 40 °C | Datasheet; CalRig salt fixed points |
| R3 | Globe temperature | Standard 150 mm black globe (emissivity about 0.95); probe ±0.3 °C after calibration; 90 % response within 30 min | Calibration in CalRig; response estimate |
| R4 | Wind speed | 0.8 to 20 m/s; ±0.5 m/s or ±10 %, whichever is larger; the share of each interval below the start-up speed is reported so that the server can flag biased intervals (restated under HMN-DDR-002; was 0.5 to 20 m/s) | Datasheet of the chosen anemometer; later wind comparison |
| R5 | Derived heat stress | Mean radiant temperature and outdoor WBGT computed per ISO 7243 definitions with the Liljegren method; WBGT within ±1.0 °C of a reference WBGT meter | Calculation note; later collocation with a reference meter |
| R6 | Reporting | 15 min means of all channels by default (adjustable 5 to 60 min); data at the gateway within 30 min; 7 days stored on the node for resend | FieldNode firmware design; airtime calculation |
| R7 | Power autonomy | No mains; 5 days without sun at the default reporting interval | FieldNode energy budget plus the sensor load in HMN-PRC-001 |
| R8 | Outdoor survival | Electronics IP65; operate at -20 to +50 °C at the node (restated under HMN-DDR-002, was +60 °C), with FieldNode's hot-climate sun shield on the core; UV-stable plastics; sensors survive driving rain and dust | Design review; datasheets |
| R9 | Measurement height | Sensors at pedestrian height (1.1 to 2.0 m) | Mounting review with pole owners |
| R10 | Fit to existing poles | Stainless band clamps for 60 to 200 mm round poles; no drilling; fitted from a ladder or lift by two people in 30 min or less | Design review; later timed trial |
| R11 | Wind survival | No failure at a 35 m/s gust; arm deflection under 10 mm at 20 m/s | Wind load calculation |
| R12 | Privacy | Environmental data only: no camera, microphone, Wi-Fi or Bluetooth scanning, or any personal data | Design review of hardware and firmware |
| R13 | Cost | Sensor head (all parts except the FieldNode core and its pole adapter) $130 or less (raised from $120 under HMN-DDR-002 v0.2, budget top-up approved by Amish on 2026-09-26), the `budget_usd` in `project.yaml`. The FieldNode core, its sun shield and the pole adapter are counted against FieldNode (HMN-DDR-001 D1, HMN-DDR-002); the full-node cost is reported for information | Priced BOM |
| R14 | Traceable data | Each node carries a calibration record from CalRig; readings published in an open, documented format with node location and height | Documentation review |
| R15 | Mass and loading on the pole | 4 kg or less for the sensor head (restated under HMN-DDR-002, was the complete node); the complete-node mass is reported for the pole owner; no part larger than 300 mm across other than the arm | Mass estimate |

*Table 2. Status from HMN-CAL-001 v0.3 (TRL 3 calculations), not met first.*

| ID | Value (HMN-CAL-001) | Status |
| --- | --- | --- |
| R9 | Sensors at 2.67 to 2.69 m; pedestrian-height air 0.2 to 0.8 °C warmer in strong sun | **Not met** |
| R5 | Input error ±0.30 °C RSS, ±0.55 °C worst case with the fan; calm intervals flagged; Liljegren model error unknown | **At risk** |
| R10 | 120° V-saddle fits 60 to 200 mm; 37 min estimated | **At risk** (time) |
| R14 | Probe calibrated before fitting fits a CalRig bay; the assembled 150 mm globe does not; payload format defined | **At risk** |
| R1 | 0.43 °C with the fan at any wind speed; 1.04 °C at 1 m/s with the fan off | Met on paper (fan flow assumed) |
| R3 | Probe ±0.18 °C (±0.26 °C with a maximum-tolerance reference); 90 % response about 12 min | Met on paper |
| R4 | Start-up about 0.8 m/s (typical, unverified); calm share reported and flagged at 20 % of an interval | Met on paper (start-up unverified) |
| R6 | 20 B payload; 23.7 s/day at SF9; 7 days in 21.5 kB; 16 min latency for 99 % of intervals | Met on paper |
| R7 | Sensors and fan 35.4 mW, 35 % of FieldNode's 100 mW design allowance | Met on paper (panel shading not included) |
| R8 | FieldNode interior 57.2 °C at 50 °C air with its sun shield, against 70 °C; sensor head parts within ratings | Met on paper (shield factor assumed) |
| R11 | Arm factor 13.4 on yield; 0.29 mm at 20 m/s; clamp twist factor 2.5 | Met on paper (preload assumed) |
| R13 | Sensor head $127.00 against $130; FieldNode core with shield and adapter $141.00; full node $268.00 | Met on paper ($3 margin) |
| R15 | Sensor head 1.91 kg; complete node 4.70 kg for information; largest part 290 mm | Met on paper |
| R2 | SHT45 ±1.0 %RH typical | Met by design |
| R12 | No imaging, audio or radio scanning parts; environmental payload only | Met by design |

## Assumptions

- The FieldNode core performs as stated in FND-CAL-001 v0.2 (100 mW design sensor allowance, 5.75 days without sun at that load; hot-climate node with the sun shield 2.55 kg, $134.00).
- WBGT is derived, not measured with a wetted wick, because a natural wet-bulb sensor needs a water reservoir that would need refilling at every node.
- Pole owners permit clamped attachments at the proposed height.
