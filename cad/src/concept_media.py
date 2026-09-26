"""HeatMap Node concept media (TRL 3), built from the parametric model in cad/src/model.py.

Run from the repo root:  python cad/src/concept_media.py
CONCEPT, NOT FOR FABRICATION. Key figures quote HMN-CAL-001 (docs/04-calcs/sizing.py).

The kit's cutaway cutter is centered on Z = 0 and at the mean Y of the parts it cuts, so the
scene is shifted down by the arm height (pavement at Z = -arm_z), and the FieldNode core, its
pole adapter, the harness and the lanyards are left out of the cutaway. The section then
passes through the middle of the shield and the globe. The pole and a 1.75 m person are
context parts (hero and isometric only).
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Pos  # noqa: E402
from concept import Part, render_all, human_figure  # noqa: E402
from model import PARAMS as P, BOM, build_parts, derived, pole_context  # noqa: E402

D = derived(P)
m = build_parts(P)

STYLE = {  # model key: (color, exploded offset in mm)
    "fieldnode": ("#CBD5E1", (0, -420, 0)),
    "shield": ("#F3F4F6", (0, -350, -250)),
    "th_sensor": ("#0EA5E9", (0, -350, -520)),
    "globe": ("#1F2937", (160, 0, -380)),
    "probe": ("#C2410C", (160, -320, -120)),
    "anemometer": ("#0F766E", (180, 0, 260)),
    "arm": ("#94A3B8", (0, 0, 120)),
    "clamp": ("#D4A017", (0, 0, 0)),
    "harness": ("#111827", (-60, -300, -80)),
    "lanyard": ("#B45309", (60, 250, 60)),
    "adapter": ("#D4A017", (0, -200, -60)),
}
parts = []
for key, (num, name) in BOM.items():
    color, off = STYLE[key]
    parts.append(Part(name, m[key], color, num, off))

person = human_figure(1750.0, x=1150.0, y=0.0, z=0.0)
person.name = "a 1.75 m person"
context = [Part("existing street pole (not supplied)", pole_context(P), "#9CA3AF", None), person]

SHIFT = P["arm_z"]
for p in parts + context:
    p.shape = Pos(0, 0, -SHIFT) * p.shape

render_all(
    parts, project="HeatMap Node", title="Street heat stress node concept", dwg_no="HMN-DWG-010",
    key_figures=["Air temperature, humidity, 150 mm globe temperature and wind",
                 "Sensors at about 2.7 m on an existing pole; FieldNode core below",
                 "Example: 35 C air, 40 %RH, 50 C globe, 1 m/s: MRT 74.8 C, WBGT 31.7 C (HMN-CAL-001)",
                 "Sensor draw 0.12 mW against a 100 mW FieldNode allowance",
                 "Sensor head $130 (budget $120); with FieldNode core $256; node 4.68 kg"],
    scale_figure=False, context=context,
    cut_exclude=tuple(BOM[k][1] for k in ("fieldnode", "adapter", "harness", "lanyard", "clamp")),
    flow={"title": "data flow from street to map (values from HMN-CAL-001)", "unit": "",
          "stages": [("Sensors on the arm", "Ta, RH, Tg, wind\nsampled each 60 s"),
                     ("FieldNode core", "15 min means\nstored in flash"),
                     ("LoRaWAN uplink", "20 B payload,\n96 per node per day"),
                     ("Gateway (TwinKit)", "resends gaps\nfrom node flash"),
                     ("Heat stress model", "MRT and WBGT\n(Liljegren method)"),
                     ("Block-level map", "hourly, open data\nno personal data")]},
)
