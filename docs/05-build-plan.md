---
doc_id: HMN-BLD-001
title: HeatMap Node prototype build plan
project: HeatMap Node
doc_type: Build plan
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: First build plan at TRL 3, with pictures by component and step; design made constructable (HMN-DDR-003)
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Step 12 gives the sensor port pinout decided by Amish on 2026-10-02 (HMN-DEC-001)"
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: "FieldNode core moved above the arm (HMN-DEC-001, item 3): steps 14 to 16 reordered and redrawn, harness leads re-specified, pictures redrawn"
---

# HeatMap Node prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order. The pole is not shown.*

The prototype is one HeatMap Node on a street pole: a sensor head on a short aluminium arm, about 2.8 m up, and a FieldNode core above it, its bottom at about 3.1 m, that powers the sensors and sends their readings by radio. The arm carries a stack of white plates with a small fan on top and an air temperature and humidity sensor inside, a 150 mm black globe with a temperature probe at its centre, and a cup anemometer at its tip. Figure 1 shows the 19 components in the order you make or fit them. Six kinds are made in a small workshop: the arm saddle (a bent aluminium sheet), two arm cheeks, the arm, the printed shield plates, the printed fan cowl and two printed V-blocks that seat the FieldNode core on a large pole. Everything else is bought and fitted, and the FieldNode core is built to its own plan (FND-BLD-001) with these V-blocks in place of its own. The work is sawing, drilling and filing aluminium, one sheet-metal bending job that a local shop can do, 3D printing in ASA, cutting threaded rod and tube to length, and plugging in bought sensors. The sensor head's parts cost about $136, from the bill of materials.

> **Safety:** The node is fitted at about 2.7 to 3.6 m on a street pole next to traffic: that work needs the pole owner's written permission, a lift or a stable ladder with a second person, fall protection and traffic management, and must stay clear of overhead lines and any live parts of a lighting pole. The FieldNode core holds a lithium iron phosphate cell of about 19 Wh; follow the cell stops in its own build plan. The black globe gets hot in sun (about 67 °C at 50 °C air), the cups spin, and the fan starts by itself every 3 minutes once powered. Cut aluminium edges are sharp: deburr everything. Printing ASA gives off fumes; print in a ventilated space.

## 2. What changed to make it buildable

The concept showed what the node does; some of its parts could not be made or fixed as drawn. Each change below keeps what the node does, and all of them are recorded in decision record HMN-DDR-003, open for Amish's review.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Arm saddle | A closed tray 110 wide with a round seat for one pole size | A channel bent from 3 mm sheet, 120 wide, with a V notch in each flange lined with rubber trim (Figures 2 and 3) | A sheet can be bent this way, and the V seats any pole from 60 to 200 mm |
| Arm to saddle | No fixing | Two angle cheeks bolted to the saddle, the arm bolted between them through crush sleeves (Figure 5) | Every joint is face to face and bolted |
| Strap bands | Rings through the saddle | Through slots in the saddle and across its front (Figure 3) | The buckle sits where it can be reached |
| Shield | Three rods through solid plates, two of them inside the fan cowl; hung on one unfixed rod | Four rods clear of the cowl, printed bosses between plates, two rods up through the arm on spacers (Figure 10) | The stack is clamped and hangs rigidly from the arm |
| Fan and cowl | Floating, no fixing | Fan flat on the top plate, cowl on legs over the fan's corner holes, four screws through all three (Figure 13) | One set of screws holds both |
| Sensor | Floating in the stack | Held in a hub printed on the third plate (Figure 11) | Stays at the centre of the air path |
| Globe hanger | A solid rod meeting the probe at the same point | A hollow threaded brass tube, nutted to the arm; the probe runs down inside it (Figure 16) | The hanger and the probe share one path |
| Anemometer | Standing on the arm with no fixing | Mast through the arm, pinned with one bolt; arm 10 mm longer (Figure 17) | Cannot tip or turn |
| Harness and lanyards | Passing through parts; ending at the arm | Rerouted round every part; lanyards looped round the arm | Every cable and wire has a real path |
| FieldNode core position | Below the arm, its bottom at 2.15 m, with the sensor leads running up the pole to the arm | Above the arm, its bottom at 3.11 m so that its antenna whip clears the arm by 100 or more; the leads run from the ports up the pole and down to the arm | The sensor head no longer shades the core's solar panel, and the core's lid is reached from the same ladder or lift that fits the arm |
| FieldNode adapter | Flat blocks for one pole size, covering FieldNode's band slots | V-blocks with band slots and inserts at FieldNode's screw holes (Figure 15) | Fits the FieldNode back plate with no new holes |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Root" is the end of the arm at the pole, "tip" the far end; "left" and "right" are as seen standing at the arm tip, looking back at the pole. Workshop tolerance is 0.5 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4.

