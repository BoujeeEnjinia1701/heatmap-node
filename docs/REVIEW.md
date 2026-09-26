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

## Session 2026-09-25: TRL 3

On 2026-09-25 Amish asked for this batch of repos to go through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's TRL 2 items one by one, so every item that carried a recommendation is adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. This session ran `/advance-trl3` on that basis and stopped at TRL 3.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (HMN-DDR-001 v0.1, status proposed): eight items adopted as recommended for TRL 3, open for Amish's review (D1 to D8), and two left open (O1, O2).
- `docs/04-calcs/01-sizing.md` (HMN-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: mean radiant temperature, natural wet bulb and WBGT with an error budget, shield radiation error, globe and probe response and calibration, height correction and pole shading, sensor power, payload and storage, wind on the arm and clamp, outdoor temperatures, fit and installation time, mass and cost, with a status for every requirement. The script imports the model, reads the BOM and `project.yaml`, and prints every number the note quotes.
- `cad/src/model.py`: parametric build123d model (V-saddle and bands, arm with hangers, eight-plate shield, sensor, globe with probe, anemometer, lanyards, harness, FieldNode core envelope from FND-DWG-001 and a wider pole adapter). Exports `cad/step/` and `cad/stl/` for `heatmap-node-assembly`, `sensor-head` and `fieldnode-core-envelope`.
- `cad/src/sheets.py` and `cad/drawings/HMN-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, 1:10, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". HMN-DWG-001 was free because the concept blueprint is HMN-DWG-010.
- `bom/bom.csv` (12 lines, all priced with a supplier or supplier type) and `bom/bom-notes.md`. Added line 11 (secondary retention lanyards, $3, the TRL 2 safety note asked for them) and line 12 (FieldNode pole adapter, $7).
- `cad/src/concept_media.py` now builds from the model; all of `media/` re-rendered and every image checked; temporary `_views` folders deleted. The FieldNode core now faces -Y (the FieldNode convention), so the cutaway leaves out the core, adapter, harness, lanyards and clamp; the cut then passes through the shield and globe. The scene is still shifted down by the arm height for the kit's cutter.
- HMN-PRB-001, HMN-PRC-001 and HMN-REQ-001 revised to v0.3; `README.md` (TRL line, links, key figures, components, safety) and `project.yaml` (`trl: 3`, `trl_target: 3`, evidence list) updated. PDFs rebuilt in `docs/pdf/`.

### Requirement status (HMN-CAL-001, Table 2)

6 not met, 3 at risk, 4 met on paper, 2 met by design.

| ID | Status | Key number |
| --- | --- | --- |
| R1 Air temperature | **Not met** | Passive shield about 1.04 °C high in full sun at 1 m/s, 2.09 °C at 0.5 m/s (targets ±0.5 and ±1.0 °C); assumption-sensitive |
| R4 Wind | **Not met** | Start-up about 0.8 m/s against 0.5 m/s; reading zero at a true 0.5 m/s puts MRT 8.2 °C low |
| R8 Outdoor survival | **Not met** | FieldNode interior 78.3 °C at 50 °C air, 88.3 °C at 60 °C, against a 70 °C rating (from FND-CAL-001) |
| R9 Height | **Not met** | Sensors at 2.67 to 2.71 m; pedestrian-height air 0.2 to 0.8 °C warmer in strong sun |
| R13 Cost | **Not met** | Sensor head $130.00 against $120 |
| R15 Mass | **Not met** | 4.68 kg against 4.0 kg (FieldNode 2.41 kg, not the 1.7 kg assumed at TRL 2) |
| R5 WBGT | At risk | Input errors ±0.59 °C RSS, ±0.88 °C worst; +0.9 °C in calm air; Liljegren model error not known |
| R10 Fit and time | At risk | Fits 60 to 200 mm; 37 min against 30 min |
| R14 Traceability | At risk | Assembled 150 mm globe does not fit a CalRig bay; the probe fits if calibrated before assembly |
| R3, R6, R7, R11 | Met on paper | Probe ±0.18 °C, 90 % response about 12 min; 20 B payload, 21.5 kB for 7 days; 0.116 mW; arm factor 13.8, clamp twist factor 2.6 |
| R2, R12 | Met by design | |

Key numbers: worked example MRT 74.8 °C and WBGT 31.7 °C; sensor head 44.1 N at 35 m/s; about 314 N·m added at the pole base; full node $256.00.

### Decisions recorded (HMN-DDR-001)

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review: D1 budget covers the sensor head only (R13 redefined; `budget_usd` unchanged at $120); D2 arm at about 2.8 m with a height correction and a later 2.0 versus 2.8 m pilot (R9 target unchanged); D3 150 mm globe; D4 cup anemometer; D5 naturally ventilated shield; D6 WBGT derived by the Liljegren method; D7 FieldNode core with TwinKit or a public LoRaWAN network; D8 open data, environmental channels only. No reworded pitch or problem line was recommended, so `project.yaml` and `README.md` keep the existing wording.

### Still awaiting Amish

1. **O1, first partner and city** for co-design and a pilot. No preference stated.
2. **O2, data publisher and host.** No recommendation was made.
3. **New, sensor head budget (R13).** Options: (a) raise `budget_usd` to $130; (b) keep $120 and find $10 of savings (for example a formed sheet saddle or a cheaper harness); (c) count the pole adapter against FieldNode, since it fixes a FieldNode fit limit. Recommendation: (c), with a note to the FieldNode project that its kit needs a large-pole variant; this brings the head to $123, so (b) is still needed for a small saving. Not applied.
4. **New, shield (R1, R5).** Options: (a) keep the passive shield and relax R1 to ±1.0 °C at 1 m/s or more; (b) add a small fan run before each reading (about 30 mW, error about 0.1 °C, WBGT budget ±0.20 °C); (c) keep passive and flag readings when the wind is under 2 m/s in sun. Recommendation: (b), since it fixes R1 and most of R5 within the FieldNode allowance. Not applied; D5 stands until Amish decides.
5. **New, mass (R15).** Options: (a) relax R15 to 5 kg; (b) keep 4 kg for the sensor head only (2.03 kg). Recommendation: (b), matching the budget split of D1. Not applied.
6. **New, R8 range.** R8 asks for +60 °C at the node while HMN-PRB-001 states +50 °C. Recommendation: set R8 to +50 °C and adopt FieldNode's proposed sun shield on HeatMap nodes; even at +50 °C the core exceeds its rating without the shield. Not applied.
7. **New, arm orientation.** The pole shades the globe for about 0.9 h a day when the arm points east or west. Recommendation: point the arm toward the equator where the street allows, with the FieldNode core below it; check panel shading at the first site. Not applied (the model keeps the arm along +X).
8. **New, anemometer (R4).** Options: (a) relax R4 to "0.8 to 20 m/s" and use the calm-share byte to flag biased intervals; (b) a lower-threshold anemometer at higher cost. Recommendation: (a) for a first pilot. Not applied.

### Cross-repo consistency

- FieldNode (FND REVIEW, FND-CAL-001): mass 2.41 kg, cost $126.00, 100 mW design allowance, 32 B records, 23.7 s/day at SF9 and 81 N at 35 m/s are used as published. Conflict noted, FieldNode not edited: FieldNode's 50 mm V-blocks seat only on poles up to about 71 mm, while HeatMap Node mounts on 60 to 200 mm street poles; this repo adds its own adapter (line 12). FieldNode's interior temperature (its R3, not met) makes HeatMap R8 not met.
- CalRig (CLR REVIEW): the reference uncertainty (0.14 °C typical, 0.24 °C at maximum tolerance) is used for R3. CalRig already notes that the 150 mm globe exceeds its 90 x 70 x 50 mm bay; HeatMap Node proposes calibrating the probe before it is fitted, so only the probe needs a bay. No CalRig edit.
- TwinKit: the 1.02 % worst-case uplink loss is used for R6 latency; no conflict.

### Safety concerns

- Work at height next to traffic and overhead lines; the node adds about 314 N·m at the pole base at 35 m/s, which the pole owner must check.
- Clamp preload carries the smallest margin (twist factor 2.6 at an assumed 1,000 N per band); installers need a torque figure.
- Falling parts: stainless lanyards now back the globe and shield fixings.
- FieldNode LiFePO4 cell (about 19 Wh) overheats at the top of the ambient range without FieldNode's proposed shield; the 45 °C charge lockout must never be defeated.
- Hot surfaces: the globe reaches about 67 °C at 50 °C air.
- Misuse of the data as a warning or as a fitness-to-work decision for an individual.

### Gaps and notes

- Citations: the SHT45 accuracy was checked on the Sensirion product page. The globe equation's ISO 7726:1998 attribution and the 0.15 m and 0.95 defaults were checked in the pythermalcomfort documentation; the coefficients 6.3 and 1.4 were not read from the standard itself (the standard and a Wiley paper returned 403 or did not show them). Still not found by WebFetch: NOAA heat mapping campaign figures (heat.gov pages have no counts) and Maricopa County heat death counts (the page links PDFs only). Singapore NEA and Ahmedabad were not retried. The anemometer start-up speed has no source. Nothing was added to the README from these.
- The shield error, height correction and globe response rest on assumptions that only tests can settle. The wet-bulb model is a simplified stand-in for the Liljegren code.
- Existing material beyond TRL 3: `build-log/README.md` (scaffold) is present, untouched and not extended. No test, build or firmware material exists.

### Recommended next step

TRL 4 is on hold by Amish's instruction; this repo stops at TRL 3. Amish's review is needed on D1 to D8 and on items 1 to 8 above. For the record only, TRL 4 would need: a bench build of the sensor head on a FieldNode core; a lab test report (TST, `environment: lab`) covering the shield error against an aspirated reference in simulated sun with and without a fan, globe step response, probe calibration in CalRig, anemometer start-up, and clamp preload and slip on 60 and 200 mm poles; and build log entries. None of this has been started.
