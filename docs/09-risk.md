---
doc_id: HMN-RSK-001
title: HeatMap Node risk register and hazard analysis
project: HeatMap Node
doc_type: Risk register and hazard analysis
version: "0.1"
status: Draft
date: 2026-11-01
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-01
    author: Amish Chadha
    change: "First register at the kit 1.9.1 upgrade: project risks, preliminary hazard analysis and design FMEA for options A and B"
---

# HeatMap Node risk register and hazard analysis

The biggest risks are that the derived WBGT does not match a reference instrument on a street (PR-005), that a head or globe falls from a pole in wind, and that nobody keeps the nodes up. The hazards that matter most to people are a fall from a ladder at a pole and contact with an energized street light pole; both are controlled by procedure, not by this design alone. Method: STANDARDS section 23. Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high).

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | Derived WBGT is off in streets | Liljegren model not validated for street canyons; calm intervals | Maps misguide siting (PR-005 at risk) | 3 | 4 | Design lead | Collocate with a reference WBGT meter at TRL 4; consider option B reference heads (HMN-OPT-001) |
| R2 | No partner pole | Cities slow to grant attachment | No trial network | 3 | 4 | Amish | Approach the first candidate city after Amish agrees; nothing is agreed (HMN-DEC-001) |
| R3 | Cost grows beyond the target | Prices change; the head is already USD 6 over | Network too costly | 4 | 3 | Design lead | Savings in HMN-DEC-001; Amish decides any change to the target |
| R4 | Sensors at 2.8 m misrepresent pedestrians | Height chosen for reach and vandal resistance | Bias of 0.2 to 0.8 °C in strong sun (PR-009) | 4 | 2 | Design lead | Report the correction; test 2.0 m against 2.8 m (HMN-DEC-001 O2) |
| R5 | FieldNode changes under the head | Shared core is updated in its own repo | Interface drift (adapter, ports) | 3 | 3 | Design lead | Interfaces listed in HMN-DEC-001, to confirm 7; cross-repo note in REVIEW.md |
| R6 | Upkeep not kept | Volunteers, no funding | Fouled shields, stalled fans | 3 | 3 | Partner | Visit interval and steps in the plan (PR-018); option A chosen partly for this reason |
| R7 | Theft or vandalism | Visible head at 2.8 m | Loss of node | 2 | 3 | Partner | Height, stainless bands that need a tool to undo, no scrap value (aluminium and ASA only) |
| R8 | Data misread as a heat warning | Maps shared without context | Wrong action by the public | 2 | 4 | Amish | State that the node supplies data and public warnings stay with the responsible agency (HMN-PRB-001, Out of scope) |
| R9 | Cell or electronics fail in heat | 57.2 °C interior at 50 °C air | Node offline; cell damage | 3 | 4 | FieldNode lead | Charge cut-off (PR-016, STEM S25) |

## Preliminary hazard analysis

Table 2. Hazards.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Fall from a ladder or lift at 2.8 m | Fitting the arm on a street pole | Serious injury | 5 | 3 | Two people; lift or secured ladder; fit only where the owner permits; plan notes (HMN-BLD-001) | 3 |
| H2 | Contact with an energized pole | Street light pole faulted to ground | Electric shock | 5 | 1 | Only poles the owner has isolated or checks; owner's technician; no work on a wet pole | 2 |
| H3 | A part falls on a passer-by | Band slip, boss failure, wind | Head injury | 5 | 2 | Lanyards on the globe and the shield; clamp twist factor 2.5; 35 m/s case (HMN-CAL-001); check at the first visit | 3 |
| H4 | Lithium cell fault | Charging in the heat; crushing; short | Fire, venting | 5 | 2 | LiFePO4 chemistry; charge cut-off (O4); cell and BMS in FieldNode's own safety case | 3 |
| H5 | Burns from hot parts | Globe up to 67 °C and shield plates 65 to 75 °C in the sun | Minor burn to a person fitting or servicing | 2 | 3 | Wear gloves; let parts cool; labels | 1 |
| H6 | Cuts and pinches | Formed aluminium edges, strap bands, fan | Cuts | 2 | 3 | Edges broken (cad_check edge breaks); finger guard on the fan; gloves | 1 |
| H7 | Fan entanglement | Cable or finger in a 60 mm fan | Minor injury | 2 | 2 | Cowl with legs over the fan; fan stops between readings | 1 |
| H8 | Manual handling | Carrying a 4 to 5 kg node up a ladder | Strain | 2 | 3 | Lift the core and the arm separately; hoist rope | 1 |
| H9 | Mistaken for a surveillance device | A box on a pole | Public concern | 2 | 3 | Label the node; no camera, microphone or radio scan (PR-012); publish the data format | 1 |
| H10 | Standing water in the reservoir (option B only) | A closed bottle with a 6 mm gland | Mosquito or biofilm growth | 2 | 2 | Closed bottle; inspect at refill (STEM S36) | 1 |

## Design FMEA (first pass, P3)

