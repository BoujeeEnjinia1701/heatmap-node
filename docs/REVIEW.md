# Review note: HeatMap Node

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (HMN-PRB-001 v0.2): problem with cited figures, users, operating environment, constraints, out of scope, prior work, open questions; co-design checklist kept.
- `docs/03-requirements.md` (HMN-REQ-001 v0.2): 15 measurable requirements (R1 to R15) and a status table against the concept estimates.
- `docs/02-concept.md` (HMN-PRC-001 v0.2): how it works, numbered components, globe-to-MRT and WBGT method with a worked example and sensitivity, power, radio, wind load, mass, cost, design choices, safety, open questions.
- `cad/src/concept_media.py`: massing model of the sensor arm, shield, globe, probe, anemometer, clamp, harness and FieldNode core on a 114 mm street pole. The pole and a 1.75 m person are context parts (hero and isometric only), so the exploded and cutaway views stay readable. The model is shifted so the arm sits at Z = 0 because the kit's cutaway cutter is centered on Z = 0; ground is at Z = -2.8 m.
- `media/`: hero, concept blueprint (PNG, PDF, SVG), cutaway (sensor in shield, probe in globe), exploded view with BOM callouts 1 to 9, data flow diagram (values labeled as estimates), `model.glb` and `viewer.html`. Temporary `_views` folders removed.
- `bom/bom.csv` (10 lines, indicative prices) and `bom/bom-notes.md`.
- `README.md`: hero and links line; Concept rationale, Burning platform, Where it could be used (industry and region tables), What sparked the idea expanded with cited sources; Problem, Concept, Key components and Safety updated.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml`: unchanged (pitch and problem remain consistent with the sources found).

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Worked example (35 °C, 40 %RH, 50 °C globe, 1 m/s) | MRT about 75 °C; WBGT about 31 °C | R5 |
| MRT sensitivity to wind (0.5 / 1.5 m/s instead of 1 m/s) | about 67 / 80 °C | R4, R5 at risk |
| Sensor power | under 1 mW, against about 115 mW FieldNode allowance | R7 met |
| Radio | 96 uplinks of about 20 B a day; 7 days of data about 13 kB | R6 met |
| Wind load at 35 m/s | about 110 N total; about 17 N·m at the arm root | R11 met by estimate |
| Mass | about 3.3 kg | R15 met |
| Arm height | about 2.8 m | **R9 not met** |
| Sensor head cost (BOM lines 2 to 10) | about $120 | R13 met with no margin |
| Full node cost with FieldNode core | about $246 | **R13 not met, about twice the $120 budget** |

Requirements not met: **R4** (anemometer start-up about 0.8 m/s, above the 0.5 m/s target), **R9** (sensors not at pedestrian height), **R13** (full node cost). At risk: **R1** (passive shield error in calm sun), **R5** (WBGT accuracy in calm air), **R15** (if a larger panel is needed).

### Proposed, awaiting Amish

1. **Budget (R13).** Options: (a) count the FieldNode core as a shared component budgeted in its own repo, and hold HeatMap Node's $120 to the sensor head (about $120 now); (b) raise `budget_usd` to about $250 for a full node; (c) cut the head to about $70 by dropping the anemometer and using a table tennis ball globe, at a large accuracy cost. Recommendation: (a), with R13 reworded to "sensor head $120 or less". `project.yaml` is unchanged.
2. **Measurement height (R9).** Options: (a) arm at about 2.8 m with a height correction studied at TRL 3; (b) arm at 2.0 m with tamper-resistant fixings; (c) 1.5 to 2.0 m only on private or school poles. Recommendation: (a) for city poles, with a short pilot comparing 2.0 and 2.8 m.
3. **Globe size.** 150 mm standard globe (recommended) or a 38 to 40 mm painted table tennis ball globe (cheaper, faster, less comparable).
4. **Wind.** Fit a cup anemometer (recommended), use a sonic anemometer (better calm-air response, several times the cost) or borrow wind from the nearest official station (cheapest, least accurate).
5. **Shield.** Naturally ventilated (recommended at TRL 2) or a small fan-aspirated shield powered by FieldNode.
6. **Derived WBGT** by the Liljegren method rather than a wetted natural wet-bulb sensor.
7. **Platform.** Build on FieldNode and send data through TwinKit or a public LoRaWAN network.
8. **Data policy.** Open data under an open license, environmental channels only; publisher and host to be agreed with the first partner.
9. **First partner and city** for co-design and a pilot network.

### Safety concerns

- Work at height next to traffic, near overhead lines and on lighting poles that may carry mains voltage: asset owner permission, trained crews, traffic management.
- About 19 Wh LiFePO4 cell in the FieldNode core: fusing, charge temperature limits.
- Hot surfaces (globe and arm above 60 °C in sun, estimate), deburring of cut edges, spinning cups.
- Misuse of data as a warning or as a fitness-to-work decision for individuals; the docs state it is for planning and research only.
- Falling parts from a pole: arm and globe fixings need a secondary retention (for example a lanyard) at TRL 3.

### Problems and notes

- WebSearch was unavailable this session. Sources were verified by fetching pages directly. Could not be read and so left out: NOAA heat mapping campaign figures (heat.gov pages had no figures), Maricopa County heat death counts, Singapore NEA WBGT network, Ahmedabad heat action plan outcomes (NRDC page 404, publisher 403, Europe PMC rate limited). The Liljegren et al. (2008) citation was verified through the README of the open `wbgt` package, as the publisher page returned 403.
- The forced-convection globe equation and the sensor accuracy classes (SHT45, low-cost anemometer start-up) are stated without a source and marked for confirmation at TRL 3.
- FieldNode's pole kit fits 40 to 60 mm poles; HeatMap Node needs longer bands. This is a local BOM note, not a change to FieldNode.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).

### Recommended next step

Review this note and the media, then decide items 1 and 2. If approved, run `/advance-trl3` to write the calculation note (globe equation and source, shield error, wind sensitivity, wind load), produce the parametric model and drawing sheet, and define the CalRig procedure for the globe and humidity sensors.