### 3.1 Arm saddle

![Figure 2. Making sketch of the arm saddle](../cad/drawings/HMN-DWG-101.png)

*Figure 2. Arm saddle making sketch (HMN-DWG-101).*

**What it is and what it is made from.** The bracket that the arm bolts to and that the strap bands pull against the pole. Aluminium sheet 3 mm thick, 5052-H32 (it bends without cracking), bent into a channel 120 wide, 180 tall and 40 deep.

**How to make it.**

1. Cut a blank 120 wide and about 250 long. Ask the bending shop for the exact length for its bend allowance: the web must be 180 outside and each flange must stand 40 out from the web's outer face.
2. At each end of the blank (these become the flanges), mark a 120° V centred on the width: 110.9 wide at the end, its point 32 in from the end. Saw and file to the lines. About 4.5 of material stays at each corner.
3. On the web, drill four 6.6 holes for the cheek screws: 35 each side of the centre line, 65 and 115 up from the bottom bend line.
4. Cut four band slots 3 wide and 16 tall: 55 each side of the centre line, centred 20 in from each bend line. Chain drill 3 mm and file square.
5. Bend both flanges 90° the same way, inside radius about 3 mm.
6. Deburr every edge and hole. Push rubber edge trim over both V edges, starting at the point of the V.

**How it fits the parts next to it.**

![Figure 3. Joint 1: arm saddle on the pole](05-build-plan/joint-01.png)

*Figure 3. The pole bears on the trimmed V edges of both flanges; each band runs round the back of the pole, through two slots in the web and across its front.*

The pole touches both edges of each V through the trim: a 114 mm pole 29 each side of centre, a 60 mm pole 15 each side and a 200 mm pole 50 each side, always inside the notch. The flat web faces away from the pole and carries the cheeks (Figure 5). The two bands sit 70 above and below the arm's centre line, clear of the cheeks.

**Check before moving on.** Hold the saddle against a 114 mm tube: it must not rock, and both flanges must touch the tube through the trim with the web square to the tube.

### 3.2 Arm cheeks (make 2)

![Figure 4. Making sketch of the arm cheek](../cad/drawings/HMN-DWG-102.png)

*Figure 4. Arm cheek making sketch (HMN-DWG-102).*

**What it is and what it is made from.** Two short angles that grip the root of the arm and bolt it to the saddle. Aluminium equal angle 40 x 40 x 3, 6063.

**How to make it.**

1. Cut two 80 lengths; square and deburr the ends.
2. Flat leg (the one that goes on the saddle): two 6.6 holes, 22.5 from the outside corner of the angle, 15 and 65 up from the bottom end.
3. Upright leg (the one that grips the arm): two 6.6 holes at mid-height (40 up), 12 and 32 out from the outside face of the flat leg.
4. Clamp the two upright legs back to back and drill them together so the holes match. The two cheeks are mirror images.

**How it fits the parts next to it.**

![Figure 5. Joint 2: arm root between the cheeks](05-build-plan/joint-02.png)

*Figure 5. The arm's end bears on the saddle web between the cheeks; two M6 bolts pass through both cheeks, the arm and a crush sleeve inside the arm.*

Each flat leg lies flat on the front of the web, held by two M6 x 16 button-head screws put in from inside the saddle with nyloc nuts on the cheek. The upright legs stand out from the web 25 apart, and the arm fits between them, touching both. The crush sleeves inside the arm stop its 2 mm walls folding when the bolts are tightened.

