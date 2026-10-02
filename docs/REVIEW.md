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

1. **Budget (R13).** Options: (a) count the FieldNode core as a shared component budgeted in its own repo, and hold HeatMap Node's $120 to the sensor head (about $120 now); (b) raise `budget_usd` to about $250 for a full node; (c) cut the head to about $70 by dropping the anemometer and using a table tennis ball globe, at a large accuracy cost. Recommendation: (a), with R13 reworded to "sensor head $120 or less". `project.yaml` is unchanged. **Decided by Amish, 2026-09-25: go with recommendation.**
2. **Measurement height (R9).** Options: (a) arm at about 2.8 m with a height correction studied at TRL 3; (b) arm at 2.0 m with tamper-resistant fixings; (c) 1.5 to 2.0 m only on private or school poles. Recommendation: (a) for city poles, with a short pilot comparing 2.0 and 2.8 m. **Decided by Amish, 2026-09-25: go with recommendation.**
3. **Globe size.** 150 mm standard globe (recommended) or a 38 to 40 mm painted table tennis ball globe (cheaper, faster, less comparable). **Decided by Amish, 2026-09-25: go with recommendation.**
4. **Wind.** Fit a cup anemometer (recommended), use a sonic anemometer (better calm-air response, several times the cost) or borrow wind from the nearest official station (cheapest, least accurate). **Decided by Amish, 2026-09-25: go with recommendation.**
5. **Shield.** Naturally ventilated (recommended at TRL 2) or a small fan-aspirated shield powered by FieldNode. **Decided by Amish, 2026-09-25: go with recommendation.** Superseded by the fan decision (item 4 of the TRL 3 session); see HMN-DDR-002.
6. **Derived WBGT** by the Liljegren method rather than a wetted natural wet-bulb sensor. **Decided by Amish, 2026-09-25: go with recommendation.**
7. **Platform.** Build on FieldNode and send data through TwinKit or a public LoRaWAN network. **Decided by Amish, 2026-09-25: go with recommendation.**
8. **Data policy.** Open data under an open license, environmental channels only; publisher and host to be agreed with the first partner. **Decided by Amish, 2026-09-25: go with recommendation.**
9. **First partner and city** for co-design and a pilot network. No recommendation: still Proposed, awaiting Amish.

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

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review (now decided by Amish, 2026-09-25: go with recommendation; see HMN-DDR-002): D1 budget covers the sensor head only (R13 redefined; `budget_usd` unchanged at $120); D2 arm at about 2.8 m with a height correction and a later 2.0 versus 2.8 m pilot (R9 target unchanged); D3 150 mm globe; D4 cup anemometer; D5 naturally ventilated shield; D6 WBGT derived by the Liljegren method; D7 FieldNode core with TwinKit or a public LoRaWAN network; D8 open data, environmental channels only. No reworded pitch or problem line was recommended, so `project.yaml` and `README.md` keep the existing wording.

### Still awaiting Amish

