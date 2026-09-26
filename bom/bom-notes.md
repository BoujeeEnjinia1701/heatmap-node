# BOM notes

Costs are indicative USD prices at quantity 1 for a TRL 3 paper design, with a supplier or supplier type for every line. They are not quotes. `docs/04-calcs/sizing.py` (HMN-CAL-001 v0.2, section L) reads `bom.csv` and checks the totals against `budget_usd` in `project.yaml`.

- Line numbers 1 to 9 and 11 to 13 match the callouts in `media/exploded.png`. Line 10 (hardware and consumables) has no callout.
- Sensor head (lines 2 to 11 and 13): $127.00, $3.00 within the $130 `budget_usd` (raised from $120 by a budget top-up Amish approved on 2026-09-26), so R13 is met on paper. Under HMN-DDR-002 (decided by Amish, 2026-09-25) the pole adapter (line 12) counts against the FieldNode core and the saddle (line 8) is formed from 3 mm sheet ($8.00 to $5.00); those two bring the head to $120.00, and the aspiration fan and cowl (line 13, $7.00) add the $7.
- FieldNode side (lines 1 and 12): $141.00. Line 1 is the hot-climate FieldNode node with its sun shield, $134.00 (base $126.00 plus the $8.00 shield, FND-CAL-001 v0.2), costed and budgeted in the FieldNode repo. Full node: $268.00, for information.
- Line 12 replaces the FieldNode kit's 50 mm V-blocks, which only seat on poles up to about 71 mm. The unused V-blocks are still in FieldNode's $126.00. A large-pole FieldNode kit variant is listed as a cross-repo action.
- Line 3 accuracy is the typical figure from the Sensirion product page. Line 6's start-up speed and line 13's power and flow are typical values for the class, not checked against a chosen part.
- The street pole, gateway (TwinKit or a public LoRaWAN network), calibration in CalRig, installation labor and traffic management are not included.