**Check before moving on.** The holes in both cheeks and the saddle line up without forcing a screw.

### 3.3 Sensor arm

![Figure 6. Making sketch of the sensor arm](../cad/drawings/HMN-DWG-103.png)

*Figure 6. Sensor arm making sketch (HMN-DWG-103).*

![Figure 7. Hole positions along the arm](05-build-plan/arm-holes.png)

*Figure 7. Every hole, measured from the root end, all on the centre line of their face.*

**What it is and what it is made from.** The arm that holds the shield, the globe and the anemometer about 250 to 500 out from the pole. Aluminium square tube 25 x 25 x 2, 6063, 530 long.

**How to make it.**

1. Cut 530 of tube; square and deburr both ends. Mark the root end.
2. Through both side walls, on the centre line: 6.6 holes at 12 and 32 from the root (cheek bolts) and a 5.5 hole at 500 (the pin through the anemometer mast).
3. Through the top and bottom walls, on the centre line: 5.5 holes at 178.3 and 270.3 (shield rods), a 10.5 hole at 424.3 (globe hanger tube) and a 16.5 hole at 500.0 (anemometer mast; open it with a step drill).
4. Drill each pair of holes in one pass on a drill press with the tube clamped square, so the two holes of a pair line up.
5. Cut two crush sleeves 21 long from 8 mm aluminium tube with a 0.8 mm wall. Push them in from the root end until they line up with the cheek bolt holes.
6. Push the plastic end plug into the tip.

**How it fits the parts next to it.** The root end bears flat on the saddle web between the cheeks (Figure 5). The shield rods, the globe tube and the anemometer mast pass down through their holes (Figures 10, 16 and 17). The sensor leads run along the side that faces left as you stand at the tip, held by cable ties.

**Check before moving on.** A drill of each hole size passes straight through each pair of holes.

### 3.4 Shield plates (8): seven ring plates and a top plate

![Figure 8. Making sketch of the ring plates](../cad/drawings/HMN-DWG-105.png)

*Figure 8. Ring plate making sketch (HMN-DWG-105), drawn with the sensor hub that only the third plate carries.*

![Figure 9. Making sketch of the top plate](../cad/drawings/HMN-DWG-104.png)

*Figure 9. Top plate making sketch (HMN-DWG-104).*

**What it is and what it is made from.** Eight white plates, 15 apart, that shade the sensor from the sun and let air through. UV-stable white ASA, printed flat in an enclosed printer, 4 walls and at least 40 % infill.

**How to make it.**

1. Print six ring plates: 110 across, 3 thick, a 56 centre hole, and four bosses 10 across and 12 tall around 5.5 rod holes on a 92 circle, 90° apart. Print them bosses up; they need no supports.
2. Print the seventh ring plate the same, with a hub 22 across and 8 tall in the centre hole on three 4 mm spokes. Its bore is 18.5. Add a 2.5 side hole through the hub wall and form an M3 thread in it with the nylon set screw.
3. Print the top plate: 110 across, 3 thick, a 56 centre hole, four 5.5 rod holes on the same 92 circle, and four 4.4 fan screw holes on a 50 square, centred, on the diagonals between the rod holes. No bosses.
4. Remove any stringing from the holes with a drill of the hole size.

**How it fits the parts next to it.**

![Figure 10. Joint 3: a long shield rod through the stack and the arm](05-build-plan/joint-03.png)

*Figure 10. The bosses of each plate carry the plate above. An acorn nut under the bottom plate and a nut on the top plate clamp the stack; the two rods in line with the arm continue up through a spacer and the arm to a nut on top.*

![Figure 11. Joint 5: the sensor in its hub](05-build-plan/joint-05.png)

*Figure 11. The sensor sits in the hub of the third plate at the centre of the stack; its lead leaves between the second and third plates.*

From the bottom, the order is six plain ring plates, then the hub plate, then one plain ring plate, then the top plate: the hub plate is the third from the top. Four M5 stainless threaded rods pass through all eight plates. The two rods in line with the arm are 192 long; the other two are 121 long.

**Check before moving on.** The eight plates stack 108 tall on the rods with even 12 mm gaps, and the sensor capsule slides into the hub and is held by the set screw.