1. **O1, first partner and city** for co-design and a pilot. No preference stated.
2. **O2, data publisher and host.** No recommendation was made.
3. **New, sensor head budget (R13).** Options: (a) raise `budget_usd` to $130; (b) keep $120 and find $10 of savings (for example a formed sheet saddle or a cheaper harness); (c) count the pole adapter against FieldNode, since it fixes a FieldNode fit limit. Recommendation: (c), with a note to the FieldNode project that its kit needs a large-pole variant; this brings the head to $123, so (b) is still needed for a small saving. Not applied. **Decided by Amish, 2026-09-25: go with recommendation.** Applied in the 2026-09-25 recommendations-accepted session below.
4. **New, shield (R1, R5).** Options: (a) keep the passive shield and relax R1 to ±1.0 °C at 1 m/s or more; (b) add a small fan run before each reading (about 30 mW, error about 0.1 °C, WBGT budget ±0.20 °C); (c) keep passive and flag readings when the wind is under 2 m/s in sun. Recommendation: (b), since it fixes R1 and most of R5 within the FieldNode allowance. Not applied; D5 stands until Amish decides. **Decided by Amish, 2026-09-25: go with recommendation.** Applied in the 2026-09-25 recommendations-accepted session below.
5. **New, mass (R15).** Options: (a) relax R15 to 5 kg; (b) keep 4 kg for the sensor head only (2.03 kg). Recommendation: (b), matching the budget split of D1. Not applied. **Decided by Amish, 2026-09-25: go with recommendation.** Applied in the 2026-09-25 recommendations-accepted session below.
6. **New, R8 range.** R8 asks for +60 °C at the node while HMN-PRB-001 states +50 °C. Recommendation: set R8 to +50 °C and adopt FieldNode's proposed sun shield on HeatMap nodes; even at +50 °C the core exceeds its rating without the shield. Not applied. **Decided by Amish, 2026-09-25: go with recommendation.** Applied in the 2026-09-25 recommendations-accepted session below.
7. **New, arm orientation.** The pole shades the globe for about 0.9 h a day when the arm points east or west. Recommendation: point the arm toward the equator where the street allows, with the FieldNode core below it; check panel shading at the first site. Not applied (the model keeps the arm along +X). **Decided by Amish, 2026-09-25: go with recommendation.** Applied in the 2026-09-25 recommendations-accepted session below.
8. **New, anemometer (R4).** Options: (a) relax R4 to "0.8 to 20 m/s" and use the calm-share byte to flag biased intervals; (b) a lower-threshold anemometer at higher cost. Recommendation: (a) for a first pilot. Not applied. **Decided by Amish, 2026-09-25: go with recommendation.** Applied in the 2026-09-25 recommendations-accepted session below.

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

## Session 2026-09-25: recommendations accepted

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item in this note and in HMN-DDR-001 that carried a recommendation is now decided by Amish, 2026-09-25: go with recommendation. The decisions and their effects are recorded in `docs/decisions/0002-recommendations-accepted.md` (HMN-DDR-002 v0.1). Fourteen items were decided: D1 to D8 of HMN-DDR-001 and six TRL 3 items (N1 to N6).

### Decisions applied and what changed

| Decision | Before | After |
| --- | --- | --- |
| D1 to D8 (HMN-DDR-001) | Adopted for TRL 3, open for review | Decided; D5 (passive shield) superseded by N2; D2 pilot on hold (TRL 4) |
| N1 Budget: adapter counted against FieldNode, plus savings | Head $130.00 (adapter $7 inside); saddle 5 mm wall, $8.00, 0.57 kg | Adapter on the FieldNode side; formed 3 mm sheet saddle $5.00, 0.40 kg; head $120.00 before the fan. `budget_usd` stays $120 |
| N2 Fan-aspirated shield | Passive: 1.04 °C at 1 m/s, 2.09 °C at 0.5 m/s; WBGT input budget ±0.59 °C; sensors 0.116 mW | 60 mm 5 V fan and cowl (line 13, $7.00), 6 s every 3 min: 0.43 °C at any wind; ±0.30 °C; 35.4 mW (35 % of allowance). Sensors 25 mm lower (2.67 to 2.69 m) |
| N3 R15 sensor head only | Complete node 4.68 kg against 4 kg, not met | Head 1.91 kg against 4 kg, met on paper (complete node 4.70 kg for information) |
| N4 R8 +50 °C and FieldNode sun shield | R8 at +60 °C; core 78.3 °C at 50 °C air; FieldNode $126.00, 2.41 kg | R8 at +50 °C; core 57.2 °C at 50 °C air; FieldNode $134.00, 2.55 kg; shield in the model |
| N5 Arm toward the equator, core below | Arm along +X, core on the -Y face; pole shades the globe about 0.9 h a day | Arm and core both face +X (the equator); pole shading of the globe near midday removed; new panel shading found (N8) |
| N6 R4 0.8 to 20 m/s, calm flag | R4 0.5 to 20 m/s, not met | R4 restated; server flags an interval when 20 % or more is below start-up; met on paper |

