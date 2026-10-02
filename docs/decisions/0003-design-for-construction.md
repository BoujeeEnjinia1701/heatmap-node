---
doc_id: HMN-DDR-003
title: HeatMap Node design for construction
project: HeatMap Node
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Accepted by Amish on 2026-10-02, with A1 as recommended"
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Tables 1 and 2 and the item in Table 3 (A1), now decided as recommended and recorded in the design decisions register (HMN-DEC-001).

## Context

On 2026-09-30 Amish asked for every repo to get a prototype build plan that shows how each component is made and how it fits the next, with pictures, and wrote: "If you are realising that the design cannot be built as per concept, fix the design assumptions to match and be physically feasible as you draw the illustrations." The model of HMN-DDR-002 showed what HeatMap Node does but was a massing model: parts floated, overlapped or had no fixing, and the saddle and the pole adapter seated only one pole size. Checking the model with build123d (part overlaps, contacts and clearances) found the thirteen problems below.

The changes keep what the node does: the same sensors, globe, fan-aspirated shield, arm height and direction, sensor positions along the arm, FieldNode core and pole range. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now builds every component separately and runs 399 constructability checks (`python cad/src/model.py --check`): no two parts share material, parts that must touch do touch, parts that must stay apart are at least the stated clearance apart, and poles of 60 and 200 mm touch both faces of each V. All 399 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The arm saddle was drawn as a five-sided tray 110 x 180 x 30 mm with a round cut that fits only a 114 mm pole. Its side walls would hit a larger pole, a sheet cannot be formed into a closed tray with a curved seat, and nothing showed how the pole bears on it. | A channel bent from one 3 mm 5052 sheet: a flat web 120 wide and 180 tall facing out, and top and bottom flanges 40 deep pointing at the pole. Each flange has a 120° V notch cut before bending, lined with 1.5 mm rubber edge trim; the pole bears on the trimmed V edges. | Two straight bends on a cut blank is the simplest shape a sheet can take. The V seats any pole from 60 to 200 mm, which a round seat cannot. The web is 120 mm (was 110) so a 200 mm pole still bears 5 mm inside the notch corners. |
| P2 | The arm butted against the saddle with no fixing. | Two arm cheeks (40 x 40 x 3 mm aluminium angle, 80 mm long): each flat leg is held to the web by two M6 button-head screws from inside the saddle; the arm sits between the upright legs, held by two M6 bolts through both cheeks and the arm, with an aluminium crush sleeve inside the tube at each bolt. | Every joint is face to face and bolted. The sleeves stop the 2 mm tube walls crushing when the bolts are tightened. Two bolts 20 mm apart carry the arm's weight moment as a couple. |
| P3 | The strap bands were drawn as rings round the pole that passed through the saddle. | Each band goes round the back of the pole, through two 3 x 16 mm slots in the web, 55 mm each side of centre, and across the web's front face, 70 mm above and below the arm, clear of the cheeks. | This is how a band holds a bracket to a pole; the buckle sits on the front where it can be reached. |
| P4 | The shield's three rods were drawn as solid bars through plates with no holes and nothing setting the gaps; two rods ran through the fan cowl. The only link to the arm was a 12 mm rod from the arm to the cowl lid, with no fixing. | Four M5 stainless rods on a 92 mm circle, 90° apart, clear of the cowl by 5 mm. Each ring plate is printed with four 10 mm bosses, 12 mm tall, that carry the plate above; acorn nuts below and nuts on the top plate clamp the stack. The two rods in line with the arm continue up through it on 41 mm aluminium spacers, with a nut on top of the arm. | The bosses set the 15 mm pitch with no loose spacers to lose. The rods in tension and the spacers in compression hold the stack rigidly 45 mm below the arm, as the concept placed it. |
| P5 | The fan floated 1 mm above the top plate and the cowl stood on four unfixed posts. | The fan sits flat on the top plate over its 56 mm hole. The printed cowl is a 76 mm lid on four legs that stand on the fan's corners; four M4 x 40 screws pass through lid, legs, fan and top plate, with nuts under the plate. | One set of screws holds fan and cowl. The cowl keeps its 76 mm lid and 30 mm height, so the exhaust and the wind area are unchanged. |
| P6 | The temperature and humidity capsule floated in the middle of the stack. | The third plate from the top is printed with a 22 mm hub on three 4 mm spokes; the capsule is a push fit in its 18.5 mm bore, held by a nylon M3 set screw, at the same height as before. | The capsule stays at the centre of the aspirated air path. Its lead leaves between the second and third plates (see P10). |
| P7 | The globe hung on a solid 12 mm rod that met the probe stem at the same point; the globe boss had no hole. | A hollow M10 x 1 brass threaded tube (lamp rod, 7 mm bore) screws into the globe's boss with a lock nut, passes through 10.5 mm holes in the arm and is held by a nut below and above the arm. The probe runs down inside the tube to the globe centre and leaves at its top. | The hanger and the probe share one path, as on a commercial globe thermometer. The globe stays 45 mm below the arm and its centre where the concept put it. |
| P8 | The anemometer mast stood on the arm top with no fixing. | The mast passes down through 16.5 mm holes in the arm, 30 mm from the tip, and is pinned by one M5 bolt through arm and mast. The arm is 530 mm (was 520) so the mast keeps its place after P1. | A through-mast cannot tip and the pin stops it turning. The cups now reach 668 mm from the pole axis (was 679 mm). |
| P9 | The arm tube had open ends. | A plastic plug in the tip; the root end bears on the web. | Keeps water, insects and nesting out of the tube. The appearance model already showed a plug. |
| P10 | The harness passed through the saddle, the fan, the pole and the FieldNode core. | Two leads from FieldNode ports A and B run under the core to the pole, up the pole 62 mm from its axis (outside both pairs of bands, held by long UV-stable cable ties), round the side of the saddle and along the arm's side. Lead A's tail enters the shield between the second and third plates to the sensor; lead B's tails go to the top of the globe hanger tube and into the foot of the anemometer mast. | Every cable now has a real path that clears every part by at least 0.5 mm. |
| P11 | The lanyards ended at the arm with nothing holding them. | Each lanyard is looped round the arm and closed with its snap hook: one from a hole in the top plate, one from the globe boss. | A loop round the arm backs up the rod and tube fixings; it does not depend on them. |
| P12 | The FieldNode pole adapter was drawn as flat blocks with a shallow round seat that fits one pole size, covering FieldNode's band slots, with no fixing. | Two printed ASA V-blocks 110 x 30 x 38 mm with a 120° V across the full width, two 3.5 x 16 mm band slots right through in line with the FieldNode back plate slots, and two M4 heat-set inserts at FieldNode's V-block screw holes, so FieldNode's own countersunk screws hold them. | The adapter now fits the FieldNode back plate of Rev P3 with no new holes in it, seats 60 to 200 mm poles, and lets FieldNode's band path work as designed. |
| P13 | The FieldNode envelope followed FND-DWG-001 Rev P1. | Updated to Rev P3 (FND-DDR-003): ports and antenna in the front row 55 mm from the box back, band slots and V-block screw holes in the back plate; the back plate is 3 mm nearer the pole with the new adapter. | Keeps the interfaces that the adapter and harness use the same as the FieldNode build plan. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | Sensor head 2.12 kg (was 1.91 kg), within R15's 4 kg [K1], [K2]. Complete node 4.95 kg for information, with FieldNode at 2.61 kg after its own design for construction. | Cheeks, bolts, a fourth rod, spacers, the brass hanger tube and nuts. |
| Cost | Lines 2, 4, 8, 10 and 12 repriced; sensor head $136.00 against the unchanged $130 value-engineering target, $6.00 over it [L1], [L2]. Line 1 follows FieldNode to $148.00 (counted against FieldNode). | Parts added for construction. `budget_usd` is a value-engineering target, not a limit (Amish, 2026-10-01). |
| Wind and clamp | Arm 530 mm: root moment 14.6 N·m, factor 13.0 on yield, tip 0.31 mm at 20 m/s; clamp twist factor 2.5 [H1] to [H5]. | Longer arm, 10 mm. |
| Drawing | HMN-DWG-001 Rev P4; making sketches HMN-DWG-101 to 107 added. | Follows the model. |
| Documents | HMN-CAL-001 v0.4, HMN-REQ-001 v0.6, HMN-PRC-001 v0.6. R13 is now reported against the value-engineering target; no other requirement changed status. | Follows the model. |

*Table 3. Proposed, then accepted by Amish as recommended on 2026-10-02.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | The sensor hub's three 4 mm spokes sit in the aspirated air path, 15 mm above the sensing tip. HMN-CAL-001 does not include their effect on the 0.43 °C shield error. | (a) keep the hub on spokes and include it in the TRL 4 side-by-side shield test; (b) hang the capsule on its lead from a clip on the second plate, with no spokes. | (a): the hub ring and spokes block about 13 % of the 56 mm opening at that one plate, beyond what the capsule itself blocks; a lead-hung capsule can swing against the plates. **Decided 2026-10-02: (a).** |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan HMN-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status: 1 not met (R9), 3 at risk (R5, R10, R14), 8 met on paper, 2 met by design, and R13 $6 over the value-engineering target (HMN-CAL-001 v0.4).
- The photoreal renders (`media/render-*.png`), `media/card.png` and `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept saddle, the three-rod shield and the solid globe rod. They need updating on Amish's Mac, where Blender is.
- The globe boss thread, the anemometer mast size, the fan's hole spacing and the capsule diameter are checked when the parts are bought; they are listed in the design decisions register (HMN-DEC-001).