### 3.5 Fan cowl

![Figure 12. Making sketch of the fan cowl](../cad/drawings/HMN-DWG-106.png)

*Figure 12. Fan cowl making sketch (HMN-DWG-106).*

**What it is and what it is made from.** A lid that keeps rain off the fan and turns its air out sideways. UV-stable white ASA, printed lid down.

**How to make it.**

1. Print a lid 76 x 76 x 3 on four legs 8 x 8 and 12 tall, the legs on a 50 square.
2. Drill a 4.4 hole down through each leg and the lid if the print has closed it.

**How it fits the parts next to it.**

![Figure 13. Joint 4: fan and cowl on the top plate](05-build-plan/joint-04.png)

*Figure 13. The fan sits flat on the top plate; the cowl's legs stand on the fan's corners; four M4 screws hold all three.*

The fan sits flat on the top plate over its centre hole, blowing upward. The cowl's legs stand on the fan's four corners, lifting the lid 12 above the fan. Four M4 x 40 pan-head screws go down through the lid, the legs, the fan's corner holes and the top plate, with nuts under the plate. The lid edge is at least 4 from every rod and spacer.

**Check before moving on.** The lid sits level and the fan turns freely by hand.

### 3.6 Pole adapter V-blocks (make 2)

![Figure 14. Making sketch of the adapter V-block](../cad/drawings/HMN-DWG-107.png)

*Figure 14. Adapter V-block making sketch (HMN-DWG-107).*

**What it is and what it is made from.** Two blocks that seat the FieldNode core on a street pole of 60 to 200 mm, in place of FieldNode's own V-blocks, which fit only small poles. ASA, printed at 100 % infill with 5 walls.

**How to make it.**

1. Print each block standing on its 110 x 38 face: 110 wide, 30 tall, 38 deep, with a 120° V across the whole width, its point 31.8 in from the pole face and 6.2 from the flat back.
2. The print includes two band slots 3.5 wide and 16 tall that run right through from the V to the back, 51 each side of centre and centred on the height.
3. In the flat back, 18 each side of centre and centred on the height, make holes for M4 brass heat-set inserts, 8 deep, sized for the inserts you have. Press the inserts in with a soldering iron until flush.

**How it fits the parts next to it.**

![Figure 15. Joint 8: adapter V-block between the pole and the FieldNode back plate](05-build-plan/joint-08.png)

*Figure 15. The block's flat back sits on the back of the FieldNode back plate; each band passes round the pole, through the block and the plate, and across the plate's front.*

The flat back sits flat on the back face of the FieldNode back plate, where FieldNode's own V-blocks would go, 20 and 270 up from the plate's bottom edge. FieldNode's two M4 countersunk screws per block go in from the front of its plate into the inserts. The block's band slots line up with the plate's band slots. A 114 mm pole touches both faces of the V about 15 in from the pole face.

**Check before moving on.** Each block seats on a 114 mm tube without rocking, and a strip of band passes straight through block and plate slots together.

### 3.7 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **FieldNode core (line 1).** Build it to the FieldNode build plan FND-BLD-001, hot-climate version with its sun shield, but leave out its two V-blocks and its band clamps: the adapter V-blocks (section 3.6) and the 13 mm strap bands take their place.
- **Temperature and humidity sensor (line 3).** SHT45-class digital sensor in an 18 mm capsule at least 45 long with a membrane cap, on a lead long enough to reach the arm (about 0.4 m), with its plug on the free end.
- **Black globe (line 4).** A 150 mm thin-wall copper float ball with a top boss threaded M10 x 1 (or an adapter to M10 x 1). Clean it, key the surface with fine abrasive and spray it matte black outside, two coats. Its hanger is an 86 mm length of M10 x 1 hollow brass lamp rod (7 mm bore) with three M10 x 1 nuts.

![Figure 16. Joint 6: the globe hanger tube through the arm](05-build-plan/joint-06.png)

*Figure 16. The hollow tube screws into the globe's boss and is locked with a nut; a nut below and a nut above the arm hold it. The probe runs down inside the tube to the globe's centre.*