Files changed: `bom/bom.csv` (lines 1, 8, 12 respecified, line 13 added) and `bom/bom-notes.md`; `cad/src/model.py` (formed saddle, fan and cowl, top plate hole, lower shield, FieldNode turned under the arm with its sun shield, harness reroute) and re-exported STEP and STL; `cad/src/sheets.py` and HMN-DWG-001 at Rev P2; `cad/src/concept_media.py` key figures, flow label and exploded offsets, all of `media/` re-rendered (hero, blueprint, exploded, cutaway and flow checked; `_views` folders deleted); `docs/04-calcs/sizing.py` and HMN-CAL-001 v0.2; HMN-REQ-001 v0.4, HMN-PRC-001 v0.4, HMN-PRB-001 v0.4, HMN-DDR-001 v0.2, new HMN-DDR-002 v0.1; `README.md` (budget line, Concept, components, safety, and a rewritten "What sparked the idea"); `project.yaml` evidence list. All PDFs rebuilt, and every generated file now shows designmolecule.com.

### Requirement status (HMN-CAL-001 v0.2, Table 2)

2 not met, 3 at risk, 8 met on paper, 2 met by design (before: 6, 3, 4, 2).

| ID | Status | Key number |
| --- | --- | --- |
| R9 Height | **Not met** | Sensors at 2.67 to 2.69 m; pedestrian-height air 0.2 to 0.8 °C warmer in strong sun |
| R13 Cost | **Not met** | Sensor head $127.00 against $120 (fan and cowl $7) |
| R5 WBGT | At risk | ±0.30 °C RSS input budget; Liljegren model error unknown |
| R10 Fit and time | At risk | 37 min against 30 min |
| R14 Traceability | At risk | Assembled globe does not fit a CalRig bay |
| R1, R3, R4, R6, R7, R8, R11, R15 | Met on paper | R1 0.43 °C (fan flow assumed); R7 35.4 mW (panel shading not included); R8 57.2 °C; R11 factors 13.4 and 2.5; R15 1.91 kg |
| R2, R12 | Met by design | |

### Still awaiting Amish

1. **O1, first partner and city.** No preference stated, no recommendation.
2. **O2, data publisher and host.** No recommendation.
3. **N7, sensor head budget after the fan.** $127.00 against $120. Options: (a) raise `budget_usd` to $130; (b) keep $120 and cut $7 more (for example a cheaper anemometer class, at the cost of R4); (c) count the fan against a separate accuracy option. Recommendation: (a). **Decided by Amish, 2026-09-26: budget top-up to $130 (option a), applied in the session below.**
4. **N8, FieldNode panel shading.** With the core below the arm and both facing the equator, the shield, cowl, globe and arm shade 44, 34, 27 and 16 % of the panel with the sun along the arm at 30, 45, 60 and 75° elevation (HMN-CAL-001 [E3]). Options: (a) mount the core above the arm; (b) keep it below and accept the loss pending FieldNode's bypass diode layout; (c) move the core to the pole's east or west face. Recommendation: (a). Not applied.

### Cross-repo actions (other repos not edited)

- **FieldNode:** add a large-pole kit variant (V-blocks for 60 to 200 mm poles) so that HeatMap's line 12 adapter, now counted against FieldNode, becomes a FieldNode part (N1).
- **FieldNode:** HeatMap nodes use the hot-climate build with the sun shield ($134.00, 2.55 kg), as FieldNode's own cross-repo note expected (N4).
- **FieldNode:** the port assignment assumed here (5 V switched rail on the temperature and humidity port powering the fan and sensor) should be considered when FieldNode's pinout (its O2) is set; and FieldNode's energy budget should allow for partial panel shading if N8 option (b) is chosen.
- **CalRig:** unchanged; the probe is still calibrated before it is fitted to the globe.

### Safety

- The shield fan starts on its own every 3 min; unplug the sensor lead before working on the shield.
- The FieldNode sun shield keeps the cell within its charge limits at hot sites and must not be left off.
- The node now adds about 337 N·m at the pole base at 35 m/s; the pole owner must check it. The clamp twist factor is 2.5, the smallest margin; installers need a torque figure, and the formed sheet saddle's stiffness is to be checked at detail design.
- Work at height, hot surfaces and data misuse notes are unchanged.

