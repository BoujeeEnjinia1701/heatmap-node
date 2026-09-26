"""HeatMap Node concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; CONCEPT, NOT FOR FABRICATION.

Coordinates in mm. Z up, ground at Z = 0. The existing street pole (grey, not supplied)
stands at the origin. The FieldNode core hangs on the pole's -X face; a horizontal sensor arm
reaches out along +X so the globe and the radiation shield sit clear of the pole and the panel.
Everything is centered on Y = 0 so the cutaway plane passes through the shield and the globe.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Sphere, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all, human_figure

# ---------------- key dimensions (proposed, awaiting Amish) ----------------
POLE_R = 57.0          # 114 mm street light or sign pole
POLE_H = 3400.0        # shown height (real poles are taller)
ARM_Z = 2800.0         # sensor arm height above the pavement
ARM_LEN = 520.0        # arm length from the pole face
ARM_W = 25.0           # 25 mm square aluminium tube
SHIELD_X = 300.0       # radiation shield center, from pole axis
SHIELD_R = 55.0        # 110 mm plates
N_PLATES = 8
PLATE_PITCH = 15.0
GLOBE_X = 500.0        # black globe center, from pole axis
GLOBE_R = 75.0         # 150 mm standard globe
BOX = (90.0, 200.0, 150.0)   # FieldNode enclosure depth (X), width (Y), height (Z)
BOX_Z = 2450.0


def tube3(a, b, r):
    """Round tube between two 3D points."""
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def ring(r_in, r_out, h, z):
    return Pos(0, 0, z) * (Cylinder(r_out, h) - Cylinder(r_in, h + 2))


# ---------------- existing pole (context, no BOM number) ----------------
pole = Pos(0, 0, POLE_H / 2) * Cylinder(POLE_R, POLE_H) + Pos(0, 0, 10) * Box(300, 300, 20)

# ---------------- 1 FieldNode core: enclosure, 6 W panel as sun hood, bracket, antenna ----------------
bx = -POLE_R - 15 - BOX[0] / 2
enclosure = Pos(bx, 0, BOX_Z) * Box(*BOX)
backplate = Pos(-POLE_R - 7.5, 0, BOX_Z + 60) * Box(15, 120, 380)
fn_bands = ring(POLE_R, POLE_R + 4, 20, BOX_Z - 90) + ring(POLE_R, POLE_R + 4, 20, BOX_Z + 210)
panel = Pos(bx - 40, 0, BOX_Z + BOX[2] / 2 + 150) * Rot(0, -35, 0) * Box(200, 290, 17)
posts = (tube3((-POLE_R - 15, -120, BOX_Z + 150), (bx - 20, -120, BOX_Z + BOX[2] / 2 + 150), 6)
         + tube3((-POLE_R - 15, 120, BOX_Z + 150), (bx - 20, 120, BOX_Z + BOX[2] / 2 + 150), 6))
antenna = tube3((bx, 70, BOX_Z - BOX[2] / 2), (bx, 70, BOX_Z - BOX[2] / 2 - 180), 6)
fieldnode = enclosure + backplate + fn_bands + panel + posts + antenna

# ---------------- 8 Arm clamp: saddle and two stainless bands ----------------
saddle = Pos(POLE_R + 15, 0, ARM_Z) * Box(30, 70, 180)
arm_bands = ring(POLE_R, POLE_R + 4, 20, ARM_Z - 70) + ring(POLE_R, POLE_R + 4, 20, ARM_Z + 70)
clamp = saddle + arm_bands

# ---------------- 7 Sensor arm with hangers ----------------
x0 = POLE_R + 30
arm = Pos(x0 + ARM_LEN / 2, 0, ARM_Z) * Box(ARM_LEN, ARM_W, ARM_W)
shield_top = ARM_Z - ARM_W / 2 - 20
globe_c = ARM_Z - ARM_W / 2 - 45 - GLOBE_R
arm = (arm + tube3((SHIELD_X, 0, ARM_Z), (SHIELD_X, 0, shield_top), 6)
       + tube3((GLOBE_X, 0, ARM_Z), (GLOBE_X, 0, globe_c + GLOBE_R + 12), 6))

# ---------------- 2 Multi-plate radiation shield ----------------
shield = None
for i in range(N_PLATES):
    z = shield_top - i * PLATE_PITCH
    plate = Pos(SHIELD_X, 0, z) * (Cylinder(SHIELD_R, 3) if i == 0 else Cylinder(SHIELD_R, 3) - Cylinder(28, 5))
    shield = plate if shield is None else shield + plate
for a in (0, 120, 240):   # three spacer rods
    rx, ry = SHIELD_X + 42 * math.cos(math.radians(a)), 42 * math.sin(math.radians(a))
    shield = shield + tube3((rx, ry, shield_top), (rx, ry, shield_top - (N_PLATES - 1) * PLATE_PITCH), 2.5)

# ---------------- 3 Air temperature and humidity sensor, inside the shield ----------------
sensor_z = shield_top - (N_PLATES - 1) * PLATE_PITCH / 2
th_sensor = Pos(SHIELD_X, 0, sensor_z) * Cylinder(9, 45)

# ---------------- 4 Black globe, 150 mm thin copper sphere, matte black ----------------
globe = Pos(GLOBE_X, 0, globe_c) * (Sphere(GLOBE_R) - Sphere(GLOBE_R - 1.5))
globe = globe + Pos(GLOBE_X, 0, globe_c + GLOBE_R + 4) * Cylinder(10, 16)   # top boss

# ---------------- 5 Globe temperature probe (NTC bead at the center on a stiff tube) ----------------
probe = (tube3((GLOBE_X, 0, globe_c + GLOBE_R + 12), (GLOBE_X, 0, globe_c), 2.5)
         + Pos(GLOBE_X, 0, globe_c) * Sphere(5))

# ---------------- 6 Cup anemometer on a short mast at the arm tip ----------------
AX = x0 + ARM_LEN - 20
hub_z = ARM_Z + ARM_W / 2 + 170
anemometer = tube3((AX, 0, ARM_Z + ARM_W / 2), (AX, 0, hub_z), 8) + Pos(AX, 0, hub_z) * Cylinder(22, 40)
for a in (30, 150, 270):
    cx, cy = AX + 70 * math.cos(math.radians(a)), 70 * math.sin(math.radians(a))
    anemometer = anemometer + tube3((AX, 0, hub_z + 10), (cx, cy, hub_z + 10), 2.5)
    anemometer = anemometer + Pos(cx, cy, hub_z + 10) * ((Sphere(22) - Sphere(20)) - Pos(20 * math.cos(math.radians(a + 90)), 20 * math.sin(math.radians(a + 90)), 0) * Box(40, 40, 50))

# ---------------- 9 Sensor harness (M12 leads from the enclosure to the sensors) ----------------
hx = -POLE_R - 20
harness = (tube3((bx + 20, -60, BOX_Z - BOX[2] / 2), (bx + 20, -60, BOX_Z - BOX[2] / 2 - 60), 4)
           + tube3((bx + 20, -60, BOX_Z - BOX[2] / 2 - 60), (hx, -62, BOX_Z - BOX[2] / 2 - 60), 4)
           + tube3((hx, -62, BOX_Z - BOX[2] / 2 - 60), (hx, -62, ARM_Z - 40), 4)
           + tube3((hx, -62, ARM_Z - 40), (x0, -20, ARM_Z - 20), 4)
           + tube3((x0, -20, ARM_Z - 20), (AX, -20, ARM_Z - 20), 4)
           + tube3((SHIELD_X, -20, ARM_Z - 20), (SHIELD_X, -12, sensor_z + 20), 3)
           + tube3((GLOBE_X + 25, -20, ARM_Z - 20), (GLOBE_X + 8, -8, globe_c + GLOBE_R + 14), 3))

# The kit's cutaway cutter is centered on Z = 0, so the model is shifted down to put the arm at Z = 0.
# Ground level is then Z = -ARM_Z. The pole and the person are context (hero and isometric only).
SHIFT = Pos(0, 0, -ARM_Z)
pole = SHIFT * pole
fieldnode, shield, th_sensor, globe, probe, anemometer, arm, clamp, harness = (
    SHIFT * s for s in (fieldnode, shield, th_sensor, globe, probe, anemometer, arm, clamp, harness))

person = human_figure(1750.0, x=1150.0, y=0.0, z=-ARM_Z)
person.name = "a 1.75 m person"
context = [Part("existing street pole (not supplied)", pole, "#9CA3AF", None), person]

parts = [
    Part("FieldNode core (enclosure, 6 W panel, cell, radio)", fieldnode, "#CBD5E1", 1, (-420, 0, 0)),
    Part("Multi-plate radiation shield", shield, "#F3F4F6", 2, (0, -350, -250)),
    Part("Air temperature and humidity sensor", th_sensor, "#0EA5E9", 3, (0, -350, -520)),
    Part("Black globe, 150 mm", globe, "#1F2937", 4, (160, 0, -380)),
    Part("Globe temperature probe", probe, "#C2410C", 5, (160, -320, -120)),
    Part("Cup anemometer", anemometer, "#0F766E", 6, (180, 0, 260)),
    Part("Sensor arm", arm, "#94A3B8", 7, (0, 0, 120)),
    Part("Arm clamp and bands", clamp, "#D4A017", 8, (0, 0, 0)),
    Part("Sensor harness, M12", harness, "#111827", 9, (-60, -300, -80)),
]

render_all(
    parts, project="HeatMap Node", title="Street heat stress node concept", dwg_no="HMN-DWG-010",
    key_figures=["Air temperature, humidity, 150 mm globe temperature and wind",
                 "Sensor arm at about 2.8 m on an existing pole (proposed)",
                 "Example: 35 C air, 50 C globe, 1 m/s gives MRT about 75 C, WBGT about 31 C (estimate)",
                 "Sensor draw under 1 mW; FieldNode allows about 115 mW (estimate)",
                 "Sensor head about $120; with FieldNode core about $246 (indicative)"],
    scale_figure=False, context=context,
    cut_exclude=("FieldNode core (enclosure, 6 W panel, cell, radio)",
                 "Sensor harness, M12", "Arm clamp and bands"),
    flow={"title": "data flow from street to map (values are estimates)", "unit": "",
          "stages": [("Sensors on the arm", "Ta, RH, Tg, wind\nsampled each 60 s"),
                     ("FieldNode core", "15 min means\nstored in flash"),
                     ("LoRaWAN uplink", "about 20 B,\n96 per node per day"),
                     ("Gateway (TwinKit)", "resends gaps\nfrom node flash"),
                     ("Heat stress model", "MRT and WBGT\n(Liljegren method)"),
                     ("Block-level map", "hourly, open data\nno personal data")]},
)