- **Globe probe (line 5).** A 10 k thermistor bead on a stiff 5 mm stem about 165 long, so the bead sits at the globe's centre with the stem's top 4 above the tube. Calibrate it before fitting, as the calibration plan says.
- **Cup anemometer (line 6).** Three-cup, pulse output, on a 16 mm tube mast with its cable leaving at the foot. Cut the mast so it stands 170 above the arm and 15 below it, and drill a 5.5 hole across it 27.5 above its foot for the pin.

![Figure 17. Joint 7: anemometer mast through the arm tip](05-build-plan/joint-07.png)

*Figure 17. The mast passes down through the arm and one M5 bolt pins arm and mast together.*

- **Shield rods and spacers (line 2).** M5 316 stainless threaded rod cut to two lengths of 192 and two of 121; two spacers 41 long cut from 8 mm aluminium tube with a 5.3 bore; four M5 acorn nuts and six M5 nuts.
- **Fan (line 13).** 60 x 60 x 15, 5 V, ball bearing, corner holes on a 50 square for M4.
- **Rubber edge trim and strap bands (lines 8 and 12).** Edge trim for 3 mm sheet with about 1.5 of rubber on the edge. Four 13 mm 316 stainless strap bands with buckles, two for the saddle and two for the adapter, cut to length for the pole on site (about 0.5 m each on a 114 mm pole).
- **Sensor harness (line 9).** Two outdoor cables, lead A about 1.2 m and lead B about 1.4 m long, with M12 5-pin A-coded plugs at the core end. At the sensor end, lead A ends in a plug for the temperature and humidity sensor and a two-wire tail for the fan; lead B ends in a tail for the probe and a tail for the anemometer, each with a sealed heat-shrink breakout.
- **Lanyards (line 11).** Two 1.5 mm 316 stainless wire lanyards with ferrules and snap hooks, about 150 long.
- **Fixings (line 10).** Stainless: 2 x M6 x 40 hex bolts and 4 x M6 x 16 button-head screws with nyloc nuts; 1 x M5 x 35 bolt with a nyloc nut; 4 x M4 x 40 pan-head screws with nuts; 1 nylon M3 set screw; 25 mm square tube end plug; about 12 UV-stable cable ties 400 long and a bag of short ones; sealant.

## 4. Putting it together

Steps 1 to 12 are done on the bench. Step 13 is done on the bench with the FieldNode core, and steps 14 to 16 at height on the pole. In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in.

### Step 1: rubber trim onto the saddle

![Step 1](05-build-plan/step-01.png)

Push the trim over both V edges, starting at the point of each V and working out to the corners. Trim it flush with the corners.

### Step 2: cheeks onto the saddle

![Step 2](05-build-plan/step-02.png)

Four M6 x 16 button-head screws from inside the saddle, nyloc nuts on the cheeks, snug only so the cheeks can still move a little.

### Step 3: arm between the cheeks

![Step 3](05-build-plan/step-03.png)

Slide the arm's root between the cheeks until it bears on the web, with the crush sleeves lined up. Two M6 x 40 bolts, heads on the right, nyloc nuts on the left. Tighten these two bolts, then the four cheek screws. Check the arm is square to the web.

### Step 4: start the shield stack

![Step 4](05-build-plan/step-04.png)

Stand the four rods upright, acorn nuts at the bottom, the two long rods opposite each other. Slide on the six plain ring plates one at a time, bosses up, then the hub plate.

### Step 5: sensor into the hub

![Step 5](05-build-plan/step-05.png)

Push the capsule up through the rings into the hub until its top is level with the top of the hub, and nip the nylon set screw. Lay its lead out over the hub between two rods, at 45° to them, on the side the leads will run.

### Step 6: close the stack

![Step 6](05-build-plan/step-06.png)

Fit the last ring plate over the lead, then the top plate. Put a nut on each rod on the top plate and tighten finger tight plus a quarter turn: the plastic must not crack.

### Step 7: fan and cowl

![Step 7](05-build-plan/step-07.png)

Fan flat on the top plate over its hole, label up so it blows upward, its leads toward the sensor lead. Cowl on the fan, legs on the corners. Four M4 x 40 screws through lid, legs, fan and plate, nuts under the plate (reach in through the gap below it), snug.