### TRL 4

TRL 4 remains on hold by Amish's instruction. `trl` and `trl_target` stay at 3. The 2.0 versus 2.8 m pilot, the site check of panel shading, choice and testing of the fan, a side-by-side shield test, firmware for the fan timing and calm flag, and any purchasing are decided where applicable but not started.

### Notes

- The fan figures (0.9 W, 6.6 L/s free air, 60 % delivered, 2 s sensor time constant) are class values and assumptions, not a chosen part. The earlier estimate of about 30 mW for 0.1 °C assumed 3 m/s across the whole 60 cm² stack section, which a 0.3 W fan cannot deliver; the revised figures give 35 mW for 0.43 °C.
- "What sparked the idea" now cites the 1950s US Marine Corps heat flags and the 1957 origin of WBGT (HPRC; Budd, 2008). The Budd abstract was read through the publisher's page; the Parris Island location given in secondary sources was left out because no primary source for it could be opened.

## Session 2026-09-26: sources strengthened

### Sources

Every link in "Concept rationale", "Burning platform", "Where it could be used" and "What sparked the idea" was fetched again and checked against the sentence it supports: WHO heat and health fact sheet (489,000 deaths a year, 45 % in Asia, 36 % in Europe, informal settlements), Ballester et al. 2023 (61,672 deaths in 35 countries), US EPA heat islands (1 to 7 °F by day), Hoffman et al. 2020 (2.6 °C, up to 7 °C), Hsu et al. 2021 (all but 6 of 175 urbanized areas), WMO Africa report release (+0.3 °C per decade 1991 to 2022, observation gaps, most rapid warming in North Africa), ISO 7243:2017, the DoD Human Performance Resource Center heat flag page, Liljegren et al. 2008 and Budd 2008 (bibliographic records confirmed through Crossref). All are primary sources, peer-reviewed papers or official agency pages, and every country or region row carries a citation that supports it.

- Replaced: none. No Wikipedia, blog or trade-press link was found in scope, and no row needed replacing.
- "What sparked the idea" is unchanged (HPRC, US Department of Defense; Budd, 2008). Its INSPIRATIONS.md line is unchanged.
- Not re-read this session: the Budd (2008) abstract text (publisher page and Europe PMC unavailable; PubMed returned a CAPTCHA). The claim that WBGT cut heat casualties and lost training time rests on the reading of the publisher page recorded in the session above. The heat-death figures left out in the first session (Maricopa County, Ahmedabad, Singapore NEA, NOAA campaigns) remain out.

### Budget

- N7 decided by Amish, 2026-09-26 ("I am ok with the budget top ups"): `budget_usd` $120 to $130 in `project.yaml`.
- `docs/04-calcs/sizing.py` reads `budget_usd` and was re-run: [L2] now reads "sensor head within by $3.00". R13 not met to met on paper.
- Requirement status: 1 not met (R9), 3 at risk (R5, R10, R14), 9 met on paper, 2 met by design.
- Documents revised: HMN-REQ-001 v0.5, HMN-CAL-001 v0.3, HMN-DDR-002 v0.2, HMN-PRC-001 v0.5, HMN-PRB-001 v0.5 (budget constraint only); `README.md` budget line and Concept paragraph; `bom/bom-notes.md`.
- Concept media: the blueprint key figure in `cad/src/concept_media.py` now reads "budget $130"; all of `media/` was regenerated and the temporary `_views` folders deleted.
- Still awaiting Amish: O1, O2 and N8.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26.

### What was done

