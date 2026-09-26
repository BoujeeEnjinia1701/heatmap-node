---
doc_id: HMN-CAL-001
title: HeatMap Node sizing calculations
project: HeatMap Node
doc_type: Calculation
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (mean radiant temperature, natural wet bulb and WBGT error budget, shield error, globe response and probe, height and shading, power, data, wind and clamp, outdoor temperatures, fit and installation, mass, cost)
---

# HeatMap Node sizing calculations

On paper, HeatMap Node measures what it sets out to measure, but it misses six of its fifteen requirements. The heat stress method works: in the worked example (35 °C air, 40 %RH, 50 °C globe, 1 m/s wind) mean radiant temperature is 74.8 °C and WBGT is 31.7 °C, and the input errors add up to ±0.59 °C of WBGT (root sum square) against the ±1.0 °C of R5. The misses are: R1, because a naturally ventilated shield reads about 1.0 °C high in full sun at 1 m/s (target ±0.5 °C); R4, because a low-cost cup anemometer does not start below about 0.8 m/s; R8, because the FieldNode core's interior exceeds its electronics rating at the top of the ambient range (inherited from FND-CAL-001); R9, because the sensors sit at about 2.7 m, where the air is 0.2 to 0.8 °C cooler than at pedestrian height on a sunny afternoon; R13, because the sensor head costs $130 against the $120 budget; and R15, because the complete node weighs 4.68 kg against 4.0 kg, mainly because the FieldNode core weighs 2.41 kg, not the 1.7 kg assumed at TRL 2. The TRL 3 work added two parts: stainless lanyards as secondary retention for the globe and shield, and a wider V-block adapter so that the FieldNode core seats on street poles. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [A1], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that a place is safe or unsafe for people, and HeatMap Node data must not be used to decide whether a particular person may work or exercise. Pole mounting, the pole's added wind load and the FieldNode cell are safety matters; see HMN-PRC-001, Safety.

## Scope and method

The note checks every requirement in HMN-REQ-001 v0.3 against the design in HMN-PRC-001 v0.3 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, derived dimensions and part solids, so the heights, lengths, areas and volumes used here are those in the STEP files and in drawing HMN-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. FieldNode figures (mass, cost, wind load, interior temperature, airtime, sensor allowance) are quoted from FND-CAL-001 v0.1, and the calibration reference uncertainty from CLR-CAL-001 v0.1; no sibling repo was edited. Run the script from the repo root with `python docs/04-calcs/sizing.py`.