### Step 8: hang the shield on the arm

![Step 8](05-build-plan/step-08.png)

Drop a spacer over each long rod. Lift the shield until the long rods pass up through the arm, the spacers bearing on the arm's underside. Fit a nut on each rod on top of the arm and tighten until the stack no longer moves. **Hold point:** the stack hangs square under the arm with no gap at either spacer.

### Step 9: hang the globe

![Step 9](05-build-plan/step-09.png)

Screw the hanger tube 14 into the globe's boss with a nut, lock the nut. Feed the probe down the tube until its bead sits at the centre (its stem top 4 above the tube top) and seal the tube's top round the stem. Run the lower nut onto the tube, push the tube up through the arm and fit the top nut; set the globe 45 below the arm and tighten both nuts against the arm.

### Step 10: anemometer onto the arm tip

![Step 10](05-build-plan/step-10.png)

Feed the mast down through the arm until its pin hole lines up with the arm's side holes, with the cups' cable at the foot. One M5 x 35 bolt through arm and mast, nyloc nut.

### Step 11: retention lanyards

![Step 11](05-build-plan/step-11.png)

Fit one lanyard through a 2 mm hole drilled in the top plate between two rods, on the right-hand side, and loop it round the arm; fit the other round the globe's boss under the lock nut and loop it round the arm. Close both snap hooks. Each loop must be snug but must not carry load.

### Step 12: sensor leads along the arm

![Step 12](05-build-plan/step-12.png)

Plug the sensor's plug into lead A and join the fan's two wires to its tail; join the probe and the anemometer to lead B's tails. The pins follow FieldNode's candidate pinout (HMN-DEC-001): on port A, the sensor's I2C lines on data pins 2 and 4, with sensor and fan on the switched rail; on port B, the thermistor on analog pin 5 and the anemometer pulse on pin 2. Run both leads along the left side of the arm with a short cable tie every 80, and leave the rest of each lead coiled at the root. **Hold point:** the leads pass outside the cheek bolt heads and nothing touches the cups.

### Step 13: adapter V-blocks onto the FieldNode core

![Step 13](05-build-plan/step-13.png)

On the FieldNode core built to its own plan without its V-blocks: two M4 countersunk screws per block from the front of its back plate into the inserts, snug.

### Step 14: sensor head onto the pole

![Step 14](05-build-plan/step-14.png)

The sensor head, assembled on the bench, goes on first, with the arm axis at 2.8 m and the arm toward the equator. Hold the saddle on the pole, pass each band round the pole, through its two web slots and across the web front, and tension each band with the band tool to its maker's setting for about 1,000 N and lock the buckle. Check the arm is level. **Hold point:** safety stop S3.

### Step 15: FieldNode core onto the pole above the arm

![Step 15](05-build-plan/step-15.png)

Lift the core, with its V-blocks on, to the pole on the same side as the arm, panel facing the equator, so that its bottom is about 310 above the top of the arm and its antenna whip clears the arm by 100 or more. Pass each band round the pole, through its block and plate slots and across the plate front, below and above the box, and tension and lock it as in step 14. **Check:** from the ladder or lift position that fitted the arm, the core's lid opens fully and its screws can be reached. If it cannot be reached, fit the core instead on the pole's east or west face at the same height, panel still toward the equator.

### Step 16: leads up the pole to the ports

![Step 16](05-build-plan/step-16.png)