- New `cad/src/product_model.py`: `product_parts()` returns 65 named parts (49 shell, 11 internal, 4 accessory, 1 context), each with a colour, a render material, its BOM line and an exploded-view offset. It imports PARAMS, `derived()` and the `path` and `rod` helpers from `cad/src/model.py`, so every main dimension, height and interface is unchanged. It also defines `TITLE` and three `RENDER_VIEWS`: hero (on a short section of the existing street pole), exploded and detail (without the pole).
- What the appearance model adds: filleted arm tube with a black end cap and an identity label with the teal accent; the V-saddle with rounded edges, a rubber liner, bolt heads, and strap bands with buckles and screws; eight shield plates with rounded edges on stainless rods with top nuts and acorn nuts; the aspiration fan as a frame, a seven-blade rotor and a hub label under the white cowl; the temperature and humidity capsule with a PTFE membrane cap and an M12 connector; the matte black globe with its seam flange, a brass boss and a probe gland, and the probe stem and bead inside; the anemometer as mast, body, teal rotor cap and cups; the harness with an M12 plug, cable ties along the arm and the stainless lanyards; the FieldNode core as back plate, enclosure base and lid with a parting line and lid screws, sun shield with a name plate, solar panel frame with cells, busbars and a junction box, support bars, whip antenna with base nut, M12 sockets and a vent plug; and the pole adapter V-blocks and strap bands.
- `README.md`: the hero image now points to `media/render-hero.png`, and the links line starts with the exploded render. The render files are produced separately and were not created in this session.
- Matplotlib previews were checked for the hero, exploded and detail views (kept outside the repo). All shapes are valid and tessellate; `.kit/product_export.py` exports all 65 parts.

### Differences from model.py

Each item below is appearance only, and none changes a PARAMS value.

- **FieldNode internals and split enclosure.** The model treats the FieldNode core as an envelope. The appearance model splits the enclosure into a base and a front lid and shows a board, a LoRaWAN module can and a horizontal 32 mm LiFePO4 cell inside, so the exploded view can show the board and battery. These are stand-ins; FND-DWG-001 and the FieldNode BOM define the real parts. Proposed, awaiting Amish. Recommendation: keep them as stand-ins and ask the FieldNode repo to confirm the cell format and board position at its next update.
- **Vent slots and name plate on the FieldNode sun shield.** Four vent slots in each side sheet and a HeatMap Node name plate on the front are not in FND-DWG-001. Proposed, awaiting Amish. Recommendation: keep the name plate (it identifies the node to the public and the pole owner) and drop the side slots unless FieldNode adopts them, since its sun shield is already ventilated through the top slot and open bottom.
- **Arm end cap.** A 2.5 mm black plug is drawn beyond the arm tip, so the arm reads 2.5 mm longer than `arm_len`; the overall reach is set by the anemometer cups and is unchanged. Proposed, awaiting Amish. Recommendation: accept, and add a plug to BOM line 10 at the next BOM revision.
- **Globe seam flange.** A 1.2 mm raised seam ring is drawn at the globe equator, as on pressed float balls. Proposed, awaiting Amish. Recommendation: accept for appearance; its effect on the globe reading is negligible at this TRL.
- **Harness start.** The harness is drawn from the M12 plug under the FieldNode port instead of from inside the port; routing is otherwise the same.

### TRL

This is an appearance model only: no tolerances, no fabrication detail, no PCB layout. `trl` and `trl_target` stay at 3, and TRL 4 remains on hold.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-01: design for construction and prototype build plan (kit 1.7.0)

Under Amish's 2026-09-30 instruction to make the design physically buildable and to write an illustrated build plan ("fix the design assumptions to match and be physically feasible"), and his 2026-10-01 note that `budget_usd` is a value-engineering target. Kit 1.7.0 installed (`.kit/`, `.claude/commands/`, `CLAUDE.md`).

### Design changes made for construction (HMN-DDR-003, Draft, open for Amish's review)

