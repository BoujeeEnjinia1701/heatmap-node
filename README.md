# HeatMap Node

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827) [![DOI](https://zenodo.org/badge/1388476860.svg)](https://zenodo.org/badge/latestdoi/1388476860) [![REUSE compliant](https://github.com/BoujeeEnjinia1701/heatmap-node/actions/workflows/reuse.yml/badge.svg)](https://github.com/BoujeeEnjinia1701/heatmap-node/actions/workflows/reuse.yml) [![Archived in Software Heritage](https://archive.softwareheritage.org/badge/origin/https://github.com/BoujeeEnjinia1701/heatmap-node/)](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/BoujeeEnjinia1701/heatmap-node)

**Area:** Smart Cities · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** $130 USD for the sensor head (FieldNode core and its pole adapter budgeted separately) · **Difficulty:** 2 of 5

A street-level heat and humidity node that measures heat stress (including a globe temperature) to map urban heat islands block by block.

![HeatMap Node: street-pole heat stress sensor with a black globe thermometer, product render](media/render-hero.png)

[Exploded render](media/render-exploded.png) · [Detail render](media/render-detail.png) · [Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement (PDF)](cad/drawings/HMN-DWG-001.pdf) · [Calculations](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Concept rationale

Block-level heat data lets a city put shade, trees, cool surfaces and cooling centers where they protect the most people, and then check whether they worked. Air temperature alone misses what makes a sunny street dangerous: radiant heat from the sun and from hot walls and pavement. HeatMap Node therefore measures what is needed to estimate the standard heat stress index, wet bulb globe temperature (WBGT, [ISO 7243:2017](https://www.iso.org/standard/67188.html)): air temperature, humidity, a black globe temperature and wind. WBGT is then estimated with a published open method ([Liljegren et al., 2008](https://doi.org/10.1080/15459620802310770)) instead of a wetted wick that would need refilling at every pole.

It is open and garage-buildable because mapping heat block by block takes many nodes, and the hottest neighborhoods are often the ones with the least money to buy them. The sensor head is a copper float ball, printed shield plates, an aluminium tube and off-the-shelf sensors, and it plugs into the lab's shared FieldNode core for solar power and LoRaWAN radio. Community groups, schools and cities can build, calibrate (with CalRig) and audit the same design, and the data stays open.

## Burning platform

WHO estimates about 489,000 heat-related deaths each year between 2000 and 2019, 45 % of them in Asia and 36 % in Europe ([WHO](https://www.who.int/news-room/fact-sheets/detail/climate-change-heat-and-health)). In one summer, 2022, an estimated 61,672 people died of heat across 35 European countries ([Ballester et al., *Nature Medicine*, 2023](https://www.nature.com/articles/s41591-023-02419-z)).

Cities concentrate the risk and spread it unevenly. The US EPA reports urban daytime temperatures about 1 to 7 °F (about 0.5 to 4 °C) above outlying areas ([US EPA](https://www.epa.gov/heatislands/learn-about-heat-islands)). Formerly redlined US neighborhoods have land surface temperatures about 2.6 °C higher than other neighborhoods, and up to 7 °C higher in some cities ([Hoffman et al., 2020](https://www.mdpi.com/2225-1154/8/1/12)). Official stations are too few to see these block-to-block differences, and satellites measure surfaces, not the heat a person on the pavement feels.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Municipal climate and urban forestry | Target tree planting, shade (with CoolShade) and cool surfaces block by block, and measure the effect before and after |
| Public health | Neighborhood heat stress during heat waves to direct outreach and cooling center hours |
| Construction and outdoor work | Local WBGT estimates for work and rest planning on and near sites |
| Transit and school operators | Heat stress at bus stops, platforms and schoolyards |
| Urban design and real estate | Evidence for street and building design choices that reduce radiant heat |
| Research and education | A calibrated, repeatable street-level method for heat studies and classroom science |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| United States | In all but 6 of the 175 largest urbanized areas, the average person of color lives in a census tract with higher surface urban heat island intensity than non-Hispanic white residents ([Hsu et al., 2021](https://www.nature.com/articles/s41467-021-22799-5)) |
| Europe | About 61,672 heat-related deaths in summer 2022 across 35 countries ([Ballester et al., 2023](https://www.nature.com/articles/s41591-023-02419-z)); dense cities with older, unshaded streets need local evidence for cooling plans |
| South and Southeast Asia | Asia accounts for about 45 % of global heat-related deaths ([WHO](https://www.who.int/news-room/fact-sheets/detail/climate-change-heat-and-health)); rapidly growing cities include informal settlements that WHO notes are often hotter than other urban areas |
| Sub-Saharan Africa | Africa warmed by about 0.3 °C per decade over 1991 to 2022, and WMO describes big gaps in weather observations there ([WMO](https://wmo.int/news/media-centre/africa-suffers-disproportionately-from-climate-change)); low-cost nodes can add street-level data where stations are few |
| North Africa and the Middle East | WMO reports particularly rapid warming and extreme heat in North Africa ([WMO](https://wmo.int/news/media-centre/africa-suffers-disproportionately-from-climate-change)); outdoor workers and dense old cities face high radiant loads |

## What sparked the idea

The idea traces back to US Marine Corps training sites in the late 1940s and early 1950s. Heat flags were introduced there to address high rates of heat illness, but the temperature readings behind them did not account for sunlight or wind ([Human Performance Resource Center, US Department of Defense](https://www.hprc-online.org/physical-fitness/environmental-extremes/military-heat-flag-conditions-explained)). Yaglou and Minard's answer in 1957 was wet bulb globe temperature, which adds a black globe to catch the sun, and a review of the index's history records that it cut both heat casualties and lost training time ([Budd, *Journal of Science and Medicine in Sport*, 2008](https://doi.org/10.1016/j.jsams.2007.07.003)). HeatMap Node takes the same black globe, wind reading and shaded air temperature off the training ground and onto city street poles, where the neighborhoods hit hardest by heat are often the least measured.

## Problem

Heat waves kill more people than most other weather hazards, and cities lack fine-grained data on where heat is worst. Full problem statement: [docs/01-problem.md](docs/01-problem.md).

## Concept

A sensor arm clamps to an existing street pole with its axis at 2.8 m, points toward the equator and plugs into a FieldNode core (solar panel, LiFePO4 cell, LoRaWAN radio, and a sun shield for hot sites) mounted below it. It carries a fan-aspirated radiation shield with a temperature and humidity sensor, a standard 150 mm black globe with a thermistor at its center, and a small cup anemometer. Every 3 min the fan runs for 6 s before the air is read. Nodes send 15 min means; a server computes mean radiant temperature and WBGT, flags calm intervals below the anemometer's start-up, and maps the results block by block. Only environmental values leave the node: no camera, microphone or personal data.

TRL 3 calculations ([HMN-CAL-001](docs/04-calcs/01-sizing.md)): in a worked example, 35 °C air at 40 %RH with a 50 °C globe at 1 m/s gives a mean radiant temperature of 74.8 °C and WBGT of 31.7 °C. With the fan the shield reads 0.43 °C high in full sun at any wind speed (1.04 °C at 1 m/s without it), and the sensor input errors add up to ±0.30 °C of WBGT. The sensors and fan draw 35 mW against FieldNode's 100 mW allowance, the sensor head weighs 1.91 kg, and the arm has a factor of 13.4 on yield in a 35 m/s gust. Not met on paper: pedestrian measurement height (sensors at about 2.7 m). The sensor head costs $127 against its $130 budget; the full node with the FieldNode core, sun shield and pole adapter is $268. WBGT accuracy against a reference meter, installation time and calibration of the assembled globe are at risk. With the arm toward the equator, the sensor head shades part of the FieldNode panel near noon; a fix is awaiting review.

Full design precis: [docs/02-concept.md](docs/02-concept.md). Requirements: [docs/03-requirements.md](docs/03-requirements.md).

## Key components

1. FieldNode core with its hot-climate sun shield (enclosure, 6 W panel, LiFePO4 cell, LoRaWAN radio)
2. Multi-plate radiation shield
3. Air temperature and humidity sensor (SHT45)
4. Black globe, 150 mm copper sphere, matte black
5. Globe temperature probe (NTC at the center)
6. Cup anemometer
7. Sensor arm, 25 mm aluminium tube
8. Arm clamp: formed sheet 120° V-saddle with stainless strap bands for 60 to 200 mm poles
9. Sensor harness with M12 plugs
10. Hardware and consumables
11. Secondary retention lanyards for the globe and shield
12. Pole adapter that seats the FieldNode core on street poles
13. Aspiration fan and cowl on the shield

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Street furniture and pole mounts must be installed only with the asset owner's permission, by trained crews, with fall protection and traffic management as local rules require. Keep clear of overhead power lines and live parts of lighting poles.
>
> The FieldNode core contains a LiFePO4 cell: fuse it, charge only within the maker's temperature limits and never install a damaged or wet cell. The black globe and arm get hot in the sun (about 67 °C at 50 °C air, HMN-CAL-001), the anemometer cups spin, and the shield fan starts on its own every 3 min; unplug the sensor lead before working on it. The globe and shield are backed by stainless lanyards so that a failed fixing does not drop them onto the street.
>
> HeatMap Node data is for planning and research, not an official heat warning.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (HMN-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `HMN-PRC-001/v1.0`.

## Credits

Designed by Amish Chadha. See [CONTRIBUTORS.md](CONTRIBUTORS.md) for roles. To cite this design, use [CITATION.cff](CITATION.cff) (GitHub shows it as "Cite this repository").

AI assistance (Claude) was used to accelerate concept renders, prototype documentation and first-pass sizing calculations. Design direction and all decisions are Amish Chadha's, recorded in this repository's decision records (`docs/decisions/`).

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab.
