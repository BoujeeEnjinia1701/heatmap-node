---
doc_id: HMN-REG-001
title: HeatMap Node regulatory and standards register
project: HeatMap Node
doc_type: Regulatory register
version: "0.1"
status: Draft
date: 2026-11-01
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-01
    author: Amish Chadha
    change: "First register at the kit 1.9.1 upgrade; sources checked 2026-11-01; anything marked to assess needs a qualified reviewer"
---

# HeatMap Node regulatory and standards register

Which standards and regulations bear on a street-pole heat stress node that carries a solar cell, a LoRa radio and no personal data. Not legal advice; anything marked "to assess" needs a qualified reviewer before any product claim. Nothing here is certified: the node is a research and educational prototype at TRL 3. Method: STANDARDS section 23.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | ISO 7243:2017, WBGT index for heat stress | International | Definition of the wet bulb globe temperature index and its weights (0.7 natural wet bulb, 0.2 globe, 0.1 air outdoors with solar load) | Defines the quantity the node reports (PR-005); the node supplies the index as data and does not assess exposure | Design lead | Applies; met by design (HMN-CAL-001 B2) |
| G2 | ISO 7726, instruments for measuring physical quantities of the thermal environment | International | Accuracy classes and response times of globe, air and humidity instruments | Reference for the 150 mm globe, the air temperature class and response; edition and class limits to check against the paper | Design lead | To assess |
| G3 | NIOSH Publication 2016-106, criteria for occupational exposure to heat | United States | Recommended exposure limits that use WBGT with work rate and acclimatization | Context for users; the node is not an exposure-limit instrument | Design lead | Does not apply to the product; context only |
| G4 | OSHA heat exposure guidance | United States | Employer programs for heat | Employers may read the data; the node is not a compliance instrument | Partner | Does not apply; to assess before any claim to employers |
| G5 | 47 CFR 15.247 (FCC), digital modulation and hopping systems in 902 to 928 MHz | United States | Dwell time and power for the LoRa radio | One uplink of 247 ms at SF9 is under the 400 ms dwell (STEM S16); the radio module's grant is FieldNode's | FieldNode lead | Applies; met by design at the HeatMap level; module certification to assess in FieldNode |
| G6 | LoRa Alliance RP002-1.0.4 regional parameters | US915 plan | Channels, data rates, dwell | Fixes the airtime budget (HMN-CAL-001 G2) | Design lead | Applies; met by design |
| G7 | 47 CFR Part 15 Subpart B, unintentional radiators | United States | Emissions from the electronics (fan, MCU) | The fan and sensor board are inside FieldNode's emissions envelope | FieldNode lead | To assess |
| G8 | IEC 60529, degrees of protection (IP code) | International | IP65 for the enclosure | FieldNode's enclosure carries IP65 (PR-008); HeatMap adds M12 sealed leads and a PTFE vent cap on the SHT45 | Design lead | Met by design; certification needed later |
| G9 | UN Manual of Tests and Criteria, Part III, 38.3 (lithium cells) | International transport | Cell safety tests for shipping | Applies to cells shipped inside FieldNode; the cell supplier's report is needed | FieldNode lead | Certification needed later |
| G10 | RoHS 2011/65/EU, WEEE 2012/19/EU, Radio Equipment Directive 2014/53/EU | European Union | Substances, end-of-life, radio conformity if the node is sold in the EU | Not for a prototype; relevant only if a partner sells in the EU | Partner | To assess |
| G11 | AASHTO structural supports for highway signs, luminaires and traffic signals | United States | Wind loads and fatigue of attachments to light and signal poles | Pole owners may ask for the node's wind area and moment; the head's 35 m/s case is in HMN-CAL-001 H1 to H6 | Pole owner | To assess |
| G12 | Pole-owner attachment permission (city or utility) | Local | Permission and liability for clamped attachments | Needed for every pole; no drilling | Partner | Applies; to assess per city |
| G13 | Personal data law (for example GDPR in the EU, state privacy laws in the US) | Local | Personal data | The node holds environmental data only (PR-012); no camera, microphone or radio scanning, so personal data law is expected not to apply | Design lead | Does not apply by design; to assess by a lawyer before deployment |
| G14 | WMO Guide to Instruments and Methods of Observation (WMO-No. 8) | International guidance | Radiation shields, siting and exposure of air temperature sensors | Street siting breaks the open-site rule on purpose; the node is a street-level instrument, not a climate station | Design lead | Guidance; does not apply to the product |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

All accessed 2026-11-01.

- ISO 7243:2017, https://www.iso.org/standard/67188.html.
- NIOSH 2016-106, https://www.cdc.gov/niosh/docs/2016-106/default.html.
- OSHA, "Heat exposure," https://www.osha.gov/heat-exposure.
- FCC, 47 CFR 15.247, https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-15/subpart-C/subject-group-ECFR2a5a6f3d3f3e4a6/section-15.247; 47 CFR Part 15, https://www.ecfr.gov/current/title-47/part-15.
- LoRa Alliance, RP002-1.0.4 Regional Parameters, https://resources.lora-alliance.org/technical-specifications/rp002-1-0-4-regional-parameters.
- IEC, IP ratings, https://www.iec.ch/ip-ratings.
- UNECE, UN Manual of Tests and Criteria, https://unece.org/transport/dangerous-goods/un-manual-tests-and-criteria.
- AASHTO store, structural supports specification, https://store.transportation.org/Item/CollectionDetail?ID=205.
- WMO, CIMO Guide, https://www.wmo.int/pages/prog/www/IMOP/CIMO-Guide.html.
- ISO 7726, EU directives (RoHS, WEEE, RED) and the privacy laws: listed by name only; not retrieved in this session, so editions and obligations are "to assess".
