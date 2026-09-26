# BOM notes

Costs are indicative USD prices at quantity 1 for a TRL 3 paper design, with a supplier or supplier type for every line. They are not quotes. `docs/04-calcs/sizing.py` (HMN-CAL-001, section L) reads `bom.csv` and checks the totals against `budget_usd` in `project.yaml`.

- Line numbers 1 to 9, 11 and 12 match the callouts in `media/exploded.png`. Line 10 (hardware and consumables) has no callout.
- Sensor head (lines 2 to 12): $130.00, $10.00 over the $120 `budget_usd`. Under HMN-DDR-001 D1 (adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review) the budget covers the sensor head only, so R13 is not met. The $10 is the two parts added at TRL 3: the lanyards (line 11, $3) and the FieldNode pole adapter (line 12, $7).
- FieldNode core (line 1): $126.00, the FieldNode BOM total from FND-CAL-001, costed and budgeted in the FieldNode repo. Full node: $256.00, for information.
- Line 12 replaces the FieldNode kit's 50 mm V-blocks, which only seat on poles up to about 71 mm. The unused V-blocks are still in FieldNode's $126.00.
- Line 3 accuracy is the typical figure from the Sensirion product page. Line 6's start-up speed is a typical low-cost value, not checked against a chosen part.
- The street pole, gateway (TwinKit or a public LoRaWAN network), calibration in CalRig, installation labor and traffic management are not included.
