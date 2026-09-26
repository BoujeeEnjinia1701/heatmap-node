---
doc_id: HMN-PRC-001
title: HeatMap Node design precis
project: HeatMap Node
doc_type: Design precis
version: "0.2"
status: Draft
date: '2026-09-25'
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
  change: Populate to TRL 2 (architecture, components, first-order numbers, safety, media, open questions)
---

# HeatMap Node design precis

## Summary

HeatMap Node is a sensor head that clamps to an existing street pole and plugs into the lab's FieldNode core. A horizontal arm holds a naturally ventilated radiation shield with an air temperature and humidity sensor, a standard 150 mm black globe with a thermistor at its center, and a small cup anemometer. From these four readings a server computes mean radiant temperature and an estimated wet bulb globe temperature (WBGT), the heat stress index defined in [ISO 7243:2017](https://www.iso.org/standard/67188.html), using the method of [Liljegren et al. (2008)](https://doi.org/10.1080/15459620802310770). Tens of nodes across a neighborhood give block-by-block heat stress maps, day and night, all season.

First-order estimates: the sensors draw under 1 mW, far inside FieldNode's allowance; the node weighs about 3.3 kg; the sensor head costs about $120 and the full node, with the FieldNode core, about $246 against a $120 budget. Every choice below is proposed, awaiting Amish.

![Hero render](../media/hero.png)

*Figure 1. HeatMap Node on a 114 mm street pole, arm at about 2.8 m, with a 1.75 m person for scale. The pole is not supplied. CONCEPT, NOT FOR FABRICATION.*

## How it works

1. **Air temperature and humidity.** A digital sensor sits inside a stack of eight white plates that block direct and reflected sun while letting wind through. No fan is fitted, to save power and moving parts.
2. **Radiant heat.** A thin copper sphere painted matte black reaches a balance between absorbed sun and long-wave radiation from hot walls and pavement and convective loss to the air. A thermistor at its center reads this globe temperature.
3. **Wind.** A cup anemometer gives the wind speed needed to separate radiant from convective heat at the globe.
4. **Logging and radio.** The FieldNode core samples every 60 s, averages over 15 min, stores the means in flash and sends about 20 bytes by LoRaWAN to a gateway such as TwinKit. Missing packets are resent from flash.
5. **Heat stress and mapping.** A server script computes mean radiant temperature and WBGT and places each node on a block-level map, published as open data. Only environmental values leave the node.

![Data flow](../media/flow.png)

*Figure 2. Data flow from the street to the map. All values are estimates.*

![Cutaway](../media/cutaway.png)

*Figure 3. Section through the sensor arm: temperature and humidity sensor inside the radiation shield, and the thermistor at the center of the globe.*

## Main components

Numbers match the exploded view (Figure 4) and `bom/bom.csv`.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | FieldNode core | IP65 enclosure, 6 W panel as sun hood, 3.2 V 6 Ah LiFePO4 cell, MPPT board, STM32WL-class LoRaWAN module, two M12 ports | Shared lab component; see the FieldNode README. Needs longer pole bands |
| 2 | Radiation shield | Eight 110 mm white plates at 15 mm pitch, printed UV-stable ASA | Naturally ventilated |
| 3 | Temperature and humidity sensor | SHT45-class digital sensor with PTFE membrane cap | I2C over the M12 port |
| 4 | Black globe | 150 mm thin copper sphere, matte black | Standard globe size, so published globe equations apply |
| 5 | Globe probe | 10 k NTC bead at the globe center | Calibrated in CalRig |
| 6 | Cup anemometer | Three-cup, pulse output, on a short mast at the arm tip | Counted by the FieldNode low-power timer |
| 7 | Sensor arm | 25 mm square aluminium tube, about 520 mm | Keeps globe and shield about 250 to 450 mm clear of the pole |
| 8 | Arm clamp | Saddle and two stainless bands for 60 to 200 mm poles | No drilling |
| 9 | Sensor harness | Two M12 5-pin leads along the pole and arm | Plug-in at both ends |

![Exploded view](../media/exploded.png)

*Figure 4. Exploded view with callouts matching the BOM.*

The blueprint sheet is in [media/concept-blueprint.pdf](../media/concept-blueprint.pdf) and an interactive model in [media/viewer.html](../media/viewer.html).

## First-order numbers

All values are estimates for concept screening and will be checked by calculation at TRL 3.

### From measurements to heat stress

For a standard globe under forced convection, mean radiant temperature (MRT) follows from globe temperature *T*g, air temperature *T*a, wind speed *v* (m/s), globe diameter *D* (m) and emissivity *ε*:

MRT = [(*T*g + 273)⁴ + 1.1 × 10⁸ *v*^0.6 / (*ε D*^0.4) × (*T*g - *T*a)]^0.25 - 273

