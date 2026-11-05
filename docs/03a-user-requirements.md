---
doc_id: HMN-URS-001
title: HeatMap Node user requirements
project: HeatMap Node
doc_type: User requirements
version: "0.1"
status: Draft
date: 2026-11-01
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-01
    author: Amish Chadha
    change: "First draft at the kit 1.9.1 upgrade, written from the users and stakeholders in HMN-PRB-001 v0.7 and used to score the concept options (HMN-OPT-001); each need traced to product requirements in HMN-PRS-001; to review with a co-design partner"
---

# HeatMap Node user requirements

What the people who will use, host and pay for a HeatMap network need, written from their side. The fourteen needs below come from the users and stakeholders in HMN-PRB-001 (Tables 1 and 2) and from the 2026-09-25 requirements work. They score the concept options (HMN-OPT-001) and are met by the product requirements in HMN-PRS-001 (links in HMN-RTM-001). They are a desk draft until a co-design partner, the first candidate being the City of Phoenix Office of Heat Response and Mitigation (HMN-DEC-001), reviews them with the people who would use the data and fit the nodes. Method: STANDARDS section 22.

Table 1. User requirements.

| ID | Category | Title | Need | Priority | Source |
| --- | --- | --- | --- | --- | --- |
| UR-001 | Performance | Street-level heat stress | The node reports the heat a person feels on the street (heat stress, not only air temperature), with the air temperature, humidity and wind that explain it | High | City heat officer, public health department (PRB Table 1) |
| UR-002 | Performance | Numbers I can trust | The readings are accurate enough to compare blocks and to stand beside a reference instrument, and the error is stated | High | Researcher, public health department |
| UR-003 | Deployment and assembly | Fits the poles we have | Fits existing street light, sign or utility poles without drilling or welding | High | City heat officer, pole owner |
| UR-004 | Deployment and assembly | Quick to fit | Two people fit a node from a ladder or lift in about half an hour | Medium | Pole owner, community group |
| UR-005 | Logistics | Runs without mains | The node runs from its own solar panel through several days without sun | High | City heat officer, pole owner |
| UR-006 | Performance | Near-real-time data | Data reaches the gateway within about half an hour, so a heat wave can be followed | High | Public health department |
| UR-007 | Cost | Cheap enough for a network | The sensor head costs little enough that tens of nodes per neighborhood are possible | High | City heat officer, community group |
| UR-008 | Environment and durability | Survives the street | Works through -20 to +50 °C at the node, full sun, driving rain, dust and wind gusts | High | City heat officer, pole owner |
| UR-009 | Regulatory | Environmental data only | No camera, microphone or device tracking; nothing that identifies a person | High | Community group, residents |
| UR-010 | Usability | Open, documented data | Readings come with the node's location, height and calibration record in an open, documented format | Medium | Researcher, community group |
| UR-011 | Maintenance | Little upkeep | A visit is needed rarely and takes little skill or consumables | Medium | Pole owner, community group |
| UR-012 | Safety | Safe overhead | Nothing falls on passers-by in wind, the node adds little load to the pole, and edges are safe | Medium | Pole owner, residents |
| UR-013 | Performance | Measured where people walk | The sensors sit at or near pedestrian height | Medium | Public health department, researcher |
| UR-014 | Logistics | Buildable by a community | A community group or workshop can build it from open files, common parts and a printer | Medium | Community group |

Categories: deployment and assembly, performance, usability, safety, environment and durability, logistics, maintenance, cost, regulatory. Priorities: High, Medium, Low.
