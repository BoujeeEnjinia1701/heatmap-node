---
doc_id: HMN-CAL-001
title: HeatMap Node sizing calculations
project: HeatMap Node
doc_type: Calculation
version: "0.6"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (mean radiant temperature, natural wet bulb and WBGT error budget, shield error, globe response and probe, height and shading, power, data, wind and clamp, outdoor temperatures, fit and installation, mass, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-09-26'
  author: Amish Chadha
  change: "Budget top-up approved by Amish: R13 target $130, script re-run"
- version: "0.4"
  date: '2026-10-01'
  author: Amish Chadha
  change: Design for construction (HMN-DDR-003); mass from the constructable model; FieldNode figures after FND-DDR-003; cost reported against the value-engineering target
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Panel shading text notes the core position decided on 2026-10-02; no figures changed"
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Core moved above the arm in the model (2026-10-02): panel shading rerun (E3, new E3b), added pole moment 423 N m, shorter harness, head 2.08 kg; no requirement status changes"
---

# HeatMap Node sizing calculations

On paper, HeatMap Node meets or is on track for thirteen of its fifteen requirements; one is not met, and the sensor head's estimated cost is $6 over its value-engineering target. Version 0.2 applies the decisions Amish accepted on 2026-09-25 (HMN-DDR-002): a small fan aspirates the radiation shield before each air reading, R4, R8, R13 and R15 are restated, the saddle is formed from sheet, the arm points toward the equator with the FieldNode core (since 2026-10-02, above it), and the FieldNode core carries FieldNode's hot-climate sun shield. The heat stress method is unchanged: in the worked example (35 °C air, 40 %RH, 50 °C globe, 1 m/s wind) mean radiant temperature is 74.8 °C and WBGT is 31.7 °C, and with the fan the input errors add up to ±0.30 °C of WBGT (root sum square), against ±0.59 °C with the passive shield. The one miss is R9, because the sensors sit at about 2.7 m, where the air is 0.2 to 0.8 °C cooler than at pedestrian height on a sunny afternoon. Version 0.3 applies the budget top-up Amish approved on 2026-09-26 (HMN-DDR-002 v0.2): `budget_usd` became $130, and the $127 sensor head was then $3 under it. Version 0.4 follows the design for construction (HMN-DDR-003): the parts added to make the node buildable bring the sensor head to 2.12 kg and $136.00, $6.00 over the $130 value-engineering target (`budget_usd` is a hypothetical control target, not a limit: Amish, 2026-10-01), and the 530 mm arm changes the wind figures slightly. The new orientation raised one problem: with the core below the arm, the shield, globe and arm shaded 16 to 44 % of the FieldNode panel near noon (section E). Version 0.6 carries the decision of 2026-10-02 into the model: the core is above the arm (bottom at 3.11 m), the panel is no longer shaded by the head (0 % in every case run), the harness leads are shorter (1.2 m and 1.4 m), and the added moment at the pole base rises from 338 to 423 N·m. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [A1], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that a place is safe or unsafe for people, and HeatMap Node data must not be used to decide whether a particular person may work or exercise. Pole mounting, the pole's added wind load and the FieldNode cell are safety matters; see HMN-PRC-001, Safety.

## Scope and method

The note checks every requirement in HMN-REQ-001 v0.6 against the design in HMN-PRC-001 v0.6 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, derived dimensions and part solids, so the heights, lengths, areas and volumes used here are those in the STEP files and in drawing HMN-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. FieldNode figures (mass, cost, wind load, interior temperature, airtime, sensor allowance) are quoted from FND-CAL-001 (v0.4 for mass and cost after FieldNode's design for construction, v0.2 for wind and heat, which that change left unchanged) for the hot-climate node with its sun shield, and the calibration reference uncertainty from CLR-CAL-001 v0.1; no sibling repo was edited. Run the script from the repo root with `python docs/04-calcs/sizing.py`.

The design case is a node on a 114.3 mm (4.5 in) street pole with the arm axis 2.8 m above the pavement, air temperature up to 50 °C, full sun and 15 min reporting.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Globe | 150 mm copper sphere, 0.4 mm wall, emissivity 0.95; convection coefficient the larger of 6.3 *v*^0.6 / *D*^0.4 (forced) and 1.4 (Δ*T* / *D*)^0.25 (natural) W/m²K | ISO 7726:1998 method as implemented in the open [pythermalcomfort `t_mrt` function](https://pythermalcomfort.readthedocs.io/en/latest/reference/pythermalcomfort.html) (defaults 0.15 m and 0.95). The coefficients 6.3 and 1.4 are the commonly quoted values and were not read from the standard itself; 6.3/σ equals the 1.1 × 10⁸ of the TRL 2 precis [A1] |
| Wet bulb | Notional wick 7 mm diameter; cylinder in cross flow Nu = 0.683 Re^0.466 Pr^(1/3); Chilton-Colburn heat and mass analogy, Lewis number 0.85; the wick sees the radiant environment measured by the globe | Textbook correlations. A simplified stand-in for the Liljegren et al. (2008) model, which the data server will use through its open implementation |
| Sensors | SHT45 typical ±0.1 °C and ±1.0 %RH ([Sensirion](https://sensirion.com/products/catalog/SHT45)); globe probe ±0.3 °C (R3); anemometer ±0.5 m/s (R4) and start-up 0.8 m/s | Sensirion product page (checked 2026-09-25); anemometer start-up is a typical low-cost value, unverified |
| Shield | White ASA plates, solar absorptance 0.25; half of the absorbed heat reaches the air passing the sensor; with the fan off, air inside the stack moves at a quarter of the wind speed; 1,000 W/m² global irradiance, sun 60° high, pavement albedo 0.15 | Assumed; only a side-by-side test can set these |
| Fan | 60 x 60 x 15 mm 5 V class fan, 0.90 W, 6.6 L/s (about 14 CFM) free air, 60 % of it delivered through the stack; FieldNode 5 V rail 85 % efficient; T and RH sensor time constant 2 s with its membrane cap | Typical values for the fan class and assumed shares; not checked against a chosen part |
| Height | Surface-layer similarity (Businger-Dyer functions) with a 250 W/m² sensible heat flux from sunlit pavement and a 0.1 m roughness length | Assumed; similarity theory is only approximate inside a street canyon |
| Wind | 35 m/s gust (750 Pa); drag coefficients 0.5 on the globe, 1.2 on the shield, mast and hub, 1.4 on open cups, 2.0 on the square arm | Screening values, not a code check |
| Clamp | 1,000 N preload per strap band, friction coefficient 0.4 | As FND-CAL-001, to keep the two notes consistent |
| Materials | Aluminium 6063, E 69 GPa, yield 145 MPa; aluminium 2.7, ASA 1.07, stainless 7.9, copper 8.96 g/cm³ | Handbook values |
| FieldNode | Hot-climate node with the sun shield, Rev P3: 2.61 kg, $148.00 ($139.00 base plus the $9.00 shield), 88 N at 35 m/s (panel 52.2 N, shielded enclosure 36.3 N), interior 7.2 K above ambient when dusty with the sun in its worst position (28.3 K without the shield); 100 mW design sensor allowance, 32 B per stored reading, 23.7 s/day airtime at SF9 | FND-CAL-001 v0.4 and v0.2 |

## A. Mean radiant temperature from the globe (R3, R4, R5)

- **Worked example.** At 35 °C air, 50 °C globe and 1 m/s, the forced convection coefficient is 13.5 W/m²K against 4.4 W/m²K for natural convection, and MRT is 74.8 °C [A1]. The TRL 2 figure of about 75 °C stands.
- **Wind is the weakest input.** With 0.5, 1.5 and 3.0 m/s instead of 1 m/s, MRT is 66.9, 80.7 and 93.9 °C [A2]. A 0.5 m/s wind error moves MRT by about 6 to 8 °C; a 1 °C air temperature error moves it by 1.5 °C and a 0.3 °C globe error by 0.7 °C [A3].
- **Calm air.** Natural convection governs only below 0.16 m/s [A4]. Below the anemometer's start-up speed the node reads zero wind: at a true 0.5 m/s, MRT is then computed as 58.8 °C instead of 66.9 °C, 8.2 °C low [A5]. R4 now covers 0.8 to 20 m/s (HMN-DDR-002), and intervals with a large share of calm air are flagged by the server (section G) rather than corrected.

## B. Natural wet bulb and WBGT (R5)

- **Check of the wick model.** With no radiant excess the model gives a wet bulb of 24.2 °C at 35 °C and 40 %RH [B1], the psychrometric value the TRL 2 precis assumed (about 24.5 °C).
- **Worked example.** In sun the natural wet bulb is 26.0 °C, and WBGT = 0.7 × 26.0 + 0.2 × 50 + 0.1 × 35 = 31.7 °C [B2]. The TRL 2 estimate (about 31 °C, with an assumed 1 °C sun excess on the wet bulb) is slightly low; the model gives a 1.8 °C excess.
- **Sensitivity.** Per unit input, WBGT moves 0.53 °C per °C of air temperature, 0.15 °C per %RH, 0.28 °C per °C of globe temperature and -0.18 °C per m/s of wind [B3]. Air temperature matters most, because it enters WBGT directly, through the wet bulb and through MRT.
- **Error budget.** With the fan-aspirated shield (section C) the input terms are 0.23 °C (air temperature), 0.15 °C (humidity), 0.09 °C (globe) and 0.09 °C (wind): ±0.30 °C root sum square and ±0.55 °C worst case [B4]. With the passive shield at 1 m/s (v0.1) they were ±0.59 °C and ±0.88 °C [B5].
- **Calm air.** A true 0.5 m/s read as zero raises the computed WBGT by 0.9 °C [B6].
- **R5 is at risk.** The input budget fits the ±1.0 °C target with a wide margin, and flagged calm intervals (section G) are marked rather than trusted, but the error of the Liljegren model itself against a reference WBGT meter is not included and can only be found by collocation.

## C. Radiation error of the shield, passive and fan-aspirated (R1)

- **Heat input.** In full sun the top, sides and underside of the stack present 82, 59 and 70 cm² and absorb 3.74 W; with the fan off, air crosses the stack through about 60 cm² [C1].
- **Passive error (fan off).** The air at the sensor would read 2.09 °C high at 0.5 m/s, 1.04 °C at 1 m/s, 0.52 °C at 2 m/s and 0.35 °C at 3 m/s [C2]; with half the assumed ventilation, 2.09 °C at 1 m/s [C3]. This was the v0.1 design and is why R1 was not met.
- **Fan (HMN-DDR-002).** A 60 mm, 0.90 W fan in a cowl on the top plate draws about 4.0 L/s up the 56 mm center column of the stack, about 1.6 m/s. The steady error is 0.40 °C whatever the wind; after 6 s of running from the passive 1 m/s state the sensor reads 0.43 °C high [C4]. The fan needs at least 3.4 L/s through the stack, about half its assumed free-air flow, to hold ±0.5 °C [C6], so the margin rests on the chosen fan and on how much flow the plate stack lets through.
- **Firmware rule.** The FieldNode switches the 5 V port on for 6 s every 3 min and reads the temperature and humidity sensor at the end of the run: 480 aspirated readings a day, 5 per 15 min mean. That costs 35.3 mW on average from the cell [C5].
- **R1 is met on paper** (±0.5 °C at any wind speed), subject to the assumed fan flow and heat-transfer factors, which only a side-by-side test against an aspirated reference can confirm.

## D. Globe response and probe accuracy (R3)

- **Globe.** The 0.4 mm copper shell weighs 253 g; with a 20 g boss its heat capacity is 105 J/K [D1]. The shell alone has a time constant of 1.8 min at 0.3 m/s, 1.2 min at 1 m/s and 0.7 min at 3 m/s [D2].
- **Bead inside.** The epoxy bead couples to the shell by radiation and still air inside the sphere, with a time constant of 4.2 min. Globe and bead together respond with a time constant of about 5.4 min at 1 m/s, a 90 % response in about 12 min [D5], inside the 30 min of R3. This is faster than the 20 to 30 min estimated at TRL 2. Conduction along the probe stem is not included and only a step test can confirm the figure.
- **Probe.** At 50 °C the NTC reads 3.59 kΩ; in a 10 kΩ divider the slope is 24.3 mV/K, a 12-bit step is 33 mK, and self-heating is 0.21 mW for the 10 ms the divider is on [D3], which is negligible.
- **Calibration.** Calibrated in CalRig before it is fitted to the globe, the probe's expanded uncertainty is ±0.18 °C with CalRig's typical reference, or ±0.26 °C if the reference sensor is only as good as a maximum tolerance would allow [D4]. **R3 is met on paper.**

## E. Measurement height and pole shading (R9)

- **Height correction.** On a sunny afternoon the air near the pavement is warmer than at the sensor. At 1 m/s the estimate gives +0.72 °C at 1.1 m, +0.44 °C at 1.5 m and +0.21 °C at 2.0 m relative to the 2.69 m of the shield; at 3 m/s, +0.80, +0.50 and +0.24 °C [E1]. A node at 2.7 m therefore reads pedestrian-height air temperature low by up to about 0.8 °C in strong sun, which would enter WBGT at about 0.4 °C (section B). At night and in shade the difference is smaller or reversed. The radiant field changes less with height, because the pavement fills about half of the globe's view at any height above an open street; walls change this in narrow streets.
- **R9 is not met.** The target is unchanged under HMN-DDR-001 D2, decided by Amish on 2026-09-25; the correction above, with a pilot comparing 2.0 and 2.8 m (TRL 4, on hold), is the decided path. The fan cowl lowers the shield by 25 mm, so the sensors now sit at 2.67 to 2.69 m.
- **Pole shading of the globe.** From the globe, the 114 mm pole spans 13.0°. With the arm pointing east or west the sun would pass behind it for about 0.9 h a day. The arm now points toward the equator (HMN-DDR-002), so the pole is on the poleward side of the globe, which the sun reaches only in the tropics, near noon and high in the sky [E2].
- **Shading of the FieldNode panel.** With the core below the arm (v0.5 and earlier), the shield, cowl, globe and arm shaded 44 % of the panel at 30° elevation, 34 % at 45°, 27 % at 60° and 16 % at 75° with the sun straight along the arm, and less off axis. Amish decided on 2026-10-02 to mount the core above the arm, provided its lid stays reachable from the ladder or lift that fits the arm; the model now has the core's bottom at 3.11 m, its whip 100 mm or more above the arm. The sensor head is then wholly below the panel, and the shield, cowl, globe and arm shade 0 % of it at every sun position run (30 to 75° high, 0 to 60° off the arm's azimuth) [E3]. The reverse now needs checking: the panel and enclosure can shade the sensors, but only when the sun is on the pole side of the node. That happens only in the tropics near noon; there, a sun 45 to 75° high on the pole side shades the globe or the shield stack, and one 30° high shades the cups [E3b]. On the equator side, where the sun is outside the tropics, nothing is shaded. Shade on a series-connected panel could still cut its output by more than the shaded share, but the head no longer shades it.

## F. Sensor power (R7)

The temperature and humidity sensor takes about 11 µJ per reading, now 480 times a day, and the NTC divider 8 µJ, 1,440 times a day; with the anemometer's reed resting closed in the worst case (0.109 mW), the sensors alone draw 0.116 mW [F1], [F2]. The fan adds 35.3 mW (section C), for a total of 35.4 mW, 35 % of FieldNode's 100 mW design allowance (FND-CAL-001) [F2]. **R7 is met on paper**, with the margin now set by the fan. The panel shading in section E reduces harvest and is not included in FieldNode's energy budget.

## G. Payload, airtime and storage (R6)

- **Payload.** Eleven fields fit in 20 B: means of air temperature, humidity, globe temperature and wind, maxima of air and globe temperature, the gust, the share of the interval below the anemometer's start-up, battery voltage, status and a sequence number [G1]. The calm-share byte lets the server flag intervals where the MRT and WBGT are biased (sections A and B).
- **Airtime and storage.** At 96 uplinks a day the node uses 23.7 s/day of airtime at SF9 (FND-CAL-001). Seven days of records at FieldNode's 32 B each take 21.5 kB [G2]; the TRL 2 figure of 13 kB assumed 20 B records.
- **Calm flag.** The server marks MRT and WBGT as biased high in calm air for any interval whose calm share (time below the 0.8 m/s start-up) is 20 % or more, that is 3 min of 15 [G4]. This is the rule under the restated R4 (HMN-DDR-002); the threshold is a starting value for the pilot.
- **Latency.** Each 15 min mean is sent as its interval closes and reaches the gateway within about 16 min. The 1.02 % of uplinks lost at TwinKit's worst case arrive with the next uplink at about 31 min [G3]. **R6 is met on paper** for 99 % of intervals.

## H. Wind load, arm and clamp (R11)

- **Loads.** A 35 m/s gust across the arm puts 6.6 N on the globe, 10.7 N on the shield, 2.1 N on the fan cowl, 7.2 N on the anemometer and 19.9 N on the 530 mm arm: 46.5 N on the sensor head [H1]. The TRL 2 estimate of 110 N included the FieldNode panel and enclosure (88 N with the sun shield in FND-CAL-001 v0.2).
- **Arm.** The 25 x 25 x 2 mm tube (second moment of area 16,345 mm⁴) sees 14.6 N·m at its root and 11.1 MPa, a factor of 13.0 on yield [H2]. Its tip deflects 0.31 mm at 20 m/s and 0.95 mm at 35 m/s [H3], far inside the 10 mm of R11. Torsion from the offset loads is 0.84 N·m [H4].
- **Clamp.** Wind twists the arm about the pole with 18.1 N·m against 45.7 N·m of band friction, a factor of 2.5. The 1.37 kg on the arm, with its center of mass 425 mm out, pulls the upper band with 41 N against 2,000 N, and pushes down with 13 N against 800 N of friction [H5]. The formed 3 mm sheet saddle (now a channel whose V-notched flanges bear on the pole, HMN-DDR-003) carries these loads through the band preload; its bending stiffness has not been checked and should be at detail design. **R11 is met on paper**, subject to the preload, which a torque figure at installation must secure; the twist factor of 2.5 is the smallest margin in this section.
- **Pole.** The node adds 46 N (head) plus 88 N (FieldNode with its shield) and about 423 N·m at the pole base [H6] (338 N·m before the core moved above the arm, 2.15 m to 3.11 m up). The pole owner should check this against the pole's rating.

## I. Outdoor temperatures (R8)

- **Sensor head.** At 50 °C air and an 80 °C radiant field in near calm, the globe reaches 67.4 °C [I1]. The SHT45 and a 125 °C class epoxy NTC (assumed rating) are well within their limits; the ASA plates and aluminium arm are too.
- **FieldNode core.** HeatMap nodes now carry FieldNode's hot-climate sun shield (HMN-DDR-002). With it the core's interior runs up to 7.2 K above ambient when dusty with the sun in its worst position, 57.2 °C at 50 °C air, against a 70 °C electronics rating; without it the figure would be 78.3 °C [I2]. R8 is restated to +50 °C at the node, matching HMN-PRB-001. **R8 is met on paper**, resting on FieldNode's assumed shield factor.

## J. Fit to poles and installation (R10)

- **Fit.** A 120° V touches a round pole at ±r cos 60° from its center line: ±15 mm on a 60 mm pole, ±29 mm on a 114 mm pole and ±50 mm on a 200 mm pole, all inside the saddle's V notches (±55 mm at the flange edge) and the adapter V-blocks (±55 mm); strap bands 338 to 778 mm long cover the range [J1]. The FieldNode adapter uses the same 120° V, because FieldNode's own V-blocks only seat small poles (FND-DDR-003). The fit part of R10 is met by design, with no drilling.
- **Time.** The tasks add up to 37 min for two people working in turn from one lift, with the arm and its sensors assembled on the ground [J2], against 30 min. **R10 is at risk**; only a timed trial can settle it.

## K. Mass (R15)

- **Sensor head.** From the component volumes of the constructable model: arm with plug and sleeves 268 g, clamp (saddle, trim, cheeks, bands and bolts) 442 g, shield with rods and spacers 324 g, fan and cowl 78 g, sensor 20 g, globe with its brass hanger tube 348 g, probe 10 g, anemometer 307 g, harness 238 g (two leads cut for the core above the arm, 1.2 m and 1.4 m), lanyards 20 g and consumables 30 g: 2.08 kg [K1]. The design for construction added 0.21 kg (HMN-DDR-003).
- **Against R15.** R15 now covers the sensor head only (HMN-DDR-002), so 2.08 kg against 4.0 kg: **R15 is met on paper**. For information, with the FieldNode core and its sun shield (2.61 kg) and the pole adapter (0.22 kg) the complete node weighs 4.92 kg [K2]. The largest part other than the arm is the 290 mm FieldNode panel, within the 300 mm limit [K3].

## L. Cost (R13)

The BOM has 13 lines. Under HMN-DDR-002 the pole adapter (line 12) counts against the FieldNode core, as it fixes a FieldNode fit limit. The design for construction (HMN-DDR-003) repriced lines 2, 4, 8, 10 and 12, and line 1 follows FieldNode's own design for construction to $148.00. The sensor head (lines 2 to 11 and 13) is estimated at $136.00; the FieldNode core with its sun shield and the adapter (lines 1 and 12) at $156.00, and the full node at $292.00 [L1]. `budget_usd` is a hypothetical value-engineering target, not a spending limit (Amish, 2026-10-01). Value-engineering target: USD 130. Estimated cost of the constructable design: USD 136 (USD 6 over the target) [L2]. **R13 is over its value-engineering target by $6.00**; the cost drivers and savings worth trying are in the design decisions register (HMN-DEC-001).

## M. Results against every requirement

*Table 2. Requirement status from this note.*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R9 | Measurement height | Sensors at 2.67 to 2.69 m; pedestrian air 0.2 to 0.8 °C warmer [E1] | 1.1 to 2.0 m | **Not met** |
| R5 | Derived heat stress | Input budget ±0.30 °C RSS, ±0.55 °C worst [B4]; calm intervals flagged [G4]; model error unknown | WBGT within ±1.0 °C of a reference meter | **At risk** |
| R10 | Fit to existing poles | Fits 60 to 200 mm [J1]; 37 min [J2] | Band clamps, no drilling, 30 min | **At risk** |
| R14 | Traceable data | Probe calibrated before fitting fits a CalRig bay; the assembled globe does not (150 mm against a 90 x 70 x 50 mm bay); payload format defined [G1] | CalRig record per node; open documented format | **At risk** |
| R1 | Air temperature accuracy | 0.43 °C with the fan at any wind speed [C4]; 1.04 °C at 1 m/s with the fan off [C2] | ±0.5 °C | Met on paper (fan flow assumed) |
| R3 | Globe temperature | ±0.18 °C (±0.26 °C) [D4]; 90 % response about 12 min [D5] | ±0.3 °C; 30 min | Met on paper |
| R4 | Wind speed | Start-up about 0.8 m/s (typical, unverified); calm share sent and flagged [G1], [G4] | 0.8 to 20 m/s; calm intervals flagged | Met on paper (start-up unverified) |
| R6 | Reporting | 20 B, 23.7 s/day at SF9, 21.5 kB for 7 days, 16 min latency for 99 % [G1] to [G3] | 15 min means; 30 min; 7 days | Met on paper |
| R7 | Power autonomy | 35.4 mW with the fan, 35 % of the allowance [F2] | 5 days without sun on FieldNode | Met on paper (the head no longer shades the panel [E3]) |
| R8 | Outdoor survival | FieldNode interior 57.2 °C at 50 °C air with its sun shield [I2]; sensor head parts within ratings | Operate at -20 to +50 °C at the node | Met on paper (shield factor assumed) |
| R11 | Wind survival | Factor 13.0 on the arm; clamp twist factor 2.5; 0.31 mm at 20 m/s [H2] to [H5] | No failure at 35 m/s; under 10 mm at 20 m/s | Met on paper (preload assumed) |
| R13 | Cost | Sensor head $136.00 estimated [L1], [L2] | Value-engineering target $130 (sensor head, excluding the FieldNode core and its pole adapter) | Over the target by $6.00 |
| R15 | Mass and loading | Sensor head 2.08 kg [K2]; largest part 290 mm [K3] | 4 kg or less (sensor head); 300 mm | Met on paper |
| R2 | Relative humidity | SHT45 ±1.0 %RH typical | ±3 %RH | Met by design |
| R12 | Privacy | No camera, microphone or radio scanning parts; payload has environmental fields only [G1] | Environmental data only | Met by design |

Counts: 1 not met, 3 at risk, 8 met on paper, 2 met by design, and R13 $6.00 over its value-engineering target (v0.3: 9 met on paper with R13 $3.00 under the target; v0.2: 2 not met and 8 met on paper, before the budget top-up). In v0.1 the counts were 6 not met, 3 at risk, 4 met on paper and 2 met by design. None is left wholly unverifiable at TRL 3, although R1, R5, R8 and R10 each rest on assumptions that only a test can settle.

## Checks against the TRL 2 figures

*Table 3. TRL 2 claims (HMN-PRC-001 v0.2) against this note.*

| TRL 2 claim | This note | Action |
| --- | --- | --- |
| MRT about 75 °C in the worked example | 74.8 °C | Stands |
| WBGT about 31 °C | 31.7 °C (natural wet bulb 26.0 °C, not 25.5 °C) | Precis updated |
| MRT about 67 / 80 °C at 0.5 / 1.5 m/s | 66.9 / 80.7 °C | Stands |
| Globe response 20 to 30 min | About 12 min to 90 % | Precis and REQ updated |
| Sensor load under 1 mW; allowance about 115 mW | 0.116 mW; 100 mW design allowance (115 mW published) | Precis updated |
| 7 days of data about 13 kB | 21.5 kB at FieldNode's 32 B records | Precis updated |
| Wind load about 110 N; about 17 N·m at the arm root | Head 46.1 N plus FieldNode 88 N (v0.2); 14.1 N·m at the root | Precis updated |
| Mass about 3.3 kg | 4.70 kg complete node, 1.91 kg sensor head (v0.2) | Precis updated; R15 restated to the sensor head and met |
| Sensor head about $120; full node about $246 | $127.00; $268.00 (v0.2) | Precis, BOM notes updated |
| Arm at about 2.8 m | Arm axis 2.80 m; sensors at 2.67 to 2.69 m (v0.2) | Stands |
