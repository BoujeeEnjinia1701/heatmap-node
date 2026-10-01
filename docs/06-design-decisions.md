---
doc_id: HMN-DEC-001
title: HeatMap Node design decisions register
project: HeatMap Node
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the build plan; open decisions, items to confirm, value engineering and decisions made
---

# HeatMap Node design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design for construction | Accept the thirteen changes of HMN-DDR-003 (saddle as a V-notched channel, cheeks, four-rod shield, fan and cowl screws, sensor hub, hollow globe hanger, through-mast, end plug, harness route, lanyard loops, V-block adapter, FieldNode Rev P3 envelope), or ask for changes | Accept | Every component of the build plan | HMN-DDR-003, Table 1 |
| 2 | Sensor hub in the air path | (a) keep the hub on three spokes and include it in the TRL 4 shield test; (b) hang the capsule on its lead from a clip on the second plate | (a) | Third shield plate (making sketch HMN-DWG-105) | HMN-DDR-003, A1 |
| 3 | FieldNode panel shading by the sensor head (16 to 44 % of the panel near noon with the sun along the arm) | (a) mount the core above the arm; (b) keep it below and accept the loss, pending FieldNode's bypass diode layout; (c) move the core to the pole's east or west face | (a) | Where the FieldNode core and its adapter go on the pole, the harness length and steps 14 to 16; the plan builds option (b) as modelled until this is decided | HMN-DDR-002, N8; HMN-CAL-001 [E3] |
| 4 | First partner and city for co-design and a pilot | Any city or agency willing to host a network | None made | Not part of the TRL 3 build; sets the pole size, the radio band and the site for TRL 4 | HMN-DDR-001, O1 |
| 5 | Who publishes and hosts the data | TwinKit, CityTwin or a public platform, agreed with the first partner | None made | Not part of the build | HMN-DDR-001, O2 |
| 6 | Sensor port pin assignment, shared with FieldNode's open pinout | The pins of the two M12 ports for the I2C sensor and fan (port A) and the thermistor and anemometer pulse (port B) | Agree with FieldNode's pinout decision (its O2) | Which wires of each lead go to which sensor tail (step 12) | FieldNode FND-DDR-001, O2; HMN-DDR-002 cross-repo actions |
| 7 | Appearance model: FieldNode internals shown as stand-ins (board, module can, cell) | Keep as stand-ins; or remove | Keep, and ask the FieldNode repo to confirm cell format and board position | None (appearance only) | REVIEW.md, 2026-09-26 |
| 8 | Appearance model: vent slots and a HeatMap Node name plate on the FieldNode sun shield | Keep both; keep the name plate only; drop both | Keep the name plate, drop the side slots unless FieldNode adopts them | None at TRL 3; a name plate would be a FieldNode shield change | REVIEW.md, 2026-09-26 |
| 9 | Appearance model: raised seam ring at the globe equator | Accept for appearance; or remove | Accept | None | REVIEW.md, 2026-09-26 |

The arm end cap of the 2026-09-26 appearance review is now part of the design for construction (HMN-DDR-003, P9) and is covered by decision 1.

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
