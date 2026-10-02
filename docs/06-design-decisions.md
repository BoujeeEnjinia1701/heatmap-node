---
doc_id: HMN-DEC-001
title: HeatMap Node design decisions register
project: HeatMap Node
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the build plan; open decisions, items to confirm, value engineering and decisions made
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Amish approved the recommendations for all nine open decisions (HMN-DDR-003 accepted); moved to decisions made"
---

# HeatMap Node design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The globe's top boss is threaded M10 x 1, or an M10 x 1 adapter fits it, and the boss is soldered strongly enough to hang the globe | The hanger tube screws into the boss; the lanyard backs it up | HMN-DDR-003, P7 |
| 2 | The anemometer's mast is a 16 mm tube that can be drilled for a 5 mm pin, and its cable leaves at the foot of the mast | The mast passes through 16.5 mm holes in the arm and is pinned | HMN-DDR-003, P8 |
| 3 | The fan's corner holes are on a 50 mm square and take M4 screws | The cowl legs, the fan and the top plate share four screws | HMN-DDR-003, P5 |
| 4 | The temperature and humidity capsule is 18 mm across and at least 45 mm long | It is a push fit in the 18.5 mm hub | HMN-DDR-003, P6 |
| 5 | Rubber edge trim for 3 mm sheet with about 1.5 mm of rubber on the bearing edge | Sets where the pole bears in the V | HMN-DDR-003, P1 |
| 6 | Strap band width (13 mm) and buckle size suit the 16 mm slots, and the band tool gives the 1,000 N preload the clamp check assumes | The twist factor of 2.5 rests on that preload | HMN-CAL-001 [H5] |
| 7 | The FieldNode back plate's band slots (51 mm each side of centre) and V-block screw holes (18 mm each side) are as in FND-DWG-101 | The adapter V-blocks are drilled and slotted to match | FND-DDR-003; HMN-DDR-003, P12 |
| 8 | The heat-set inserts' hole size for the printer and filament used | The adapter blocks carry the FieldNode core through them | HMN-DDR-003, P12 |

## Value engineering

Value-engineering target: USD 130 for the sensor head (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 136 (USD 6 over the target). The FieldNode core with its sun shield and the pole adapter (USD 156) are counted against FieldNode; the full node is USD 292, for information. Main cost drivers and savings worth trying:

- The largest lines are the cup anemometer (USD 32), the globe with its hanger tube (USD 24), the shield (USD 15), the temperature and humidity sensor (USD 14) and the harness (USD 12); these five are 71 % of the head.
- Making the design constructable added USD 9: cheeks, wider sheet and trim on the saddle (USD 3), the M10 hanger tube and nuts (USD 2), a fourth rod and two spacers (USD 1), and bolts, sleeves, a plug and long cable ties (USD 3).
- Savings worth trying: one 8-pin lead in place of two 5-pin leads, if FieldNode's port design allows it (about USD 4); a float ball bought with a threaded boss already fitted, avoiding an adapter; printing the cheeks in ASA is not recommended, since they carry the arm.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 items D1 to D8: budget covers the sensor head only; arm at about 2.8 m with a height correction; 150 mm globe; cup anemometer; WBGT derived by the Liljegren method; FieldNode core with TwinKit or a public LoRaWAN network; open data, environmental channels only (D5, passive shield, later superseded by N2) | Amish: "i accept all your recommendations, go with them across all repos." | HMN-DDR-001, HMN-DDR-002 |
| 2026-09-25 | N1: pole adapter counted against FieldNode and a formed 3 mm sheet saddle | Amish, same instruction | HMN-DDR-002 |
| 2026-09-25 | N2: fan-aspirated shield, run 6 s before each reading every 3 min | Amish, same instruction | HMN-DDR-002 |
| 2026-09-25 | N3: R15 mass limit applies to the sensor head only | Amish, same instruction | HMN-DDR-002 |
| 2026-09-25 | N4: R8 at +50 °C and FieldNode's hot-climate sun shield on HeatMap nodes | Amish, same instruction | HMN-DDR-002 |
| 2026-09-25 | N5: arm toward the equator with the FieldNode core below it | Amish, same instruction | HMN-DDR-002 |
| 2026-09-25 | N6: R4 restated to 0.8 to 20 m/s with calm intervals flagged | Amish, same instruction | HMN-DDR-002 |
| 2026-09-26 | N7: `budget_usd` raised from $120 to $130 | Amish: "I am ok with the budget top ups" | HMN-DDR-002 v0.2 |
| 2026-10-01 | `budget_usd` is a hypothetical value-engineering target, not a limit; cost is reported against it | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | This register; HMN-CAL-001 v0.4 |
| 2026-10-02 | Design for construction accepted: the thirteen changes of HMN-DDR-003 as made, including the arm end cap of the 2026-09-26 appearance review (P9) (open item 1) | Amish: "i approve your recommendations for all 555 open decisions." | HMN-DDR-003, Table 1 |
| 2026-10-02 | Sensor hub kept on three spokes (option a) and included in the TRL 4 side-by-side shield test (open item 2) | Amish: "i approve your recommendations for all 555 open decisions." | HMN-DDR-003, A1 |
| 2026-10-02 | FieldNode core mounted above the arm (option a), provided its lid stays reachable from the ladder or lift used to fit the arm; if not, the core goes on the pole's east or west face (option c) (open item 3) | Amish: "i approve your recommendations for all 555 open decisions." | HMN-DDR-002, N8; HMN-CAL-001 [E3] |
| 2026-10-02 | First partner and city: a hot US city with a dedicated heat office; first candidate to approach the City of Phoenix Office of Heat Response and Mitigation, using the US915 band (open item 4) | Amish: "i approve your recommendations for all 555 open decisions." | HMN-DDR-001, O1 |
| 2026-10-02 | Data routed through a TwinKit gateway and published from CityTwin's open data export under an open licence, with Amish's lab as publisher until the partner city takes it over; mirrored on the city's own open data portal if it has one (open item 5) | Amish: "i approve your recommendations for all 555 open decisions." | HMN-DDR-001, O2 |
| 2026-10-02 | Sensor ports follow FieldNode's candidate pinout: port A, the I2C sensor on data pins 2 and 4 with sensor and fan on the switched rail; port B, the thermistor on analog pin 5 and the anemometer pulse on pin 2 (open item 6) | Amish: "i approve your recommendations for all 555 open decisions." | FieldNode FND-DDR-001, O2; HMN-DDR-002 cross-repo actions |
| 2026-10-02 | FieldNode internals kept as stand-ins in the appearance model; the FieldNode repo is asked to confirm the cell format and board position at its next update (open item 7) | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW.md, 2026-09-26 |
| 2026-10-02 | Name plate kept on the FieldNode sun shield; side vent slots dropped unless FieldNode adopts them (open item 8) | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW.md, 2026-09-26 |
| 2026-10-02 | Raised seam ring at the globe equator accepted for appearance (open item 9) | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW.md, 2026-09-26 |
