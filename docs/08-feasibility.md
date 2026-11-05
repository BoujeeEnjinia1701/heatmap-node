---
doc_id: HMN-FEA-001
title: HeatMap Node feasibility assessment
project: HeatMap Node
doc_type: Feasibility
version: "0.1"
status: Draft
date: 2026-11-01
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-01
    author: Amish Chadha
    change: "First feasibility assessment at the kit 1.9.1 upgrade, from HMN-CAL-001, HMN-STM-001 and the D3 model"
---

# HeatMap Node feasibility assessment

Verdict: option A is feasible on paper at TRL 3 as a garage-built sensor head (USD 136 against a USD 130 target) on the FieldNode core, with two open measurement questions (the street error of the derived WBGT and the fan flow) that only a collocated field comparison can close at TRL 4; option B is feasible in principle but depends on a water upkeep cycle that few partners will keep. Method: STANDARDS section 23.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | Of 40 STEM rows, 21 are within known science and 15 plausible; three failures were fixed and one (the FieldNode cell charge limit) goes to Amish; the D3 models of both options pass `cad_check` with no interference | High | WBGT model error for streets unknown (PR-005 at risk); sensors at 2.7 m (PR-009 not met) | HMN-STM-001, HMN-CAL-001 |
| Materials | Aluminium 6063 and 5052, 316 stainless, copper globe, ASA prints, EPDM trim; no exotic material | Medium | ASA heat deflection of the chosen filament, stainless on aluminium corrosion and paint ageing are plausible, not shown (S22 to S24) | HMN-STM-001 S22 to S24 |
| Manufacturing and assembly | Saddle formed from 3 mm sheet, shield and cowl printed, arm drilled; fastened with 63 fasteners in the D3 model; build plan with pictures | Medium | Forming the saddle in a garage needs a brake or a sheet-metal shop; strap-band preload (S11) | HMN-BLD-001 (`docs/05-build-plan.md`), `cad/fidelity.json` |
| Power and controls | Sensors and fan 35.4 mW, 35 % of FieldNode's 100 mW allowance; 5.75 days without sun | Medium | Cell charging above its rated temperature (S25, PR-016) is a FieldNode item | FND-CAL-001, HMN-CAL-001 F2 |
| Supply of parts | All bought parts are catalogue items (SHT45, NTC, fan, cup anemometer, M12 leads) | Medium | Prices indicative; a cup anemometer of the assumed start-up is not chosen | `bom/bom.csv`, HMN-MKT-001 |
| Cost | USD 136.00 for the head, USD 6 over the USD 130 target; full node USD 292.00 | Medium | Savings listed in HMN-DEC-001 (one 8-pin lead about USD 4) | `bom/bom.csv`, PR-013 |
| Regulatory | No personal data; radio inside FieldNode's grant; pole permission per city | Medium | Module certification and pole standards to assess | HMN-REG-001 |
| Field operation | Visits about every 6 months for option A; 5 to 7 days for option B | Medium (A), Low (B) | Insects in shield gaps and fan (S27); wick upkeep (S35) | HMN-STM-001 |

Ratings: High, Medium, Low.
