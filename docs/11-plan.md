---
doc_id: HMN-PLN-001
title: HeatMap Node project plan
project: HeatMap Node
doc_type: Project plan
version: "0.1"
status: Draft
date: 2026-11-01
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-01
    author: Amish Chadha
    change: "First plan at the kit 1.9.1 upgrade; P4 to P6 shown as planned work only"
---

# HeatMap Node project plan

The repo is at stage P3 (TRL 3, constructable design, nothing built). The next gate is Amish's choice between option A and option B (HMN-DDR-004) and his review of this upgrade; the decision requested is in the last section. Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Problem, users, requirements | Design lead | HMN-PRB-001, HMN-URS-001, HMN-PRS-001, HMN-RTM-001 | Done at P3; to review with a co-design partner |
| STEM check and calculations | Design lead | HMN-STM-001, HMN-CAL-001 | Done at P3; 15 rows plausible |
| Concept options | Design lead | HMN-OPT-001, HMN-DDR-004 | Done; choice proposed, awaiting Amish |
| Detailed CAD (D3) | Design lead | `cad/src/model.py`, `cad/fidelity.json`, STEP files, drawing HMN-DWG-001 | Done for options A and B |
| Build plan | Design lead | HMN-BLD-001 | Done for option A (paper only) |
| Regulatory, risk, market | Design lead | HMN-REG-001, HMN-RSK-001, HMN-MKT-001, HMN-FEA-001 | First pass done; items to assess |
| Partner and pole | Amish | Partner city, pole, attachment permission | Not started; nothing agreed |
| Renders | Coordinator | `media/options.png`, product renders | Rendered by the coordinator on Amish's Mac |
| Prototype build, field comparison | Partner | Built node, collocation with a reference WBGT meter | Planned (P4), on hold while the stage cap is P3 |

## Resources needed

Table 2. Resources (for planned P4 work; estimates, nothing ordered).

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Parts for one head and FieldNode core | Built node | Collect and assemble over a few days | 292.00 (`bom/bom.csv`) |
| Reference WBGT meter on loan | Collocated comparison | One partner site | To assess |
| Pole access and a lift or ladder with a second person | Fitting | Half a day | To assess |
| Sheet-metal forming and a printer | Saddle, shield and cowl | Workshop time | To assess |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 to P2 | Problem, concept, requirements, media | Done |
| P3 | Constructable design, calculations, STEM check, options, D3 CAD, build plan | Done; awaiting Amish's review and choice |
| P4 | Prototype built and bench tested | Planned only |
| P5 | Field comparison against a reference meter | Planned only |
| P6 | Pilot network with a partner | Planned only |

## Next steps and decision requested

Decision requested from Amish: choose option A, option B or a hybrid (HMN-DDR-004, the scores 140 and 129 are within 10 %), and say whether to ask FieldNode for a cell charge cut-off (O4). Recommended next step: stop at TRL 3, review this upgrade, and if the design is wanted, decide whether the repo advances to TRL 4 once the portfolio cap allows.

## References

- ISO 7243:2017, https://www.iso.org/standard/67188.html.
- Liljegren, J. C., R. A. Carhart, P. Lawday, S. Tschopp, and R. Sharp. "Modeling the Wet Bulb Globe Temperature Using Standard Meteorological Measurements." *Journal of Occupational and Environmental Hygiene* 5 (2008): 645 to 652. https://doi.org/10.1080/15459620802310770.
- US EPA. "Learn about Heat Islands." https://www.epa.gov/heatislands/learn-about-heat-islands.
