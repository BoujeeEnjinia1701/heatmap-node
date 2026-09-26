---
doc_id: HMN-PRB-001
title: HeatMap Node problem statement
project: HeatMap Node
doc_type: Problem statement
version: "0.5"
status: Draft
date: '2026-09-26'
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
  change: Populate to TRL 2 (problem, users, context, constraints, prior work, open questions)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: "TRL 3 update: budget scope and mounting height per HMN-DDR-001; operating environment aligned with HMN-CAL-001"
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: "Budget top-up approved by Amish: sensor head limit $130"
---

# HeatMap Node problem statement

Cities decide where to plant trees, build shade and open cooling centers with heat data that is too coarse to see the street a person actually walks down. Heat kills in large numbers, it falls hardest on poorer and hotter neighborhoods, and the measure that matters for the body (heat stress, which includes sun and radiant heat from hot surfaces, not only air temperature) is rarely measured at street level at all.

## The problem

Heat is one of the deadliest weather hazards. WHO estimates about 489,000 heat-related deaths each year between 2000 and 2019, 45 % of them in Asia and 36 % in Europe ([WHO fact sheet](https://www.who.int/news-room/fact-sheets/detail/climate-change-heat-and-health)). In the summer of 2022 alone an estimated 61,672 people died of heat in 35 European countries ([Ballester et al., *Nature Medicine*, 2023](https://www.nature.com/articles/s41591-023-02419-z)).

Heat is not spread evenly across a city. The US EPA reports that daytime air temperatures in urban areas run about 1 to 7 °F (about 0.5 to 4 °C) above outlying areas, and nighttime temperatures about 2 to 5 °F (about 1 to 3 °C) higher ([US EPA](https://www.epa.gov/heatislands/learn-about-heat-islands)). Inside cities the differences follow income and history: land surface temperatures in formerly redlined US neighborhoods are about 2.6 °C higher than in other neighborhoods, and up to 7 °C higher in some cities ([Hoffman et al., *Climate*, 2020](https://www.mdpi.com/2225-1154/8/1/12)). WHO notes that informal settlements are often hotter than other urban areas ([WHO fact sheet](https://www.who.int/news-room/fact-sheets/detail/climate-change-heat-and-health)).

Three gaps keep cities from acting on this at block scale:

1. **Official stations are sparse and sited away from streets.** Weather stations are placed in open, grassy sites by design, so they report the background climate, not the hot bus stop or market lane.
2. **Satellites see surfaces, not people.** Land surface temperature maps show hot roofs and roads, but the heat a pedestrian feels depends on air temperature, humidity, wind and radiant heat together.
3. **Air temperature alone understates heat stress in the sun.** The standard occupational index, wet bulb globe temperature (WBGT, [ISO 7243:2017](https://www.iso.org/standard/67188.html)), weights a black globe temperature and a natural wet-bulb temperature because sun and humidity drive heat strain. Low-cost street sensors seldom include a globe.

## Users and context

| User | What they need from the data |
| --- | --- |
| City heat, climate or resilience officer | Block-level maps of heat stress over a season to target trees, shade (see CoolShade), cool surfaces and cooling centers, and to check whether they worked |
| Public health department | Near-real-time heat stress by neighborhood during heat waves, to direct outreach to people at risk |
| Community groups and schools | A node they can build, host and read, and open data they can take to city hall |
| Outdoor employers (construction, delivery, markets) | Local WBGT estimates to set work and rest cycles |
| Researchers | A documented, calibrated, repeatable street-level method that others can replicate |

### Operating environment

- **Mounting:** existing street light, sign or utility poles (60 to 200 mm in diameter), with the asset owner's permission, with the sensor arm at about 2.8 m above the pavement (HMN-DDR-001 D2), pointing toward the equator where the street allows (HMN-DDR-002). HMN-CAL-001 estimates that on a sunny afternoon the air at pedestrian height is 0.2 to 0.8 °C warmer than at the sensors.
- **Climate:** air temperature from about -20 to +50 °C at the node (R8, restated to match under HMN-DDR-002), full sun, rain, dust and salt air near coasts; black globe temperatures can exceed 60 °C in full sun (estimate).
- **Connectivity:** LoRaWAN coverage from a community gateway (for example the lab's TwinKit gateway) or a public network; no mains power at the node.
- **Density:** tens of nodes per neighborhood, so each must be cheap, quick to fit and self-powered.

## Constraints

- Garage-buildable prototype, $130 USD or less for the HeatMap-specific sensor head (raised from $120 by a budget top-up Amish approved on 2026-09-26). The FieldNode core, its sun shield and the pole adapter that seats it on street poles are counted against FieldNode, a shared lab component costed and budgeted in its own repo (HMN-DDR-001 D1 and HMN-DDR-002, decided by Amish on 2026-09-25). HMN-CAL-001 v0.3 prices the head at $127 with the aspiration fan, within this limit.
- Built on the FieldNode core (enclosure, solar, battery, LoRaWAN radio) so that no power or radio design is repeated.
- Privacy: environmental measurements only. No camera, microphone or device tracking.
- No drilling of poles; fit with stainless band clamps.
- Open hardware (CERN-OHL-S-2.0) and open software (MIT); data in an open format.

## Out of scope

- Personal heat stress for an individual (wearables) and indoor heat.
- Issuing official heat warnings. The node supplies data; public warnings stay with the responsible agency.
- Air quality, noise and traffic, which are covered by the AirStreet, NoiseMap and CurbCount concepts.

## Prior work

- **WBGT standard and models.** ISO 7243:2017 defines WBGT as a screening index for heat stress ([ISO](https://www.iso.org/standard/67188.html)). Liljegren and colleagues showed how to estimate WBGT from standard weather measurements, including globe temperature and wind speed ([Liljegren et al., *J. Occup. Environ. Hyg.*, 2008](https://doi.org/10.1080/15459620802310770)); an open implementation of their code is available ([wbgt package](https://github.com/mdljts/wbgt)). HeatMap Node measures the inputs this model needs.
- **Heat and equity studies.** Satellite studies across 175 large US urbanized areas found that the average person of color lives in a census tract with higher surface urban heat island intensity than non-Hispanic white residents in all but 6 of them ([Hsu et al., *Nature Communications*, 2021](https://www.nature.com/articles/s41467-021-22799-5)). These studies use surface temperature; HeatMap Node adds what people experience at street level.
- **Mobile heat campaigns.** Some cities map heat on a single hot day with vehicle-mounted or hand-held sensors. These give good spatial detail but not the season-long, day-and-night record that fixed nodes give.
- **Lab components.** FieldNode (shared outdoor core), CalRig (sensor calibration chamber) and TwinKit (gateway and data layer) are sibling concepts in this lab. CoolShade is the lab's shade structure concept that HeatMap data is meant to help site.

## Open questions

- Which city or community partner hosts the first network, and on whose poles?
- What mounting height is acceptable to pole owners? HMN-CAL-001 gives a first estimate of the height error (up to about 0.8 °C in strong sun); a field comparison of 2.0 and 2.8 m is still needed.
- Which output do users want most: air temperature, WBGT, mean radiant temperature, or a simple heat stress category?
- Who owns and publishes the data?

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design