The design case is a node on a 114.3 mm (4.5 in) street pole with the arm axis 2.8 m above the pavement, air temperature up to 50 °C, full sun and 15 min reporting.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Globe | 150 mm copper sphere, 0.4 mm wall, emissivity 0.95; convection coefficient the larger of 6.3 *v*^0.6 / *D*^0.4 (forced) and 1.4 (Δ*T* / *D*)^0.25 (natural) W/m²K | ISO 7726:1998 method as implemented in the open [pythermalcomfort `t_mrt` function](https://pythermalcomfort.readthedocs.io/en/latest/reference/pythermalcomfort.html) (defaults 0.15 m and 0.95). The coefficients 6.3 and 1.4 are the commonly quoted values and were not read from the standard itself; 6.3/σ equals the 1.1 × 10⁸ of the TRL 2 precis [A1] |
| Wet bulb | Notional wick 7 mm diameter; cylinder in cross flow Nu = 0.683 Re^0.466 Pr^(1/3); Chilton-Colburn heat and mass analogy, Lewis number 0.85; the wick sees the radiant environment measured by the globe | Textbook correlations. A simplified stand-in for the Liljegren et al. (2008) model, which the data server will use through its open implementation |
| Sensors | SHT45 typical ±0.1 °C and ±1.0 %RH ([Sensirion](https://sensirion.com/products/catalog/SHT45)); globe probe ±0.3 °C (R3); anemometer ±0.5 m/s (R4) and start-up 0.8 m/s | Sensirion product page (checked 2026-09-25); anemometer start-up is a typical low-cost value, unverified |
| Shield | White ASA plates, solar absorptance 0.25; half of the absorbed heat reaches the air passing the sensor; air inside the stack moves at a quarter of the wind speed; 1,000 W/m² global irradiance, sun 60° high, pavement albedo 0.15 | Assumed; only a side-by-side test can set these |
| Height | Surface-layer similarity (Businger-Dyer functions) with a 250 W/m² sensible heat flux from sunlit pavement and a 0.1 m roughness length | Assumed; similarity theory is only approximate inside a street canyon |
| Wind | 35 m/s gust (750 Pa); drag coefficients 0.5 on the globe, 1.2 on the shield, mast and hub, 1.4 on open cups, 2.0 on the square arm | Screening values, not a code check |
| Clamp | 1,000 N preload per strap band, friction coefficient 0.4 | As FND-CAL-001, to keep the two notes consistent |
| Materials | Aluminium 6063, E 69 GPa, yield 145 MPa; aluminium 2.7, ASA 1.07, stainless 7.9, copper 8.96 g/cm³ | Handbook values |
| FieldNode | 2.41 kg, $126.00, 81 N at 35 m/s, 100 mW design sensor allowance, 32 B per stored reading, 23.7 s/day airtime at SF9; interior 28.3 K above ambient when dusty with the sun in its worst position | FND-CAL-001 v0.1 |

## A. Mean radiant temperature from the globe (R3, R4, R5)

- **Worked example.** At 35 °C air, 50 °C globe and 1 m/s, the forced convection coefficient is 13.5 W/m²K against 4.4 W/m²K for natural convection, and MRT is 74.8 °C [A1]. The TRL 2 figure of about 75 °C stands.
- **Wind is the weakest input.** With 0.5, 1.5 and 3.0 m/s instead of 1 m/s, MRT is 66.9, 80.7 and 93.9 °C [A2]. A 0.5 m/s wind error moves MRT by about 6 to 8 °C; a 1 °C air temperature error moves it by 1.5 °C and a 0.3 °C globe error by 0.7 °C [A3].
- **Calm air.** Natural convection governs only below 0.16 m/s [A4]. Below the anemometer's start-up speed the node reads zero wind: at a true 0.5 m/s, MRT is then computed as 58.8 °C instead of 66.9 °C, 8.2 °C low [A5]. This is the practical consequence of R4 not being met.

## B. Natural wet bulb and WBGT (R5)

- **Check of the wick model.** With no radiant excess the model gives a wet bulb of 24.2 °C at 35 °C and 40 %RH [B1], the psychrometric value the TRL 2 precis assumed (about 24.5 °C).
- **Worked example.** In sun the natural wet bulb is 26.0 °C, and WBGT = 0.7 × 26.0 + 0.2 × 50 + 0.1 × 35 = 31.7 °C [B2]. The TRL 2 estimate (about 31 °C, with an assumed 1 °C sun excess on the wet bulb) is slightly low; the model gives a 1.8 °C excess.
- **Sensitivity.** Per unit input, WBGT moves 0.53 °C per °C of air temperature, 0.15 °C per %RH, 0.28 °C per °C of globe temperature and -0.18 °C per m/s of wind [B3]. Air temperature matters most, because it enters WBGT directly, through the wet bulb and through MRT.
- **Error budget.** With the shield error at 1 m/s (section C) the input terms are 0.55 °C (air temperature), 0.15 °C (humidity), 0.09 °C (globe) and 0.09 °C (wind): ±0.59 °C root sum square and ±0.88 °C worst case [B4]. With a fan-aspirated shield the budget falls to ±0.20 °C [B5].
- **Calm air.** A true 0.5 m/s read as zero raises the computed WBGT by 0.9 °C [B6].
- **R5 is at risk.** The input budget fits the ±1.0 °C target, but the shield error grows fast below 1 m/s, the start-up error adds up to 0.9 °C in calm air, and the error of the Liljegren model itself against a reference WBGT meter is not included and can only be found by collocation.

## C. Radiation error of the naturally ventilated shield (R1)

- **Heat input.** In full sun the top, sides and underside of the stack present 82, 59 and 70 cm² and absorb 3.74 W; air crosses the stack through about 60 cm² [C1].
- **Error.** The air at the sensor reads 2.09 °C high at 0.5 m/s, 1.04 °C at 1 m/s, 0.52 °C at 2 m/s and 0.35 °C at 3 m/s [C2]. The error reaches 0.5 °C only at 2.1 m/s; if the stack ventilates half as well as assumed, the error at 1 m/s is 2.09 °C [C3].
- **R1 is not met** on these assumptions: ±0.5 °C is missed at 1 m/s and ±1.0 °C is missed at 0.5 m/s. The size of the error rests on three assumed factors (absorptance, share of heat reaching the sensor, ventilation), so the figure is uncertain by a factor of about two in either direction.
- **Fan option.** A small fan moving 3 m/s through the stack cuts the error to 0.09 °C. At 0.30 W and 10 % duty (run before each reading) it draws 30 mW [C4], within the FieldNode allowance but 250 times the present sensor load. It is proposed in `docs/REVIEW.md`, not adopted.

## D. Globe response and probe accuracy (R3)

- **Globe.** The 0.4 mm copper shell weighs 253 g; with a 20 g boss its heat capacity is 105 J/K [D1]. The shell alone has a time constant of 1.8 min at 0.3 m/s, 1.2 min at 1 m/s and 0.7 min at 3 m/s [D2].
- **Bead inside.** The epoxy bead couples to the shell by radiation and still air inside the sphere, with a time constant of 4.2 min. Globe and bead together respond with a time constant of about 5.4 min at 1 m/s, a 90 % response in about 12 min [D5], inside the 30 min of R3. This is faster than the 20 to 30 min estimated at TRL 2. Conduction along the probe stem is not included and only a step test can confirm the figure.
- **Probe.** At 50 °C the NTC reads 3.59 kΩ; in a 10 kΩ divider the slope is 24.3 mV/K, a 12-bit step is 33 mK, and self-heating is 0.21 mW for the 10 ms the divider is on [D3], which is negligible.
- **Calibration.** Calibrated in CalRig before it is fitted to the globe, the probe's expanded uncertainty is ±0.18 °C with CalRig's typical reference, or ±0.26 °C if the reference sensor is only as good as a maximum tolerance would allow [D4]. **R3 is met on paper.**

## E. Measurement height and pole shading (R9)

- **Height correction.** On a sunny afternoon the air near the pavement is warmer than at the sensor. At 1 m/s the estimate gives +0.73 °C at 1.1 m, +0.44 °C at 1.5 m and +0.21 °C at 2.0 m relative to the 2.71 m of the shield; at 3 m/s, +0.81, +0.51 and +0.25 °C [E1]. A node at 2.7 m therefore reads pedestrian-height air temperature low by up to about 0.8 °C in strong sun, which would enter WBGT at about 0.4 °C (section B). At night and in shade the difference is smaller or reversed. The radiant field changes less with height, because the pavement fills about half of the globe's view at any height above an open street; walls change this in narrow streets.
- **R9 is not met.** The target is unchanged under HMN-DDR-001 D2; the correction above, with a pilot comparing 2.0 and 2.8 m (TRL 4 or later, on hold), is the adopted path.
- **Pole shading.** From the globe, the 114 mm pole spans 13.0°. With the arm pointing east or west, the sun passes behind the pole for about 0.9 h a day [E2], and the globe reads low while it does. Pointing the arm toward the equator avoids this near midday; this is proposed in `docs/REVIEW.md`, not adopted.

## F. Sensor power (R7)

The temperature and humidity sensor takes about 11 µJ per reading and the NTC divider 8 µJ; at 1,440 readings a day and with the anemometer's reed resting closed in the worst case (0.109 mW), the average sensor load is 0.116 mW [F1], [F2]. That is 0.12 % of FieldNode's 100 mW design allowance (FND-CAL-001), and of the 115 mW published figure. The fan option would raise the load to about 30 mW [F2]. **R7 is met on paper**, with a wide margin.

## G. Payload, airtime and storage (R6)

- **Payload.** Eleven fields fit in 20 B: means of air temperature, humidity, globe temperature and wind, maxima of air and globe temperature, the gust, the share of the interval below the anemometer's start-up, battery voltage, status and a sequence number [G1]. The calm-share byte lets the server flag intervals where the MRT and WBGT are biased (sections A and B).
- **Airtime and storage.** At 96 uplinks a day the node uses 23.7 s/day of airtime at SF9 (FND-CAL-001). Seven days of records at FieldNode's 32 B each take 21.5 kB [G2]; the TRL 2 figure of 13 kB assumed 20 B records.
- **Latency.** Each 15 min mean is sent as its interval closes and reaches the gateway within about 16 min. The 1.02 % of uplinks lost at TwinKit's worst case arrive with the next uplink at about 31 min [G3]. **R6 is met on paper** for 99 % of intervals.

## H. Wind load, arm and clamp (R11)

- **Loads.** A 35 m/s gust across the arm puts 6.6 N on the globe, 10.7 N on the shield, 7.2 N on the anemometer and 19.5 N on the arm: 44.1 N on the sensor head [H1]. The TRL 2 estimate of 110 N included the FieldNode panel and enclosure (81 N in FND-CAL-001).
- **Arm.** The 25 x 25 x 2 mm tube (second moment of area 16,345 mm⁴) sees 13.7 N·m at its root and 10.5 MPa, a factor of 13.8 on yield [H2]. Its tip deflects 0.29 mm at 20 m/s and 0.88 mm at 35 m/s [H3], far inside the 10 mm of R11. Torsion from the offset loads is 0.48 N·m [H4].
- **Clamp.** Wind twists the arm about the pole with 17.5 N·m against 45.7 N·m of band friction, a factor of 2.6. The 1.15 kg on the arm, with its center of mass 441 mm out, pulls the upper band with 35 N against 2,000 N, and pushes down with 11 N against 800 N of friction [H5]. **R11 is met on paper**, subject to the preload, which a torque figure at installation must secure; the twist factor of 2.6 is the smallest margin in this section.
- **Pole.** The node adds 44 N (head) plus 81 N (FieldNode) and about 314 N·m at the pole base [H6]. The pole owner should check this against the pole's rating.

## I. Outdoor temperatures (R8)

- **Sensor head.** At 50 °C air and an 80 °C radiant field in near calm, the globe reaches 67.4 °C [I1]. The SHT45 and a 125 °C class epoxy NTC (assumed rating) are well within their limits; the ASA plates and aluminium arm are too.
- **FieldNode core.** The core's interior runs up to 28.3 K above ambient when dusty with the sun in its worst position: 78.3 °C at 50 °C air and 88.3 °C at 60 °C air, against a 70 °C electronics rating [I2]. **R8 is not met** for the FieldNode core at the top of the R8 range. FieldNode's proposed sun shield (48.5 °C inside at 45 °C ambient in FND-CAL-001) would address this. R8 also asks for +60 °C at the node while HMN-PRB-001 states +50 °C; aligning the two is proposed in `docs/REVIEW.md`.

## J. Fit to poles and installation (R10)

- **Fit.** A 120° V-saddle touches a round pole at ±r cos 60° from its center line: ±15 mm on a 60 mm pole, ±29 mm on a 114 mm pole and ±50 mm on a 200 mm pole, all inside the saddle's ±55 mm; strap bands 338 to 778 mm long cover the range [J1]. The same V-block geometry is used in the FieldNode adapter, because FieldNode's own 50 mm V-blocks only seat on poles up to about 71 mm (FND REVIEW). The fit part of R10 is met by design, with no drilling.
- **Time.** The tasks add up to 37 min for two people working in turn from one lift, with the arm and its sensors assembled on the ground [J2], against 30 min. **R10 is at risk**; only a timed trial can settle it.

## K. Mass (R15)

- **Sensor head.** Arm 275 g, clamp 569 g, shield 237 g, sensor 20 g, globe 283 g, probe 10 g, anemometer 300 g, harness 270 g, lanyards 20 g and hardware 50 g: 2.03 kg [K1]. The saddle is the heaviest single part; a formed sheet saddle could save about 0.3 kg (estimate).
- **Complete node.** With the FieldNode core (2.41 kg) and the pole adapter (0.24 kg) the node weighs 4.68 kg [K2]. **R15 is not met**; the TRL 2 figure of 3.3 kg used the 1.7 kg FieldNode estimate that FND-CAL-001 has since corrected. The largest part other than the arm is the 290 mm FieldNode panel, within the 300 mm limit [K3]. The FieldNode mass includes its own V-blocks, which the adapter replaces, so the total is slightly high.

## L. Cost (R13)

The BOM has 12 lines. The sensor head (lines 2 to 12) costs $130.00; the FieldNode core (line 1) costs $126.00, and the full node $256.00 [L1]. Against the $120 `budget_usd`, which under HMN-DDR-001 D1 covers the sensor head only, the head is over by $10.00; measured against the same figure the full node would be over by $136.00 [L2]. The $10 is the two parts added at TRL 3: the lanyards ($3) and the FieldNode pole adapter ($7). **R13 is not met.** No new budget figure was recommended in the TRL 2 review, so `budget_usd` is unchanged; options are in `docs/REVIEW.md`.

## M. Results against every requirement

*Table 2. Requirement status from this note.*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R1 | Air temperature accuracy | 1.04 °C at 1 m/s, 2.09 °C at 0.5 m/s in full sun [C2] | ±0.5 °C at 1 m/s or more; ±1.0 °C below | **Not met** (assumption-sensitive) |
| R4 | Wind speed | Start-up about 0.8 m/s; zero read below it [A5] | 0.5 to 20 m/s | **Not met** |
| R8 | Outdoor survival | FieldNode interior 78.3 °C at 50 °C air, 88.3 °C at 60 °C [I2]; sensor head parts within ratings | Operate at -20 to +60 °C at the node | **Not met** (FieldNode core) |
| R9 | Measurement height | Sensors at 2.67 to 2.71 m; pedestrian air 0.2 to 0.8 °C warmer [E1] | 1.1 to 2.0 m | **Not met** |
| R13 | Cost | Sensor head $130.00 [L1] | $120 or less (sensor head, DDR-001 D1) | **Not met** |
| R15 | Mass and loading | 4.68 kg complete node [K2]; largest part 290 mm [K3] | 4 kg or less; 300 mm | **Not met** (mass) |
| R5 | Derived heat stress | Input budget ±0.59 °C RSS, ±0.88 °C worst [B4]; +0.9 °C in calm air [B6]; model error unknown | WBGT within ±1.0 °C of a reference meter | **At risk** |
| R10 | Fit to existing poles | Fits 60 to 200 mm [J1]; 37 min [J2] | Band clamps, no drilling, 30 min | **At risk** |
| R14 | Traceable data | Probe calibrated before fitting fits a CalRig bay; the assembled globe does not (150 mm against a 90 x 70 x 50 mm bay); payload format defined [G1] | CalRig record per node; open documented format | **At risk** |
| R3 | Globe temperature | ±0.18 °C (±0.26 °C) [D4]; 90 % response about 12 min [D5] | ±0.3 °C; 30 min | Met on paper |
| R6 | Reporting | 20 B, 23.7 s/day at SF9, 21.5 kB for 7 days, 16 min latency for 99 % [G1] to [G3] | 15 min means; 30 min; 7 days | Met on paper |
| R7 | Power autonomy | 0.116 mW sensor load, 0.12 % of the allowance [F2] | 5 days without sun on FieldNode | Met on paper |
| R11 | Wind survival | Factor 13.8 on the arm; clamp twist factor 2.6; 0.29 mm at 20 m/s [H2] to [H5] | No failure at 35 m/s; under 10 mm at 20 m/s | Met on paper (preload assumed) |
| R2 | Relative humidity | SHT45 ±1.0 %RH typical | ±3 %RH | Met by design |
| R12 | Privacy | No camera, microphone or radio scanning parts; payload has environmental fields only [G1] | Environmental data only | Met by design |

Counts: 6 not met, 3 at risk, 4 met on paper, 2 met by design. None is left wholly unverifiable at TRL 3, although R1, R5 and R10 each rest on assumptions that only a test can settle.

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
| Wind load about 110 N; about 17 N·m at the arm root | Head 44.1 N plus FieldNode 81 N; 13.7 N·m at the root | Precis updated |
| Mass about 3.3 kg | 4.68 kg (FieldNode 2.41 kg, not 1.7 kg) | Precis updated; R15 now not met |
| Sensor head about $120; full node about $246 | $130.00; $256.00 | Precis, BOM notes updated |
| Arm at about 2.8 m | Arm axis 2.80 m; sensors at 2.67 to 2.71 m | Stands |
