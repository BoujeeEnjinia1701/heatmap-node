---
doc_id: HMN-MKT-001
title: HeatMap Node market and viability
project: HeatMap Node
doc_type: Market and viability
version: "0.1"
status: Draft
date: 2026-11-01
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-01
    author: Amish Chadha
    change: "First market note at the kit 1.9.1 upgrade; prices checked 2026-11-01"
---

# HeatMap Node market and viability

Cities, public health departments, researchers and community groups that want block-level heat stress data would use it; it competes with hand-held heat stress meters and weather stations that give one point, and an open design matters because a city can then build, repair and audit a dense network itself. Prices are cited with the date checked (2026-11-01). Method: STANDARDS section 23.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| City heat offices and public health | Hot US cities, first candidate the City of Phoenix Office of Heat Response and Mitigation (nothing agreed) | Kestrel 5400 Heat Stress Tracker, a hand-held WBGT meter, USD 549 (Kestrel product page, checked 2026-11-01): one point, carried by a person | 136.00 sensor head; 292.00 full node (`bom/bom.csv`, prototype parts only, no labour or shipping) | A fixed, solar-powered, networked node for the same price class as one hand-held meter at about half the cost, so many sites can be read at once |
| Outdoor employers and event organizers | US, any hot region | Extech HT30 heat stress WBGT meter, USD 219.00 (Extech product page, checked 2026-11-01): hand-held, one reading at a time | 292.00 full node | Local WBGT without sending a person to measure it; not a compliance instrument (HMN-REG-001 G4) |
| Researchers and universities | Urban climate groups | Weather stations and WBGT stations: price to assess (not retrieved) | 292.00 full node | Open design, documented error, calibration record, replicable method |
| Community groups and schools | Neighborhood networks, low-income districts | Hand-held meters as above | 292.00 full node | Buildable by a workshop, open data to take to city hall |

## Open route

Who would build it: makerspaces, university labs, NGOs and a city's own workshop, from the open files (CERN-OHL-S-2.0 hardware, MIT software) on the Design Molecule Labs GitHub. The saddle is sheet aluminium, the shield and cowl are printed, and the electronics are catalogue parts on the shared FieldNode core, so no part needs a factory. The strong copyleft hardware licence keeps improvements open. Viability depends on a partner city agreeing to attach nodes to poles and on field data showing the derived WBGT is close enough (PR-005); both are open. No sales, pricing or business plan is proposed at TRL 3. A cost per node below the price of one hand-held meter (USD 136 for the head, USD 292 for the node, parts only) is the argument; installation, labour, shipping and upkeep costs are to assess.

## Sources

- Kestrel Instruments, Kestrel 5400 Heat Stress Tracker, https://www.kestrelinstruments.com/kestrel-5400-heat-stress-tracker, USD 549, accessed 2026-11-01.
- Extech, HT30 Heat Stress WBGT Meter, https://www.extech.com/products/HT30, USD 219.00, accessed 2026-11-01.
- `bom/bom.csv` (indicative prices from HMN-CAL-001 and the build plan).
- US EPA, "Learn about heat islands," https://www.epa.gov/heatislands/learn-about-heat-islands, accessed 2026-11-01.