Table 3. Failure modes, sorted by RPN. RPN = severity x occurrence x detection. F11 and F12 are option B only; all others are option A (F1 to F10, F13 to F15), and most also hold for B.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Shield plates and gaps | Pass air over the sensor | Gaps blocked by insects, dust or a nest | Air temperature reads high in the sun | Sheltered 12 mm gaps; cowl lid | 4 | 4 | 4 | 64 | Inspect gaps at each visit (PR-018); screened inlet to consider (STEM S27) |
| F13 | Aspiration fan | Keep the shield ventilated | Fan stops or slows without any signal | Air temperature reads 1 to 2 C high in sun, unnoticed | Dust, bearing wear, about 1.75 M starts in 10 years | 4 | 3 | 4 | 48 | Add a tach or airflow check to the sensor step response; flag stuck readings (independent review) |
| F14 | Black globe | Read radiant heat | Rain or dew cools the globe by evaporation; a bird perches on it; dent in the 0.4 mm shell | Globe temperature reads low or biased | Weather, wildlife | 3 | 4 | 4 | 48 | Flag rain from the humidity channel; spikes on the globe top to consider |
| F8 | FieldNode cell | Store energy for 5.75 days | Charges above its rated temperature in the 57.2 °C interior | Capacity fades; at worst a cell fire | Sun load at 50 °C air | 5 | 2 | 4 | 40 | Cut charging above the cell's limit in FieldNode firmware (STEM S25, PR-016, HMN-DEC-001 O4) |
| F15 | Arm and clamp | Carry the head in wind | Fatigue crack at the bolt holes at the arm root | Arm drops or twists | Wind-induced vibration over years | 5 | 2 | 4 | 40 | Bolt holes at the root to check at TRL 4 (STEM S9); inspect at each visit |
| F2 | Aspiration fan | Draw 4.0 L/s through the stack | Bearing wears or stalls | Shield error rises to 1.04 °C at 1 m/s; reading biased in calm sun | Dust, heat, 6 s run every 3 min | 4 | 3 | 3 | 36 | Flag a fan fault by the sensor's own step response; spare fan; fan curve to measure (S7) |
| F5 | Globe probe | Measure globe temperature | Bead drifts or leaks moisture | Globe reading biased | Epoxy ageing, moisture in the boss | 3 | 3 | 4 | 36 | Recalibrate in CalRig yearly; sealed boss |
| F12 | Wick (option B) | Carry water to the sensor | Dust and salts block it | Wet bulb reads high | Street dust; hard water | 3 | 4 | 3 | 36 | Distilled water; change the wick at each visit (S35) |
| F3 | Globe and hanger tube | Hold the 150 mm black globe | Hanger tube or boss fails; globe falls | Globe lost; falls on the street | Wind and fatigue of the soldered boss; vibration | 5 | 2 | 3 | 30 | Secondary lanyard (line 11); check the boss at each visit (HMN-DEC-001, to confirm 1) |
| F4 | Clamp saddle and strap bands | Hold the arm to the pole | Band slips or relaxes; arm twists | Readings face the wrong way; at worst the head falls | Preload below 1,000 N; rubber trim creep | 5 | 2 | 3 | 30 | Check the preload with the band tool (HMN-DEC-001, to confirm 6); lanyard to the pole; re-tighten at the first visit |
| F6 | SHT45 membrane cap | Admit air, keep out water | Cap clogged with dust | Humidity lags and reads wrong | Dust and salt | 3 | 3 | 3 | 27 | Replace the cap at each visit; reference reading from option B head where fitted |
| F7 | Cup anemometer | Measure wind | Bearing stalls or start-up above 0.8 m/s | Calm intervals misread as zero | Wear, dust, ice | 3 | 3 | 3 | 27 | Calm share flagged per interval (PR-004); replace at 2 years |
| F9 | M12 leads and plugs | Connect sensors to FieldNode | Water enters a plug; UV cracks the jacket | Channel lost | Loose plug; sun | 3 | 3 | 3 | 27 | IP67 plugs; drip loops; cable ties |
| F10 | Printed ASA parts | Hold plates and the cowl | Cracks or warps at 65 to 75 °C | Plate gaps close; cowl sags | Filament with low heat deflection | 3 | 3 | 3 | 27 | Specify the filament's heat deflection above 90 °C (S23); inspect at each visit |
| F11 | Reservoir bottle (option B) | Hold water for the wick | Freezes and splits; runs dry | No wet-bulb reading; water leak | Brim fill; hot dry spell | 3 | 4 | 2 | 24 | 85 % fill line and a channel flag (K1); 5 day refill in hot spells (K1b) |

Scores are the author's judgement at TRL 3 and have not been reviewed with a co-design partner. Items at 40 or above come first in the field comparison.

## Sources

- ISO 7243:2017, https://www.iso.org/standard/67188.html, accessed 2026-11-01 (hazard context).
- HMN-STM-001 rows S7, S11, S22 to S27, S31 to S36 and HMN-CAL-001 sections H and F (design evidence).
