---
doc_id: HMN-PRS-001
title: HeatMap Node product requirements and specifications
project: HeatMap Node
doc_type: Product requirements and specifications
version: "0.8"
status: Draft
date: 2026-11-01
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
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Status from HMN-CAL-001 v0.4 after the design for construction (HMN-DDR-003); R13 reported against the value-engineering target
- version: "0.8"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Core above the arm carried into the model (2026-10-02): R7 note, R15 mass 2.08 kg head and 4.92 kg node; no status changes"
- version: "0.8"
  date: 2026-11-01
  author: Amish Chadha
  change: "Kit 1.9.1 upgrade: R1 to R15 migrated to PR-001 to PR-015 (renamed from HMN-REQ-001), each traced to a user requirement in HMN-URS-001; Tolerance and Units columns, Was column; PR-016, PR-017 and PR-018 added for the FieldNode core limits and for CAD fidelity and for upkeep; statuses unchanged from HMN-CAL-001 v0.4"

---

# HeatMap Node product requirements and specifications

What the node must do, each requirement traced to a user need in HMN-URS-001 (links in HMN-RTM-001). The requirements describe option A, the fan-aspirated shield with a black globe and a cup anemometer, which is the current design; Amish has not chosen between it and option B (HMN-OPT-001, HMN-DDR-004: proposed, awaiting Amish). They were first written as R1 to R15 and checked by calculation at TRL 3 (HMN-CAL-001 v0.4, after the design for construction, HMN-DDR-003); the column "Was" keeps the old numbers. Targets are not yet validated with users and will be revised after co-design sessions (HMN-PRB-001). Nothing has been tested.

**One requirement is not met on paper (PR-009), four are at risk (PR-001, PR-005, PR-010 and PR-014), and one is over its value-engineering target (PR-013).** Of the 15 migrated requirements the rest are met on paper or by design; PR-016 and PR-018 are new and to be verified at TRL 4. The decisions behind the targets are HMN-DDR-001 and HMN-DDR-002 (2026-09-25), the budget top-up of 2026-09-26 and the value-engineering decision of 2026-10-01 (HMN-DEC-001): R4 covers 0.8 to 20 m/s with calm intervals flagged, R8 asks for +50 °C at the node, R13 and R15 exclude the FieldNode core and its pole adapter, and `budget_usd` (130) is a hypothetical control target, not a limit.

