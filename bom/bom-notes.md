# BOM notes

Costs are indicative USD prices at quantity 1 for a TRL 3 paper design, with a supplier or supplier type for every line. They are not quotes. `docs/04-calcs/sizing.py` (HMN-CAL-001 v0.6, section L) reads `bom.csv` and checks the totals against `budget_usd` in `project.yaml`.

- Line numbers 1 to 9 and 11 to 13 match the callouts in `media/exploded.png`. Line 10 (hardware and consumables) has no callout.
- Sensor head (lines 2 to 11 and 13): $136.00. `budget_usd` ($130) is a hypothetical value-engineering target, not a limit (Amish, 2026-10-01): value-engineering target USD 130, estimated cost of the constructable design USD 136, USD 6 over the target. The design for construction (HMN-DDR-003) repriced lines 2, 4, 8, 10 and 12 for the parts that make the node buildable (cheeks, wider saddle and trim, a fourth rod and spacers, the globe hanger tube, bolts, sleeves, an end plug and cable ties): $9 on the head. Cost drivers and savings worth trying are in the design decisions register (HMN-DEC-001).
- FieldNode side (lines 1 and 12): $156.00. Line 1 is the hot-climate FieldNode node with its sun shield, $148.00 after FieldNode's own design for construction (FND-DDR-003), costed in the FieldNode repo. Full node: $292.00, for information.
- Line 12 replaces the FieldNode kit's V-blocks and band clamps, which only seat small poles. The unused parts are still in FieldNode's $148.00. A large-pole FieldNode kit variant is listed as a cross-repo action.
- Line 3 accuracy is the typical figure from the Sensirion product page. Line 6's start-up speed and line 13's power and flow are typical values for the class, not checked against a chosen part.
- The street pole, gateway (TwinKit or a public LoRaWAN network), calibration in CalRig, installation labor and traffic management are not included.
- Line 9 (harness) is re-specified for the FieldNode core above the arm (HMN-DEC-001, item 3, 2026-10-02): lead A about 1.2 m and lead B about 1.4 m instead of 1.5 m each; the price stays $12.00 because the connectors set it. Totals are unchanged: sensor head $136.00, full node $292.00.