Plug lead A into port A and lead B into port B under the core, leaving a drip loop below each plug. Run both leads down the pole on its left side, outside the core's bands, with a long cable tie every 300, then over the top of the saddle's upper flange, down the left side of the saddle and out along the arm. **Hold point:** safety stop S4.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of HMN-REQ-001.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Pole fit | R10 | Fit the saddle and one V-block on 60, 114 and 200 mm tubes on the bench | Both V faces (or both trimmed edges) touch each tube; each band closes with adjustment to spare |
| Clamp hold | R11 | Hang 2 kg on the arm tip and push sideways at the tip by hand with the head on a 114 mm tube | No slip or turn at the bands; no movement at any bolt |
| Fan | R1 | Power the fan from a 5 V bench supply for 6 s; hold a tissue strip under the bottom plate and beside the cowl | Air is drawn in at the bottom and leaves under the lid; no rubbing noise |
| Sensor readings | R1, R2, R3 | With the core running, read air temperature, humidity and globe temperature indoors | All three read within 1 °C (or 5 %RH) of a reference thermometer and hygrometer in still air |
| Wind pulse | R4 | Spin the cups by hand | Pulses counted; the calm share reads zero while spinning |
| Arm deflection | R11 | Dial gauge at the tip; 10 N sideways at the anemometer | Under 1 mm (0.31 mm expected at a 20 m/s gust) |
| Mass | R15 | Weigh the sensor head before it goes on the pole | 4 kg or less (2.08 kg estimated) |
| Fitting time | R10 | Time steps 14 to 16 with two people from one lift | 30 minutes or less (37 minutes estimated) |
| Privacy | R12 | Look over the parts list and the board | No camera, microphone or radio scanning part |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before the first cut.** Safety glasses on; the tube, angle and sheet clamped before drilling; no gloves near a turning drill.
- **S2. Before any work on the FieldNode core.** Its own safety stops (FND-BLD-001, section 6) are passed; its fuse stays out until its plan allows it.
- **S3. Before going up the pole.** Written permission from the pole owner; the pole checked for its rating against about 420 N·m of added wind moment at its base; a lift or a stable ladder with a second person; fall protection; traffic management as local rules require; no overhead line within reach and no live parts open on a lighting pole. Tools and small parts tethered or in a bag.
- **S4. Before the leads are plugged in.** Every nut on the rods, hanger tube and mast is tight; both lanyards are closed round the arm; the cups spin freely; hands clear of the fan, which starts by itself every 3 minutes once the core is powered.
- **S5. Whenever the head is worked on later.** Unplug lead A before touching the shield (the fan); let the globe cool or wear gloves in sun; stop the cups by hand before working near them.

## 7. Tools, skills and workspace

**Tools.** Hacksaw with a 24 teeth per inch blade; bench vice with soft jaws; drill press; drills 2.5 to 10.5 mm and a step drill to 20 mm; flat and half-round files; deburring tool; scriber, engineer's square, steel rule and calipers; 3D printer with an enclosure that prints ASA, bed at least 120 x 120 mm; soldering iron with an insert tip; spanners 8, 10 and 17 mm; 3 and 4 mm hex keys; screwdrivers; strap band tool for 13 mm bands; dial gauge; spring balance to 20 N; scale to 5 kg; multimeter; 5 V bench supply. The sheet bending is a job for a local sheet-metal shop with a press brake if you have no folder for 3 mm aluminium.

**Skills.** No certified trade is needed for the bench work: basic metalwork (marking out, sawing, drilling, filing), 3D printing in ASA, and plugging and splicing low-voltage leads. All circuits are extra-low voltage (5 V at most at the sensors). Work at height on a street pole needs whatever training and permits the pole owner and local rules require.

**Workspace.** A bench about 1.2 x 0.6 m; a metalwork corner kept apart from the electronics so chips stay off them; a ventilated place for the printer.

**Personal protective equipment.** Safety glasses for cutting and drilling; cut-resistant gloves for sheet and cut tube; hearing protection when sawing; a hard hat, high-visibility clothing and fall protection at the pole.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`, 399 checks); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/HMN-DWG-101` to `HMN-DWG-107`.
- General arrangement: `cad/drawings/HMN-DWG-001.pdf`, Rev P4.
- Calculations: `docs/04-calcs/01-sizing.md` (HMN-CAL-001 v0.4) and `docs/04-calcs/sizing.py`; wind and clamp [H1] to [H6], fit [J1], mass [K1], [K2], cost [L1], [L2].
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (HMN-DDR-003), with HMN-DDR-001 and HMN-DDR-002; open items in `docs/06-design-decisions.md` (HMN-DEC-001).
- Requirements: `docs/03-requirements.md` (HMN-REQ-001 v0.6).
- FieldNode core: its build plan FND-BLD-001 and drawing FND-DWG-001 Rev P3, in the FieldNode repo.