1. Arm saddle: a channel bent from 3 mm 5052 sheet, 120 x 180 x 40 mm (was a 110 mm tray with a round seat for one pole size), with 120° V notches in its flanges lined with rubber edge trim; seats 60 to 200 mm poles.
2. Arm fixing: two 40 x 40 x 3 mm angle cheeks on the saddle web (four M6 button-head screws); the arm bolted between them by two M6 bolts through crush sleeves.
3. Saddle bands: through four 3 x 16 mm web slots and across the web front (were rings through the saddle).
4. Shield: four M5 rods on a 92 mm circle, clear of the cowl (were three, two inside the cowl); printed 12 mm bosses set the plate gaps; two rods continue through the arm on 41 mm spacers (the unfixed central hanger rod is gone).
5. Fan and cowl: fan flat on the top plate; cowl on four legs over the fan's corner holes; four M4 x 40 screws through cowl, fan and plate.
6. Sensor: held in a hub on three spokes printed on the third plate, with a nylon set screw.
7. Globe: hung on a hollow M10 x 1 brass tube nutted above and below the arm; the probe runs down inside it (the solid hanger rod met the probe).
8. Anemometer: mast through the arm, pinned by one M5 bolt; arm 530 mm (was 520 mm); reach 668 mm (was 679 mm).
9. Arm end plug added.
10. Harness rerouted round every part: up the pole outside the bands, round the saddle side, along the arm's left side, tails between the plates, to the hanger tube top and into the mast foot.
11. Lanyards looped round the arm with snap hooks.
12. FieldNode pole adapter: printed 120° V-blocks 110 x 30 x 38 mm with band slots in line with FieldNode's plate slots and M4 heat-set inserts at its V-block screw holes (were flat blocks for one pole size covering the slots).
13. FieldNode envelope updated to FND-DWG-001 Rev P3; FieldNode figures to $148.00 and 2.61 kg after FND-DDR-003.

`python cad/src/model.py --check`: 399 constructability checks (no overlaps, contacts, clearances, pole range), all pass.

### What was done, with file paths

- `cad/src/model.py`: rebuilt as separate components (`build_components`) with the changes above and the checks; STEP and STL re-exported (`cad/step/`, `cad/stl/`).
- `bom/bom.csv` lines 1, 2, 4, 6, 7, 8, 10, 12 and 13 respecified; `bom/bom-notes.md` updated.
- `docs/04-calcs/sizing.py` (mass now from the component volumes) re-run; HMN-CAL-001 v0.4, HMN-REQ-001 v0.6, HMN-PRC-001 v0.6.
- `cad/drawings/HMN-DWG-001` Rev P4; making sketches `HMN-DWG-101` to `107` (saddle, cheek, arm, top plate, ring plates, cowl, adapter V-block).
- `cad/src/build_plan_media.py`: overview, arm hole layout, 8 joint close-ups and 16 assembly step pictures in `docs/05-build-plan/`.
- New `docs/05-build-plan.md` (HMN-BLD-001), `docs/06-design-decisions.md` (HMN-DEC-001), `docs/decisions/0003-design-for-construction.md` (HMN-DDR-003).
- Concept media regenerated (`media/hero.png`, `concept-blueprint.*`, `exploded.png`, `cutaway.png`, `flow.png`, `model.glb`, `viewer.html`).
- `project.yaml`: `design_state: constructable`; the build plan, register and HMN-DDR-003 added to `trl_evidence`; `budget_usd` unchanged. `README.md`: links line, value-engineering line, Concept figures and a "Building the prototype" section.

### Key results

- Sensor head 2.12 kg (was 1.91 kg) against 4 kg (R15 met on paper); complete node 4.95 kg.
- Value-engineering target: USD 130. Estimated cost of the constructable design: USD 136 (USD 6 over the target). Full node about USD 292.
- Arm factor 13.0 on yield, tip 0.31 mm at 20 m/s, clamp twist factor 2.5 (R11 met on paper, preload assumed).
- Requirement status: 1 not met (R9, measurement height), 3 at risk (R5, R10, R14), 8 met on paper, 2 met by design, R13 $6 over its value-engineering target.

### Decisions proposed and awaiting Amish

All open items are in `docs/06-design-decisions.md`: accept HMN-DDR-003; the sensor hub spokes in the air path (A1); FieldNode panel shading (N8); first partner and city (O1); data publisher (O2); port pinout shared with FieldNode; three appearance-model items from 2026-09-26.

### Stale media (made on Amish's Mac, not regenerated here)