This is the widely used forced-convection globe equation; its source and range of validity will be cited in the TRL 3 calculation note. Outdoor WBGT is 0.7 *T*nwb + 0.2 *T*g + 0.1 *T*a ([ISO 7243:2017](https://www.iso.org/standard/67188.html)), where the natural wet-bulb temperature *T*nwb is estimated from the same four readings with the Liljegren method ([open implementation](https://github.com/mdljts/wbgt)).

**Worked example (assumptions: 35 °C air, 40 %RH, 50 °C globe, 1 m/s wind, *D* = 0.15 m, *ε* = 0.95).** MRT is about 75 °C. The psychrometric wet-bulb temperature is about 24.5 °C; assuming the natural wet bulb in sun reads about 1 °C higher, WBGT is about 0.7 × 25.5 + 0.2 × 50 + 0.1 × 35 ≈ 31 °C. Air temperature alone (35 °C) says nothing about the sun load that the globe captures.

**Sensitivity.** In the same example, a wind reading of 0.5 m/s instead of 1 m/s lowers MRT to about 67 °C, and 1.5 m/s raises it to about 80 °C. A 1 °C air temperature error moves MRT by about 1.5 °C. Wind is therefore the weakest input, which is why an anemometer is fitted rather than taking wind from a distant airport station, and why calm-air accuracy is at risk (R4, R5).

### Power

The temperature and humidity sensor, sampled once a minute, averages a few microamperes. The thermistor divider is switched on only while it is read. The anemometer pulses are counted by a low-power timer; with a 100 kΩ pull-up the worst case (reed contact resting closed) is about 33 µA at 3.3 V, about 0.1 mW. The total sensor load is under 1 mW, compared with about 115 mW that FieldNode allows while still riding through 5 sunless days. HeatMap Node does not need a larger panel or cell.

### Radio

At the 15 min default, each node sends 96 uplinks of about 20 bytes a day, within FieldNode's airtime plan. Seven days of 15 min means is about 13 kB, a small fraction of FieldNode's 16 MB flash.

### Wind load and mass

At a 35 m/s gust the dynamic pressure is about 0.74 kPa. With assumed drag coefficients (sphere 0.5, plates and boxes 1.2) the forces are about 6 N on the globe, 15 N on the shield, 18 N on the anemometer, 51 N on the FieldNode panel and 16 N on the enclosure. The sensor-arm loads give about 17 N·m at the arm root, well within a 25 mm aluminium tube and a two-band clamp by inspection; this will be checked at TRL 3.

Mass is about 3.3 kg: FieldNode core 1.7 kg (from its precis), arm and clamp 0.6 kg, shield 0.3 kg, globe 0.25 kg, anemometer 0.3 kg, harness and hardware 0.15 kg.

### Cost

About $120 for the sensor head (BOM lines 2 to 10) and about $246 with the FieldNode core (line 1, about $126). The sensor head meets the $120 budget with no margin; the full node is about twice it. See the review note for the proposed options.

## Key design choices

All proposed, awaiting Amish.

1. **Build on FieldNode** rather than a separate power and radio design. Reuses a shared, field-hardened core; costs about $126 per node.
2. **Standard 150 mm globe** rather than a 38 to 40 mm table tennis ball globe. The standard size matches published globe equations and the Liljegren model; the small globe is cheaper and faster to respond but more sensitive to wind and less comparable.
3. **Derived WBGT** rather than a wetted natural wet-bulb sensor, which needs a water reservoir and wick care at every node.
4. **Fit an anemometer** rather than use wind from the nearest official station, because street wind differs strongly from airport wind and MRT is sensitive to it.
5. **Naturally ventilated shield** rather than a fan-aspirated shield. A fan would cut radiation error but adds power, noise and a wear part.
6. **Arm at about 2.8 m** to deter tampering, with a correction to pedestrian height studied at TRL 3, rather than at 1.5 to 2 m where the data is most representative (R9 not met).
7. **Open data, environmental channels only** (R12).

## Safety

> **Safety:** Mounting on street poles is work at height next to traffic. Install only with the pole owner's written permission, by trained crews, with a stable ladder or lift, fall protection and traffic management as local rules require, and keep clear of overhead power lines and any live parts of lighting poles. Check that the pole can carry the added wind load.
>
> **Safety:** The FieldNode core contains a LiFePO4 cell of about 19 Wh. Fuse it at the holder, charge only within the maker's temperature limits, and do not install a swollen, damaged or wet cell.
>
> **Safety:** The black globe and the arm can exceed 60 °C in full sun (estimate). Let them cool or wear gloves before handling. Cut edges on the aluminium arm and copper sphere must be deburred, and anemometer cups spin; stop them before working near them.
>
> **Safety:** HeatMap Node data is for planning and research. It is not an official heat warning, and it must not be used to decide whether a particular person is safe to work or exercise without the responsible agency's guidance.

## Open questions

- [ ] Budget: how to count the shared FieldNode core against the $120 budget (see the review note).
- [ ] Mounting height: what do pole owners allow, and how large is the difference between 2.8 m and pedestrian height on a hot, calm afternoon?
- [ ] Shield error in calm, sunny conditions without a fan; is a small solar-powered fan worth it?
- [ ] Which anemometer meets R4 at the low end at this price?
- [ ] Globe response time for 15 min reporting, and whether a thinner shell or smaller globe helps.
- [ ] How often must nodes be recalibrated in CalRig, and how are dust and fading of the black paint handled?
- [ ] Data model and hosting: TwinKit, CityTwin or a public platform, and who publishes it?
- [ ] Night-time value: are 15 min means enough to capture nights that do not cool, when the body cannot recover from daytime heat?