*Table 1. Product requirements and specifications. Status from HMN-CAL-001 v0.4 (`python docs/04-calcs/sizing.py`), not met first.*

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-009 | UR-013 | Physical architecture | Measurement height | Sensors at pedestrian height | 1.1 to 2.0 | range | m | Mounting review with pole owners (TRL 3); side-by-side comparison of 2.0 and 2.8 m (TRL 4) | **Not met**: sensors at 2.67 to 2.69 m; pedestrian-height air 0.2 to 0.8 °C warmer in strong sun (HMN-DDR-001 D2 chose 2.8 m for reach and vandal resistance; proposed, awaiting Amish) | R9 |
| PR-005 | UR-001, UR-002 | Performance | Derived heat stress | Mean radiant temperature and outdoor WBGT computed per ISO 7243 definitions with the Liljegren method; WBGT within the tolerance of a reference WBGT meter | 1.0 | ±, max | °C | Calculation note (TRL 3); collocation with a reference meter (TRL 4) | **At risk**: input error ±0.30 °C RSS of random terms, ±0.55 °C worst case with the fan, plus a one-sided shield bias up to 0.43 °C and height bias up to 0.4 °C; calm intervals flagged; Liljegren model error unknown | R5 |
| PR-010 | UR-003, UR-004 | Usability | Fit to existing poles | Stainless band clamps for 60 to 200 mm round poles; no drilling; fitted from a ladder or lift by two people | 30 | max | min | Design review (TRL 3); timed trial (TRL 4) | **At risk** (time): 120 degree V-saddle fits 60 to 200 mm; 37 min estimated | R10 |
| PR-014 | UR-010 | Software | Traceable data | Each node carries a calibration record from CalRig; readings published in an open, documented format with node location and height | Pass or fail | n/a | n/a | Documentation review | **At risk**: the probe calibrated before fitting fits a CalRig bay but the assembled 150 mm globe does not; payload format defined | R14 |
| PR-013 | UR-007, UR-014 | Cost | Sensor head cost | Sensor head (all parts except the FieldNode core and its pole adapter) against the value-engineering target `budget_usd`; a hypothetical control target; cost reported as over or under it. FieldNode core, sun shield and pole adapter are counted against FieldNode; the full-node cost is reported for information | 130 | max | USD | Priced BOM, `bom/bom.csv` | **Over target by USD 6.00**: USD 136.00 for the head; core with shield and adapter USD 156.00; full node USD 292.00 | R13 |
| PR-001 | UR-002 | Performance | Air temperature accuracy | Air temperature accuracy in the street against a reference aspirated thermometer, in full sun at wind speeds of 1 m/s or more (1.0 °C below 1 m/s) | 0.5 | ±, max | °C | Shield error estimate (TRL 3); side-by-side field comparison (TRL 4) | **At risk** (restated after the independent review of HMN-STM-001 S6): 0.43 °C with the fan at 1 m/s and more, on an assumed 50 % plate-to-air coupling, a 2 s sensor lag and a 6 s fan run; the energy-balance bound is 0.79 °C, above the 0.5 °C target; 1.04 °C at 1 m/s with the fan off | R1 |
| PR-002 | UR-002 | Performance | Humidity accuracy | Relative humidity accuracy from 20 to 80 %RH at 15 to 40 °C | 3 | ±, max | %RH | Datasheet; CalRig salt fixed points (TRL 4) | Met by design: SHT45 ±1.0 %RH typical | R2 |
| PR-003 | UR-001, UR-002 | Performance | Globe temperature | Standard 150 mm black globe (emissivity about 0.95); probe error after calibration; 90 % response time | 0.3 °C; 30 min | ±, max; max | °C; min | Calibration in CalRig (TRL 4); response estimate (TRL 3) | Met on paper: probe ±0.18 °C (±0.26 °C with a maximum-tolerance reference); 90 % response about 12 min | R3 |
| PR-004 | UR-001 | Performance | Wind speed | Wind speed from 0.8 to 20 m/s at ±0.5 m/s or ±10 %, whichever is larger; the share of each interval below the start-up speed is reported so the server can flag biased intervals (restated under HMN-DDR-002; was 0.5 to 20 m/s) | 0.8 to 20 | range | m/s | Datasheet of the chosen anemometer (TRL 3); wind comparison (TRL 4) | Met on paper: start-up about 0.8 m/s (typical, unverified); calm share flagged at 20 % of an interval | R4 |
| PR-006 | UR-006 | Software | Reporting | 15 min means of all channels by default (adjustable 5 to 60 min); data at the gateway within 30 min; 7 days stored on the node for resend | 30 | max | min | FieldNode firmware design; airtime calculation (TRL 3) | Met on paper: 20 B payload; 23.7 s/day at SF9; 7 days in 21.5 kB; 16 min latency for 99 % of intervals | R6 |
| PR-007 | UR-005 | Electrical | Power autonomy | No mains; days without sun at the default reporting interval | 5 | min | days | FieldNode energy budget plus the sensor load in HMN-PRC-001 (TRL 3) | Met on paper: sensors and fan 35.4 mW, 35 % of FieldNode's 100 mW design allowance | R7 |
| PR-008 | UR-008 | Environmental | Outdoor survival | Electronics IP65; operate at the node from -20 to +50 °C (restated under HMN-DDR-002, was +60 °C) with FieldNode's hot-climate sun shield on the core; UV-stable plastics; sensors survive driving rain and dust | -20 to +50 | range | °C | Design review; datasheets (TRL 3) | Met on paper: FieldNode interior 57.2 °C at 50 °C air with its sun shield, against 70 °C; sensor head parts within ratings (shield factor assumed); LiFePO4 charge limit to confirm (STEM S25) | R8 |
| PR-011 | UR-008, UR-012 | Structural | Wind survival | No failure at a 35 m/s gust; arm deflection at 20 m/s | 10 | max | mm | Wind load calculation (TRL 3) | Met on paper: arm factor 9.9 on minimum yield (7.5 with the head's weight added); 0.31 mm at 20 m/s; clamp twist factor 2.5 (preload assumed) | R11 |
| PR-012 | UR-009 | Regulatory | Privacy | Environmental data only: no camera, microphone, Wi-Fi or Bluetooth scanning, or any personal data | Pass or fail | n/a | n/a | Design review of hardware and firmware | Met by design: no imaging, audio or radio scanning parts; environmental payload only | R12 |
| PR-015 | UR-012 | Physical architecture | Mass and loading on the pole | Mass of the sensor head (restated under HMN-DDR-002, was the complete node); the complete-node mass is reported for the pole owner; no part larger than 300 mm across other than the arm | 4 | max | kg | Mass estimate (TRL 3); the D3 model's mass is in `cad/fidelity.json` | Met on paper: sensor head 2.11 kg; complete node 4.98 kg for information; largest part 290 mm | R15 |
| PR-016 | UR-005, UR-008 | Electrical | Charging limit of the cell | The FieldNode cell shall not charge above its rated charge temperature, which the interior of the core exceeds at 50 °C air | 45 | max | °C | Datasheet of the chosen cell; FieldNode firmware (TRL 3 paper) | To verify at TRL 4: interior 57.2 °C at 50 °C air against the usual 45 °C charge limit for LiFePO4 (STEM S25); a cross-repo item for FieldNode, new in this upgrade | New |
| PR-017 | UR-014 | Physical architecture | Buildable from open files | The chosen option shall be modelled to detail level D3 (real stock, every fastener, edge breaks), with a STEP file for each made and bought part and a BOM line for each | Pass or fail | n/a | n/a | `python .kit/cad_check.py --export` (TRL 3) | Met by design: `cad/fidelity.json` passes at D3 for options A and B | New |
| PR-018 | UR-011 | Usability | Little upkeep | A scheduled visit for option A (clean the shield gaps and the globe, check the fan and the clamp, swap the probe for a calibrated one) shall be needed no more often than the interval below; no consumables other than cable ties and a cloth | 6 | min | months | Maintenance steps in the build plan (TRL 3 paper); field log of fouling (TRL 4) | To verify at TRL 4: fouling of the gaps and the fan by insects and dust is unknown (STEM S27); option B would need a visit every 5 to 7 days for water (STEM S31b) | New |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, electrical, software. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Assumptions

- The FieldNode core performs as stated in FND-CAL-001 (100 mW design sensor allowance, 5.75 days without sun at that load; hot-climate node with the sun shield 2.61 kg, $148.00 after its design for construction, FND-DDR-003).
- WBGT is derived, not measured with a wetted wick, because a natural wet-bulb sensor needs a water reservoir that would need refilling at every node. Option B (HMN-OPT-001) tests that assumption on paper.
- Pole owners permit clamped attachments at the proposed height.
- The mass of the D3 model (4.3 kg for option A in `cad/fidelity.json`) differs from the calculation note's 4.98 kg complete node because the FieldNode core is modelled as an envelope with stand-in internals and the globe wall is drawn at 1.5 mm; the calculation note governs PR-015.