The design changed visibly, so `media/render-hero.png`, `media/render-exploded.png`, `media/render-detail.png`, `media/card.png` and `media/social-preview.png` and the appearance model `cad/src/product_model.py` are stale (they show the tray saddle, three-rod shield and solid globe rod). The `media/render-*.png` files are not in this cloud copy, so the README hero image and render links do not resolve here.

### Safety

No change to the safety case. The build plan adds safety stops for work at height, the FieldNode cell (its own plan), and the self-starting fan, hot globe and spinning cups. Clamp preload still carries the smallest margin (twist factor 2.5); the band tool setting is an item to confirm.

### Recommended next step

Amish's review of HMN-DDR-003 and the register. TRL 4 (building to HMN-BLD-001 and testing) stays on hold by his instruction.

## Session 2026-10-02: open decisions decided

Amish approved every recommendation for the open decisions on 2026-10-02: "i approve your recommendations for all 555 open decisions."

### Decisions recorded

Nine, all moved to "Decisions made" in HMN-DEC-001 (open items 1 to 9): design for construction accepted (HMN-DDR-003); sensor hub kept on three spokes and included in the TRL 4 shield test; FieldNode core above the arm if its lid stays reachable, otherwise on the pole's east or west face; a hot US city with a dedicated heat office first, with the City of Phoenix Office of Heat Response and Mitigation as the first candidate to approach, on US915; data through a TwinKit gateway and published from CityTwin's open data export under an open licence, with Amish's lab as publisher until the city takes it over; FieldNode's candidate pinout adopted for the two sensor ports; FieldNode internals kept as stand-ins in the appearance model; name plate kept and side vent slots dropped; raised seam ring accepted.

### Documents changed

- `docs/06-design-decisions.md` HMN-DEC-001 v0.2: decisions made; open decisions section now reads "None".
- `docs/decisions/0003-design-for-construction.md` HMN-DDR-003 v0.2: accepted (status Draft kept); A1 as recommended.
- `docs/01-problem.md` HMN-PRB-001 v0.6: first partner city and data publisher.
- `docs/02-concept.md` HMN-PRC-001 v0.7: core position and data publishing; open questions answered.
- `docs/04-calcs/01-sizing.md` HMN-CAL-001 v0.5: panel shading text notes the decided core position; no figures changed.
- `docs/05-build-plan.md` HMN-BLD-001 v0.2: step 12 gives the decided port pinout.

### Follow-up actions to carry approved decisions into the design

1. Decision 3 (model): move the FieldNode core and its adapter above the arm in `cad/src/model.py`, or to the pole's east or west face if its lid cannot be reached from the ladder or lift there; re-run the constructability check.
2. Decision 3 (pictures, drawings): redraw steps 14 to 16, the overview and the adapter making sketch for the new core position, and update the build plan text of those steps.
3. Decision 3 (BOM): re-specify the harness lead length (line 9) for the new core position.
4. Decision 3 (calculations): rerun the panel shading [E3], the wind load and the clamp check for the core above the arm, and check the core height against FieldNode's decided 1.75 m mounting height.
5. Decision 2 (docs): put the hub and spokes in the TRL 4 side-by-side shield test plan.
6. Decision 6 (docs): ask the FieldNode repo to adopt the same pinout as its O2 decision, so that both repos agree.
7. Decision 7 (docs): ask the FieldNode repo to confirm the cell format and board position at its next update, then update the stand-ins.
8. Decision 8 (pictures): drop the side vent slots from `cad/src/product_model.py`, keep the name plate, and re-render on Amish's Mac.

### Points found in the review

- R9 (sensors at 1.1 to 2.0 m) is not met, with sensors at about 2.68 m, yet no open decision addresses it; either restate R9 around the height correction already decided or add an item.
- Item 3 says the plan builds option (b) until decided; if option (a) is chosen, steps 14 to 16 and the harness length change, and the core rises above FieldNode's decided 1.75 m mounting height.
- Sensor head cost is $136 against the $130 target, $6 over; the full node is $292.
